"""Pass-06 source-pinned Genesis State binding; no Port-side gameplay authority.

The historical binding stays executable until explicit Pass-06 setup. Every new
operation requires its exact compiled admission, native candidate closure and
source commitments. Movement and color effects use the inherited Rainbow Road.
"""
import copy
import hashlib
import json
from types import SimpleNamespace

from raeon_genesis_horizon.toolchain import canonical, digest
from raeon_genesis_horizon.application import effective_view_owner

ABI = 'raeon-headless-closure-v1'
PLAYERS = ('player_1', 'player_2')


def reject():
    raise ValueError('ADMISSION_REJECTED')


def bind(previous):
    class Mechanics(previous.Mechanics):
        next_abi = ABI

        def __init__(self, topology, nodes):
            super().__init__(topology, nodes)
            self.next_contract = json.loads((self.s.h.root/'data/game/pass-06-runtime.json').read_text(encoding='utf8'))
            if self.current:
                self.rules = self.next_contract['rules']

        @property
        def current(self):
            return self.s.state.get('match_tempo', {}).get('ruleset') == ABI

        def authorize_action(self, spec):
            if not self.current:
                if spec.get('abi') == ABI:
                    if self.enabled or self.s.context['intent']['operation'] != 'P6_SETUP_MATCH':reject()
                    return
                return super().authorize_action(spec)
            op = self.s.context['intent']['operation']
            if self.state['status'] == 'MATCH_COMPLETE':reject()
            if spec.get('abi') == ABI:
                if self.defense_open and op not in ('P6_DEFENSE_RESTORE', 'P6_DEFENSE_PASS', 'P6_OPEN_GUARD'):reject()
                if any(self.state['mulligan_pending'].values()) and op not in ('P6_MULLIGAN', 'P6_OPEN_GUARD'):reject()
                return
            # No old draw, Utility, turn or inspection handler can bypass P6.
            if op not in ('COMMIT_FG', 'SET_FG_POSES', 'REOPEN_CONFIGURATION', 'RESOLVE_CONFIGURATION',
                          'LINK_CONFIGURATION', 'MERGE_CONFIGURATION', 'RETIRE_SUPPORT'):
                reject()
            self.live_active()

        def admit_plan(self, plan):
            if self.current and plan['spec'].get('abi') == ABI:return
            return super().admit_plan(plan)

        def live_active(self):
            super().live_active()
            if self.current and any(self.state['mulligan_pending'].values()):reject()

        def timing(self, identity):
            if not self.current:return super().timing(identity)
            self.live_active()
            effect = self.s.context['grant']['effect']
            if (effect.get('policy') != 'ADMITTED_CARD_EFFECT' or effect.get('card') != identity or
                effect.get('timing') != {'phase':'ACTIVE','turn':self.state['turn'],'window':None}):reject()

        def room(self, owner, removing=0):
            obj = self.state.get('compensation')
            special = int(bool(obj and obj['owner'] == owner and not obj['consumed']))
            return max(0, 10-len(self.s.state['collections'][owner+'_hand']['members'])-special+removing)

        def deck(self, owner):
            return self.s.state['collections'][owner+'_deck']['members']

        def ordered(self, owner, count):
            top = self.deck(owner)[:count]
            if any(set(top)&set(band) for band in self.state['unordered_bottom'][owner]):reject()
            return list(top)

        def draw_plan(self, owner, count, removing=0):
            wanted = min(count, self.room(owner, removing))
            cards = self.ordered(owner, wanted)
            return {'draw':cards, 'failed':wanted-len(cards), 'owner':owner, 'requested':count}

        def seed(self):
            effect = self.s.context['grant']['effect']
            value = effect.get('seed')
            if type(value) is not str or not 16 <= len(value) <= 256:reject()
            return value

        def shuffle(self, owner, seed):
            # Same rejection-sampled deterministic algorithm as the sealed
            # collection shuffle. Seed is trusted entropy, not a client choice.
            rng = {'algorithm':'sha256-counter-fisher-yates-rejection-v1','seed':seed,'counter':0}
            members = self.deck(owner)
            for i in range(len(members)-1, 0, -1):
                bound = i+1; ceiling = 2**256-2**256 % bound
                while True:
                    raw = int.from_bytes(hashlib.sha256(canonical([rng['algorithm'],seed,rng['counter']])).digest(),'big')
                    rng['counter'] += 1
                    if raw < ceiling:break
                j = raw % bound;members[i],members[j] = members[j],members[i]
            self.s.state['rng'][owner+'_deck'] = rng
            self.state['unordered_bottom'][owner] = []

        def admission(self, spec):
            if spec.get('abi') != ABI:
                return super().admission(spec)
            op = self.s.context['intent']['operation']
            if spec != self.next_contract['actions'].get(op):reject()
            action = op.removeprefix('P6_')
            args,owner = self.s.context['arguments'],self.s.context['owner']
            plan = {'kind':'extension','spec':copy.deepcopy(spec),'operation':action,'owner':owner}
            if action == 'OPEN_GUARD':reject()
            if action == 'SETUP_MATCH':
                self.trusted('TRUSTED_FAIR_BINARY_SETUP')
                if self.enabled or args['first_player'] not in PLAYERS or self.s.context['grant']['effect'].get('outcome') != args['first_player']:reject()
                self.c.validate()
                opening = {}
                for player in PLAYERS:
                    if len(self.s.state['inventories'].get(player,[])) != 60 or self.s.state['collections'][player+'_hand']['members']:reject()
                    primes = [p for p in self.c.state['primes'].values() if self.c.owner(p)==player]
                    if len(primes)!=3 or {p['slot'] for p in primes}!={player+'_prime_'+str(n) for n in (1,2,3)}:reject()
                    if len(self.deck(player))<7:reject()
                    opening[player] = list(self.deck(player)[:7])
                return dict(plan, first_player=args['first_player'], opening=opening)
            if not self.current:reject()
            if action == 'MULLIGAN':
                self.trusted('TRUSTED_MULLIGAN_SHUFFLE')
                cards=args['cards']
                if (not self.state['mulligan_pending'][owner] or len(cards)>7 or len(set(cards))!=len(cards) or
                    not set(cards)<=set(self.s.state['collections'][owner+'_hand']['members'])):reject()
                return dict(plan,selected=cards,seed=self.seed())
            if action in ('BEGIN_TURN','NORMAL_DRAW','END_ACTIVE','ADVANCE_TURN'):
                self.trusted('TRUSTED_MATCH_CONTROL')
                phase={'BEGIN_TURN':'REFRESH','NORMAL_DRAW':'DRAW','END_ACTIVE':'ACTIVE','ADVANCE_TURN':'END'}[action]
                if self.state['phase']!=phase or self.c.state['active_player']!=owner or self.defense_open:reject()
                return dict(plan,**self.draw_plan(owner,1)) if action=='NORMAL_DRAW' else plan
            if action == 'GENERATE_CHARGE':
                self.live_active()
                return dict(plan,transfers=[self.generation(self.c.field(args['field'],args['field_revision']),self.c.prime(args['prime'],args['prime_revision']),action)])
            if action == 'SPEND_CHARGE':
                self.live_active();kind,target=self.target(args)
                return dict(plan,transfers=[self.spending(self.c.prime(args['prime'],args['prime_revision']),kind,target,int(args['amount']),args['direction'],action)])
            if action in ('DEFENSE_PASS','DEFENSE_RESTORE'):
                if not self.defense_open or self.state['defense']['id']!=args['window'] or self.state['defense']['owner']!=owner:reject()
                if action=='DEFENSE_PASS':
                    if args['reason'] not in ('PASS','TIMEOUT'):reject()
                    if args['reason']=='TIMEOUT':self.trusted('TRUSTED_DEFENSE_TIMEOUT')
                    return dict(plan,reason=args['reason'])
                if args['target']!=self.state['defense']['target']:reject()
                kind,target=self.target(args);source=self.c.prime(args['prime'],args['prime_revision']);amount=int(args['amount'])
                if source['family'] not in ('Restore','Universal'):reject()
                transfers=[]
                if args['field']!='NONE':
                    field=self.c.field(args['field'],args['field_revision'])
                    generated=self.generation(field,source,action);transfers.append(generated)
                    if source['id']==target['id']:
                        if kind!='prime' or amount!=field['current_magnitude']:reject()
                        return dict(plan,transfers=transfers)
                    source=copy.deepcopy(source);self.values.assign(source,generated['result'])
                elif args['field_revision']!=0:reject()
                transfers.append(self.spending(source,kind,target,amount,'RESTORE',action,True))
                return dict(plan,transfers=transfers)
            if action == 'USE_COMPENSATION':
                obj=self.state['compensation']
                if obj['id']!=args['object'] or obj['owner']!=owner or obj['consumed']:reject()
                self.timing(obj['id'])
                return dict(plan,**self.draw_plan(owner,1,1))
            if action in ('UTILITY','LOOK_UTILITY'):
                card=self.utility(args['utility']);definition=self.next_contract['utilities'].get(card['catalog'])
                if not definition or definition['admission']!='MATURE':reject()
                return self.admit_utility(plan,card,definition,args)
            reject()

        def admit_utility(self, plan, card, definition, args):
            owner=plan['owner'];effect=definition['effect'];family=definition['family'];op=effect['operation']
            plan.update(utility=card['id'],utility_effect=copy.deepcopy(effect))
            if plan['operation']=='LOOK_UTILITY':
                if op not in ('survey','select','deep_survey') or self.s.context['inspection_scope'] is None:reject()
                return dict(plan,look=self.ordered(owner,effect['look_top']))
            selected=args['cards']
            if len(selected)!=len(set(selected)):reject()
            if family=='transduction':
                if selected:reject()
                direction=args['direction']
                if direction not in effect['directions']:reject()
                kind,target=self.target(args);amount=effect['magnitude']
                if args['target_kind']!=kind:reject()
                if (direction=='RESTORE')!=(self.c.owner(target)==owner):reject()
                if kind=='prime':result=(self.values.restore if direction=='RESTORE' else self.values.degrade)(target,amount)
                else:
                    if direction=='RESTORE' and amount>target['native_maximum']-target['current_magnitude']:reject()
                    result=self.values.add(target['current_magnitude'],amount if direction=='RESTORE' else -min(amount,target['current_magnitude']))
                return dict(plan,transfers=[{'source':card['id'],'target':target['id'],'target_kind':kind,'amount':amount,'direction':direction,
                    'operation':'UTILITY_TRANSDUCTION','result':result,'origin':owner+'_hand','destination':target['slot'] if kind=='prime' else target['space']}])
            if family=='white_restore_prime':
                if selected or args['direction']!='RESTORE':reject()
                target=self.c.prime(args['target'],args['target_revision'])
                if args['target_kind']!='prime' or self.c.owner(target)!=owner or target['state']!='INACTIVE':reject()
                return dict(plan,transfers=[{'source':card['id'],'target':target['id'],'target_kind':'prime','amount':1,'direction':'RESTORE',
                    'operation':'WHITE_REACTIVATE','result':(1,0,0),'origin':owner+'_hand','destination':target['slot']}])
            if any(args[k]!='NONE' for k in ('direction','target','target_kind')) or args['target_revision']!=0:reject()
            if op=='draw':
                if selected:reject()
                return dict(plan,**self.draw_plan(owner,effect['count']))
            if op in ('survey','select','deep_survey'):
                top=self.ordered(owner,effect['look_top'])
                if op=='survey':
                    if set(selected)!=set(top):reject()
                    return dict(plan,top=top,selected=selected)
                if len(selected)!=min(1,len(top)) or not set(selected)<=set(top):reject()
                self.capacity(owner,len(selected))
                return dict(plan,top=top,selected=selected,seed=self.seed() if op=='deep_survey' else None)
            if op=='exchange':
                if not set(selected)<=set(self.s.state['collections'][owner+'_hand']['members']):reject()
                if any(self.s.state['cards'][i]['category']=='Prime' for i in selected):reject()
                return dict(plan,selected=selected,**self.draw_plan(owner,len(selected),len(selected)))
            if op=='recover':
                if not effect.get('minimum',effect.get('count',0))<=len(selected)<=effect.get('count',effect.get('maximum_count',0)):reject()
                for identity in selected:
                    c=self.s.state['cards'].get(identity)
                    if not c or c['owner']!=owner or c['location']!=owner+'_graveyard' or c['category']=='Prime':reject()
                    if effect['card_type']!='non-Prime' and c['category']!=effect['card_type']:reject()
                if effect['destination']=='hand':self.capacity(owner,len(selected))
                return dict(plan,selected=selected)
            reject()

        def after_degrade(self, item):
            self.t.update_emergents()
            self.event('DEGRADE_RESOLVED',target=item['target'],amount=str(item['amount']))
            if self.terminal():return
            options=self.legal_options(item['target'])
            if options:
                target=self.c.state['primes'].get(item['target']) or self.t.state['fields'][item['target']]
                window=digest([self.s.h.identity,self.s.h._state['revision']+1,item['target'],len(self.state['history'])])
                self.state['defense']={'id':window,'status':'OPEN','owner':self.c.owner(target),'target':item['target'],
                    'options':options,'maximum_responses':1,'timer_seconds':'CLIENT_TUNABLE_NOT_GENESIS_SEMANTIC','timeout':'EXPLICIT_PASS_EVENT'}
                self.event('DEFENSE_OPENED',window=window,target=item['target'])

        def exhaustion(self, owner):
            self.state['failed_normal_draws'][owner]+=1
            stage=self.state['failed_normal_draws'][owner];color,amount=self.next_contract['accepted_rules']['exhaustion']['stages'][min(stage,7)-1]
            target=next((p for n in (1,2,3) for p in self.c.state['primes'].values() if p['slot']==owner+'_prime_'+str(n) and p['state']!='INACTIVE'),None)
            if target is None:self.terminal();return
            item={'source':owner+'_deck','target':target['id'],'target_kind':'prime','amount':amount,'direction':'DEGRADE',
                  'operation':'EXHAUSTION','result':self.values.degrade(target,amount),'origin':owner+'_deck','destination':target['slot']}
            self.transfer(item)
            severity={'stage':stage,'color':color,'magnitude':amount,'target':target['id'],'slot':target['slot'],'application':'APPLIED'}
            self.state['exhaustion'][owner]=severity
            self.event('FAILED_DRAW',owner=owner,escalation=severity)
            self.after_degrade(item)

        def drain_exhaustion(self):
            while self.state['pending_failed_draws'] and not self.defense_open and self.state['status']!='MATCH_COMPLETE':
                owner=self.state['pending_failed_draws'].pop(0);self.exhaustion(owner)
            if self.state['status']=='MATCH_COMPLETE':self.state['pending_failed_draws']=[]

        def resolve_draw(self, plan):
            owner=plan['owner'];self.move(plan['draw'],owner+'_deck',owner+'_hand')
            self.event('DRAW_RESOLVED',owner=owner,requested=plan['requested'],count=len(plan['draw']),generic_resource_cost=0)
            self.state['pending_failed_draws'].extend([owner]*plan['failed'])
            self.drain_exhaustion()

        def transform(self, plan):
            if plan['spec'].get('abi')!=ABI:return super().transform(plan)
            op=plan['operation'];owner=plan['owner']
            if op=='SETUP_MATCH':
                self.adopt();self.state.update(ruleset=ABI,mulligan_pending=dict.fromkeys(PLAYERS,True),
                    unordered_bottom={p:[] for p in PLAYERS},pending_failed_draws=[],result=None)
                self.rules=self.next_contract['rules'];super().transform(plan);return
            if op=='MULLIGAN':
                self.move(plan['selected'],owner+'_hand',owner+'_deck')
                self.event('MULLIGAN_RETURNED',owner=owner,count=len(plan['selected']))
                self.shuffle(owner,plan['seed']);self.event('MULLIGAN_SHUFFLED',owner=owner)
                self.move(list(self.deck(owner)[:len(plan['selected'])]),owner+'_deck',owner+'_hand')
                self.state['mulligan_pending'][owner]=False
                self.event('MULLIGAN_REDRAWN',owner=owner,count=len(plan['selected']),penalty=0);return
            if op in ('NORMAL_DRAW','USE_COMPENSATION'):
                if op=='NORMAL_DRAW':self.state['phase']='ACTIVE'
                else:
                    obj=self.state['compensation'];self.t.remove_edge(owner+'_hand',obj['binding']);obj['consumed']=True
                    self.s.h._fault('after_compensation_consumption')
                self.resolve_draw(plan);return
            if op=='LOOK_UTILITY':
                self.s.state['inspections'][self.s.context['actor']]={'revision':self.s.h._state['revision']+1,
                    'scope':dict(self.s.context['inspection_scope']),'items':plan['look']}
                return
            if op=='UTILITY' and 'transfers' not in plan:
                effect=plan['utility_effect'];action=effect['operation'];selected=plan.get('selected',[])
                if action=='draw':self.resolve_draw(plan)
                elif action=='exchange':
                    self.move(selected,owner+'_hand',owner+'_graveyard')
                    self.event('EXCHANGE_TO_GRAVEYARD',owner=owner,count=len(selected))
                    self.resolve_draw(plan)
                elif action=='recover':
                    dest=owner+('_hand' if effect['destination']=='hand' else '_deck')
                    self.move(selected,owner+'_graveyard',dest)
                    if dest.endswith('_deck') and selected:
                        members=self.deck(owner);members[:]=selected+[i for i in members if i not in selected]
                elif action=='survey':self.deck(owner)[:len(selected)]=selected
                elif action in ('select','deep_survey'):
                    self.move(selected,owner+'_deck',owner+'_hand')
                    if action=='select':
                        remainder=[i for i in plan['top'] if i not in selected]
                        members=self.deck(owner);members[:]=[i for i in members if i not in remainder]+sorted(remainder)
                        # Sorting is a set serialization codec, never a bottom
                        # order decision. Any operation reaching this band fails.
                        if len(remainder)>1:self.state['unordered_bottom'][owner].append(sorted(remainder))
                    else:self.shuffle(owner,plan['seed'])
                if self.state['status']!='MATCH_COMPLETE':self.event('UTILITY_RESOLVED',effect=action,owner=owner,generic_resource_cost=0)
                return
            if 'transfers' in plan:
                for item in plan['transfers']:self.transfer(item)
                self.t.update_emergents();item=plan['transfers'][-1]
                if op=='DEFENSE_RESTORE':
                    self.event('DEFENSE_RESTORE_RESOLVED',target=item['target']);self.close_defense('RESTORE');self.drain_exhaustion()
                elif item['direction']=='DEGRADE':self.after_degrade(item)
                else:self.event(op,target=item['target'],generic_resource_cost=0)
                return
            super().transform(plan)
            if op=='DEFENSE_PASS':self.drain_exhaustion()

        def terminal(self):
            if not self.current:return super().terminal()
            losers=self.losers()
            if not losers:return False
            winner=None if len(losers)==2 else previous.opponent(losers[0])
            result='DRAW' if len(losers)==2 else 'WIN'
            self.state.update(status='MATCH_COMPLETE',result=result,winner=winner,loser=losers[0] if len(losers)==1 else None,defense={})
            if not self.state['history'] or self.state['history'][-1]['event']!='MATCH_COMPLETE':self.event('MATCH_COMPLETE',result=result,winner=winner,losers=losers)
            return True

        def validate_terminal(self):
            if not self.current:return super().validate_terminal()
            losers=self.losers()
            if bool(losers)!=(self.state['status']=='MATCH_COMPLETE'):reject()
            if losers:
                if self.defense_open:reject()
                expected=('DRAW',None,None) if len(losers)==2 else ('WIN',previous.opponent(losers[0]),losers[0])
                if tuple(self.state[k] for k in ('result','winner','loser'))!=expected:reject()
            elif self.state['result'] is not None or self.c.state['active_player'] not in PLAYERS or not self.state['compensation']:reject()

        def validate_defense(self):
            if not self.current:return super().validate_defense()
            if self.defense_open:
                d=self.state['defense'];target=self.c.state['primes'].get(d['target']) or self.t.state['fields'].get(d['target'])
                if (not target or self.state['phase']!='ACTIVE' or self.c.owner(target)!=d['owner'] or
                    d['options']!=self.legal_options(d['target']) or d['timer_seconds']!='CLIENT_TUNABLE_NOT_GENESIS_SEMANTIC'):reject()

        def validate(self):
            super().validate()
            if not self.current:return
            if set(self.state['mulligan_pending'])!=set(PLAYERS) or any(type(v) is not bool for v in self.state['mulligan_pending'].values()):reject()
            for owner,bands in self.state['unordered_bottom'].items():
                seen=set()
                for band in bands:
                    if len(band)<2 or len(band)!=len(set(band)) or seen&set(band) or not set(band)<=set(self.deck(owner)):reject()
                    seen.update(band)
            if any(owner not in PLAYERS for owner in self.state['pending_failed_draws']):reject()
            if self.state['pending_failed_draws'] and not self.defense_open:reject()

        def project(self, view, authority):
            view=super().project(view,authority)
            if not self.current:return view
            owner=effective_view_owner(self.s.manifest,authority)
            fields=view['objects']['match']['fields']
            fields.update(ruleset=ABI,result=self.state['result'],mulligan_procedure='RETURN_TO_DECK_SHUFFLE_REDRAW_SAME_COUNT',
                mulligan_pending=copy.deepcopy(self.state['mulligan_pending']),defense_seconds='CLIENT_TUNABLE_NOT_GENESIS_SEMANTIC')
            obj=self.state['compensation']
            if obj['id'] in view['objects']:view['objects'][obj['id']]['fields']['timing']='OWN_ACTIVE'
            if owner in PLAYERS:view['objects'][owner+'_deck']['fields']['unresolved_selection_bands']=len(self.state['unordered_bottom'][owner])
            return view
    return SimpleNamespace(Mechanics=Mechanics)
