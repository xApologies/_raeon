"""Pass-05 source-pinned State binding for the compiled match-tempo contract.

This binding is entered only by Genesis admission/transform/closure. Native
State publication, INT programs and Rainbow Road remain the execution paths;
the Port supplies intents and explicitly admitted effects, never legality.
Historical v1 conformance is dormant once the current match is adopted.
"""
import copy
import json

from raeon_genesis_horizon.toolchain import digest
from raeon_genesis_horizon.application import effective_view_owner

ABI = 'raeon-match-tempo-v1'
PLAYERS = ('player_1','player_2')
LEGACY_COLOR = {'SET_ACTIVE_PLAYER','REFRESH_FIELDS','GENERATE_FIELD','SPEND_PRIME','WHITE_RESTORE_PRIME'}


def reject():
    raise ValueError('ADMISSION_REJECTED')


def opponent(owner):
    if owner not in PLAYERS:
        reject()
    return PLAYERS[1-PLAYERS.index(owner)]


class Mechanics:
    def __init__(self, topology, nodes):
        self.t, self.s, self.c, self.nodes = topology, topology.s, topology.color, nodes
        self.values = nodes.Values(self.s.ints)
        self.contract = json.loads((self.s.h.root/'data/game/pass-05-runtime.json').read_text(encoding='utf8'))
        self.rules = self.contract['rules']

    @property
    def enabled(self):
        return self.s.state.get('match_tempo',{}).get('abi') == ABI

    @property
    def state(self):
        return self.s.state['match_tempo']

    @property
    def defense_open(self):
        return self.enabled and self.state.get('defense',{}).get('status') == 'OPEN'

    def event(self, name, **value):
        self.state['history'].append(dict(event=name,revision=self.s.h._state['revision']+1,**value))

    def trusted(self, policy):
        if self.s.context['grant']['issuer'] != 'CONFORMANCE_ONLY' or self.s.context['grant']['effect'].get('policy') != policy:
            reject()

    def authorize_action(self, spec):
        op = self.s.context['intent']['operation']
        if not self.enabled:
            if spec.get('abi') == ABI and op not in ('ADOPT_PASS05','SETUP_MATCH','REQUEST_OPEN_RULE'):
                reject()
            return
        if self.state['status'] == 'MATCH_COMPLETE' or op in LEGACY_COLOR:
            reject()
        if self.defense_open and op not in ('DEFENSE_RESTORE','DEFENSE_PASS','REQUEST_OPEN_RULE'):
            reject()
        if spec.get('abi') == ABI or self.state['phase'] == 'SETUP':
            return
        if op in ('INITIALIZE_INVENTORY','SHUFFLE_DECK','DRAW_ONE','BATCH_TO_HAND'):
            reject()  # No setup/draw bypass of the current match contract.
        if spec.get('effect_source','').startswith('data/cycles/cycle_01/utilities/'):
            self.utility(self.s.context['grant']['effect'].get('card'))
            return  # Exact effect admission, never a universal Utility window.
        if self.state['phase'] != 'ACTIVE' or self.c.state['active_player'] != self.s.context['owner']:
            reject()

    def admit_plan(self, plan):
        if not self.enabled or plan['spec'].get('abi') == ABI:
            return
        if plan.get('destination','').endswith('_hand'):
            self.capacity(self.s.state['collections'][plan['destination']]['owner'],len(plan['selected']))
        source = plan['spec'].get('effect_source','')
        if source.startswith('data/cycles/cycle_01/utilities/'):
            card = self.utility(self.s.context['grant']['effect'].get('card'))
            if card['catalog'] != 'source:'+source:
                reject()

    def capacity(self, owner, incoming, removing_special=0):
        current = len(self.s.state['collections'][owner+'_hand']['members'])
        special = self.state.get('compensation') if self.enabled else None
        if special and special['owner'] == owner and not special['consumed']:
            current += 1
        if current + incoming - removing_special > self.rules['hand_maximum']:
            reject()

    def timing(self, card):
        effect = self.s.context['grant']['effect']
        expected = {'phase':self.state['phase'],'turn':self.state['turn'],
                    'window':self.state.get('defense',{}).get('id') if self.defense_open else None}
        if (self.defense_open or effect.get('policy') != 'ADMITTED_CARD_EFFECT' or
                effect.get('card') != card or effect.get('timing') != expected):
            reject()

    def utility(self, identity):
        card = self.s.state['cards'].get(identity)
        owner = self.s.context['owner']
        if not card or card['category'] != 'Utility' or card['owner'] != owner or card['location'] != owner+'_hand':
            reject()
        self.timing(identity)
        return card

    def live_active(self):
        if not self.enabled or self.state['phase'] != 'ACTIVE' or self.defense_open or self.c.state['active_player'] != self.s.context['owner']:
            reject()

    def target(self, args):
        return self.c.target(args)

    def generation(self, field, prime, operation):
        if self.c.owner(field) != self.s.context['owner'] or self.c.owner(prime) != self.s.context['owner'] or field['availability'] != 'READY':
            reject()
        return {'source':field['id'],'target':prime['id'],'target_kind':'prime','amount':field['current_magnitude'],
                'direction':'RESTORE','operation':operation,'result':self.values.restore(prime,field['current_magnitude']),
                'origin':field['space'],'destination':prime['slot'],'consume_field':True}

    def spending(self, source, kind, target, amount, direction, operation, response=False):
        if self.c.owner(source) != self.s.context['owner'] or source['id'] == target['id']:
            reject()
        record = self.c.catalog[source['identity_key']]
        if direction not in record['directions'] or (response and direction != 'RESTORE'):
            reject()
        friendly = self.c.owner(target) == self.s.context['owner']
        if not ((direction == 'RESTORE' and friendly) or (direction == 'DEGRADE' and not friendly and not response)):
            reject()
        remaining = self.values.spend(source,amount)
        if kind == 'prime':
            result = (self.values.restore if direction == 'RESTORE' else self.values.degrade)(target,amount)
        else:
            if direction == 'RESTORE' and amount > target['native_maximum']-target['current_magnitude']:
                reject()
            result = self.values.add(target['current_magnitude'],amount if direction == 'RESTORE' else -min(amount,target['current_magnitude']))
        return {'source':source['id'],'target':target['id'],'target_kind':kind,'amount':amount,'direction':direction,
                'operation':operation,'result':result,'remaining':remaining,'origin':source['slot'],
                'destination':target['slot'] if kind == 'prime' else target['space']}

    def admission(self, spec):
        op = self.s.context['intent']['operation']
        if spec != self.contract['actions'].get(op):
            reject()
        args,owner = self.s.context['arguments'],self.s.context['owner']
        plan = {'kind':'extension','spec':copy.deepcopy(spec),'operation':op}
        if op == 'REQUEST_OPEN_RULE':
            reject()  # No operation supplies missing authority, including timer/target/tie law.
        if op == 'ADOPT_PASS05':
            self.trusted('TRUSTED_PASS05_MIGRATION')
            if self.enabled:
                reject()
            self.c.validate()
            return plan
        if op == 'SETUP_MATCH':
            self.trusted('TRUSTED_FAIR_BINARY_SETUP')
            if ((self.enabled and self.state['phase'] != 'SETUP') or args['first_player'] not in PLAYERS or
                    self.s.context['grant']['effect'].get('outcome') != args['first_player']):
                reject()
            opening = {}
            for player in PLAYERS:
                if len(self.s.state['inventories'].get(player,[])) != self.rules['constructed_deck'] or self.s.state['collections'][player+'_hand']['members']:
                    reject()
                deck = self.s.state['collections'][player+'_deck']['members']
                if len(deck) < self.rules['opening_draw']:
                    reject()
                self.capacity(player,7+int(player != args['first_player']))
                opening[player] = list(deck[:7])
            return dict(plan,first_player=args['first_player'],opening=opening)
        if op in ('BEGIN_TURN','NORMAL_DRAW','END_ACTIVE','ADVANCE_TURN'):
            self.trusted('TRUSTED_MATCH_CONTROL')
            expected = {'BEGIN_TURN':'REFRESH','NORMAL_DRAW':'DRAW','END_ACTIVE':'ACTIVE','ADVANCE_TURN':'END'}[op]
            if self.state['phase'] != expected or self.c.state['active_player'] != owner or self.defense_open:
                reject()
            if op == 'NORMAL_DRAW':
                deck = self.s.state['collections'][owner+'_deck']['members']
                if deck:
                    self.capacity(owner,1)
                return dict(plan,draw=list(deck[:1]),owner=owner)
            return dict(plan,owner=owner)
        if op == 'GENERATE_CHARGE':
            self.live_active()
            return dict(plan,transfers=[self.generation(self.c.field(args['field'],args['field_revision']),
                self.c.prime(args['prime'],args['prime_revision']),op)])
        if op == 'SPEND_CHARGE':
            self.live_active()
            source = self.c.prime(args['prime'],args['prime_revision'])
            kind,target = self.target(args)
            return dict(plan,transfers=[self.spending(source,kind,target,int(args['amount']),args['direction'],op)])
        if op in ('DEFENSE_PASS','DEFENSE_RESTORE'):
            if not self.defense_open or self.state['defense']['id'] != args['window'] or self.state['defense']['owner'] != owner:
                reject()
            if op == 'DEFENSE_PASS':
                if args['reason'] not in ('PASS','TIMEOUT'):
                    reject()
                if args['reason'] == 'TIMEOUT':
                    self.trusted('TRUSTED_DEFENSE_TIMEOUT')
                return dict(plan,reason=args['reason'])
            if args['target'] != self.state['defense']['target']:
                reject()
            kind,target = self.target(args)
            source = self.c.prime(args['prime'],args['prime_revision'])
            if source['family'] not in ('Restore','Universal'):
                reject()
            amount = int(args['amount'])
            transfers=[]
            if args['field'] != 'NONE':
                field = self.c.field(args['field'],args['field_revision'])
                generated = self.generation(field,source,op)
                transfers.append(generated)
                if source['id'] == target['id']:
                    if kind != 'prime' or amount != field['current_magnitude']:
                        reject()
                    return dict(plan,transfers=transfers)
                source = copy.deepcopy(source)
                self.values.assign(source,generated['result'])
            elif args['field_revision'] != 0:
                reject()
            transfers.append(self.spending(source,kind,target,amount,'RESTORE',op,True))
            return dict(plan,transfers=transfers)
        if op == 'EFFECT_DRAW':
            card = self.utility(args['utility'])
            effect = self.s.catalog['records'][card['catalog']]['record'].get('effect',{})
            if effect.get('operation') != 'draw' or effect.get('count') not in (1,2,3):
                reject()
            count = effect['count']; self.capacity(owner,count)
            deck = self.s.state['collections'][owner+'_deck']['members']
            if len(deck) < count:
                reject()
            return dict(plan,draw=list(deck[:count]),owner=owner,utility=card['id'])
        if op == 'USE_COMPENSATION':
            obj = self.state.get('compensation')
            if not obj or obj['id'] != args['object'] or obj['owner'] != owner or obj['consumed']:
                reject()
            self.timing(obj['id']); self.capacity(owner,1,1)
            deck = self.s.state['collections'][owner+'_deck']['members']
            if not deck:
                reject()
            return dict(plan,draw=list(deck[:1]),owner=owner)
        if op == 'WHITE_REACTIVATE':
            card = self.utility(args['utility'])
            if card['catalog'] != 'source:data/cycles/cycle_01/utilities/restore_prime.json#':
                reject()
            target = self.c.prime(args['prime'],args['prime_revision'])
            if self.c.owner(target) != owner or target['state'] != 'INACTIVE':
                reject()
            return dict(plan,transfers=[{'operation':op,'source':card['id'],'target':target['id'],'target_kind':'prime',
                'amount':1,'direction':'RESTORE','result':(1,0,0),'origin':owner+'_hand','destination':target['slot']}])
        reject()

    def adopt(self):
        old = copy.deepcopy(self.c.state)
        for p in self.c.state['primes'].values():
            self.values.migrate(p)
        self.c.state['abi'] = self.nodes.ABI
        self.s.state['match_tempo'] = {'abi':ABI,'phase':'SETUP','status':'SETUP','turn':0,'first_player':None,
            'winner':None,'loser':None,'defense':{},'compensation':None,'failed_normal_draws':dict.fromkeys(PLAYERS,0),
            'exhaustion':dict.fromkeys(PLAYERS,None),'history':[],
            'migration':{'from_abi':old['abi'],'to_abi':self.nodes.ABI,'before_commitment':digest(old),
                         'preserved_prime_revisions':{k:v['revision'] for k,v in old['primes'].items()}}}
        for owner in PLAYERS:
            self.s.state['collections'][owner+'_hand']['capacity'] = 10
        self.event('PASS05_ADOPTED')

    def move(self, identities, source, target):
        for identity in identities:
            card = self.s.state['cards'][identity]
            if card['location'] != source:
                reject()
            self.s.state['collections'][source]['members'].remove(identity)
            self.s.h._fault('after_removal')
            self.c._route = (card['binding'],source,target)
            try:
                successor = self.t.transport(identity,source,target)
            finally:
                self.c._route = None
            self.t.remove_edge(source,card['binding']); self.s.add_edge(target,card['binding'])
            card['location'] = target
            card['history'].append({'from':source,'to':target,'version':successor['payload']['native']['instance_id']})
        self.s.state['collections'][target]['members'].extend(identities)

    def transfer(self, item):
        self.c.deliver(item)
        if item.get('consume_field'):
            field = self.t.state['fields'][item['source']]
            field.update(availability='USED',color_revision=field['color_revision']+1)
        elif 'remaining' in item:
            self.values.assign(self.c.state['primes'][item['source']],item['remaining'])
        self.s.h._fault('after_color_source')
        if item['target_kind'] == 'prime':
            self.values.assign(self.c.state['primes'][item['target']],item['result'])
        else:
            field = self.t.state['fields'][item['target']]
            field.update(current_magnitude=item['result'],current_color=self.nodes.COLORS[item['result']],
                         color_revision=field['color_revision']+1)
            if item['result'] == 0:
                self.c.destroy_field(field)
        self.s.h._fault('after_color_target')

    def losers(self):
        losers=[]
        for owner in PLAYERS:
            values=[p for p in self.c.state['primes'].values() if self.c.owner(p)==owner]
            if len(values)==3 and all(p['state']=='INACTIVE' for p in values):
                losers.append(owner)
        return losers

    def terminal(self):
        losers=self.losers()
        if len(losers)>1:
            reject()  # Simultaneous-terminal resolution remains OPEN.
        if losers:
            self.state.update(status='MATCH_COMPLETE',loser=losers[0],winner=opponent(losers[0]))
            self.state['defense']={}
            if not self.state['history'] or self.state['history'][-1]['event']!='MATCH_COMPLETE':
                self.event('MATCH_COMPLETE',loser=losers[0],winner=opponent(losers[0]))
        return bool(losers)

    def legal_options(self, identity):
        if identity in self.c.state['primes']:
            target=self.c.state['primes'][identity]
            if target['H']==0:return []
            room=None
        else:
            target=self.t.state['fields'][identity]
            if not target['active'] or not target['ordinary'] or target['current_magnitude']==0:return []
            room=target['native_maximum']-target['current_magnitude']
            if room<=0:return []
        owner=self.c.owner(target); options=[]
        for p in self.c.state['primes'].values():
            if self.c.owner(p)!=owner or p['family'] not in ('Restore','Universal') or p['H']==0:continue
            if p['id']!=identity and p['H']==p['H_max'] and self.nodes.quantity(p)>0:
                options.append({'prime':p['id'],'field':None})
            for f in self.t.state['fields'].values():
                if not f['ordinary'] or not f['active'] or f['availability']!='READY' or self.c.owner(f)!=owner:continue
                if p['id']==identity:
                    options.append({'prime':p['id'],'field':f['id']});continue
                h,n,r=self.values.restore(p,f['current_magnitude'])
                if h==p['H_max'] and n*p['H_max']+r>0:
                    options.append({'prime':p['id'],'field':f['id']})
        return options

    def close_defense(self, reason):
        self.state['defense'].update(status='CLOSED',reason=reason)
        self.event('DEFENSE_CLOSED',window=self.state['defense']['id'],reason=reason)

    def transform(self, plan):
        op=plan['operation']; owner=self.s.context['owner']
        if op in ('ADOPT_PASS05','SETUP_MATCH') and not self.enabled:
            self.adopt()
        if op=='ADOPT_PASS05':return
        if op=='SETUP_MATCH':
            for player,ids in plan['opening'].items():
                self.move(ids,player+'_deck',player+'_hand')
            second=opponent(plan['first_player'])
            self.s.state['serial']+=1
            name='setup_'+digest([self.s.h.identity,self.s.state['serial']])[:48]
            semantic={'id':name,'kind':'SETUP_COMPENSATION','owner':second,'public':{},'private':{}}
            obj=self.s.instantiate(name,self.s.definition(name,semantic,self.rules['compensation']))
            self.s.add_edge(second+'_hand',name)
            self.state['compensation']={'id':obj['payload']['identity'],'binding':name,'owner':second,'consumed':False}
            self.state.update(first_player=plan['first_player'],phase='REFRESH',status='RUNNING',turn=1,
                              selection='TRUSTED_FAIR_BINARY_OUTCOME')
            self.c.state['active_player']=plan['first_player']
            self.event('MATCH_SETUP',first_player=plan['first_player'],opening_count=7)
        elif op=='BEGIN_TURN':
            refreshed=[f['id'] for f in self.t.state['fields'].values()
                       if f['ordinary'] and f['active'] and f['availability']=='USED' and self.c.owner(f)==owner]
            # The compiled BEGIN_TURN admission chooses the boundary and eligible
            # set; the preserved trusted primitive performs the field updates.
            self.c.transform({'operation':'REFRESH_FIELDS','fields':refreshed})
            self.state['phase']='DRAW'; self.event('OWN_TURN_REFRESH',owner=owner,fields=refreshed)
        elif op in ('NORMAL_DRAW','EFFECT_DRAW','USE_COMPENSATION'):
            if op=='USE_COMPENSATION':
                obj=self.state['compensation']; self.t.remove_edge(owner+'_hand',obj['binding']); obj['consumed']=True
                self.s.h._fault('after_compensation_consumption')
            self.move(plan['draw'],owner+'_deck',owner+'_hand')
            if op=='NORMAL_DRAW':
                self.state['phase']='ACTIVE'
                if not plan['draw']:
                    self.state['failed_normal_draws'][owner]+=1
                    count=self.state['failed_normal_draws'][owner]
                    severity=copy.deepcopy(self.rules['exhaustion'][count-1]) if count<=6 else {'stage':count,'color':None,'magnitude':None}
                    severity.update(target=None,application='OPEN_NOT_APPLIED',stage_7_plus='OPEN' if count>6 else None)
                    self.state['exhaustion'][owner]=severity
                    self.event('FAILED_NORMAL_DRAW',owner=owner,escalation=severity)
            self.event(op,owner=owner,count=len(plan['draw']),generic_resource_cost=0)
        elif op=='END_ACTIVE':
            self.state['phase']='END';self.event('ACTIVE_ENDED',owner=owner)
        elif op=='ADVANCE_TURN':
            self.c.state['active_player']=opponent(owner);self.c.state['authority_revision']+=1
            self.state['phase']='REFRESH';self.state['turn']+=1
            self.event('PLAYER_ADVANCED',owner=opponent(owner))
        elif op=='DEFENSE_PASS':
            self.close_defense(plan['reason'])
        elif 'transfers' in plan:
            for item in plan['transfers']:
                self.transfer(item)
            self.t.update_emergents()  # Consequences precede terminal and response eligibility.
            item=plan['transfers'][-1]
            if op=='DEFENSE_RESTORE':
                self.event('DEFENSE_RESTORE_RESOLVED',target=item['target'])
                self.close_defense('RESTORE')
            elif item['direction']=='DEGRADE':
                self.event('DEGRADE_RESOLVED',target=item['target'],amount=str(item['amount']))
                if not self.terminal():
                    options=self.legal_options(item['target'])
                    if options:
                        target=self.c.state['primes'].get(item['target']) or self.t.state['fields'][item['target']]
                        window=digest([self.s.h.identity,self.s.h._state['revision']+1,item['target']])
                        self.state['defense']={'id':window,'status':'OPEN','owner':self.c.owner(target),
                            'target':item['target'],'options':options,'maximum_responses':1,'timer_seconds':'OPEN',
                            'timeout':'EXPLICIT_PASS_EVENT'}
                        self.event('DEFENSE_OPENED',window=window,target=item['target'])
            else:
                self.event(op,target=item['target'],generic_resource_cost=0)

    def synchronize(self, new_primes=()):
        if self.enabled:
            for identity in new_primes:
                p=self.c.state['primes'][identity]
                if p['C']!=0 or p['H']!=p['H_max']:reject()
                self.values.migrate(p)
            self.terminal()

    def validate(self):
        if self.c.state['abi']!=self.nodes.ABI or self.state['phase'] not in ('SETUP','REFRESH','DRAW','ACTIVE','END'):
            reject()
        if self.state['status'] not in ('SETUP','RUNNING','MATCH_COMPLETE') or type(self.state['turn']) is not int or self.state['turn']<0:
            reject()
        if self.c.state['active_player'] not in (None,*PLAYERS):reject()
        for identity,p in self.c.state['primes'].items():
            card=self.s.state['cards'][identity]; record=self.s.catalog['records'][card['catalog']]['record']
            if (card['category']!='Prime' or p['id']!=identity or p['slot']!=card['location'] or
                self.s.state['collections'][p['slot']]['kind']!='PRIME_POSITION' or
                any(p[k]!=v for k,v in {'catalog':card['catalog'],'identity_key':record['identity_key'],
                    'family':record['family'],'rank':record['rank'],'H_max':record['maximum_magnitude']}.items())):
                reject()
            self.values.validate(p)
        for owner in PLAYERS:
            if self.s.state['collections'][owner+'_hand']['capacity']!=10 or type(self.state['failed_normal_draws'][owner]) is not int or self.state['failed_normal_draws'][owner]<0:
                reject()
            self.capacity(owner,0)
        for key in ('authority_revision','refresh_serial'):
            if type(self.c.state[key]) is not int or self.c.state[key]<0:reject()
        for f in self.t.state['fields'].values():
            if not f['ordinary']:continue
            qmo=self.t.corpus.qmos[f['qmo']]; maximum=self.nodes.COLORS.index(qmo['native_color'])
            if (f['source_sha256']!=digest(qmo) or f['native_color']!=qmo['native_color'] or f['native_maximum']!=maximum or
                type(f['color_revision']) is not int or f['color_revision']<0 or type(f['refresh_serial']) is not int or
                not 0<=f['refresh_serial']<=self.c.state['refresh_serial'] or type(f['current_magnitude']) is not int or
                not 0<=f['current_magnitude']<=maximum or f['current_color']!=self.nodes.COLORS[f['current_magnitude']] or
                f['availability'] not in ('READY','USED') or (f['active'] and f['current_magnitude']==0)):
                reject()
        for row in self.c.state['history']:
            road=self.s.b.road_history[row['road_index']]
            if self.c.road_commitment(road)!=row['road_commitment_sha256'] or not self.c.audit_road(road)['pass']:reject()
        obj=self.state['compensation']
        if obj:
            native=self.s.b.resources[self.s.b.bindings[obj['binding']]]['payload']
            if (native['identity']!=obj['id'] or native['semantic']['kind']!='SETUP_COMPENSATION' or
                    native['semantic']['owner']!=obj['owner'] or obj['owner']!=opponent(self.state['first_player']) or
                    obj['id'] in self.s.state['cards'] or type(obj['consumed']) is not bool):reject()
            hand=self.s.b.resources[self.s.b.bindings[obj['owner']+'_hand']]['payload']['identity']
            count=sum(self.s.b.resources[r]['payload']['source']==hand and self.s.b.resources[r]['payload']['target']==obj['id'] and
                      self.s.b.resources[r]['payload']['relation']=='contains' for r in self.s.b.relations)
            if count!=int(not obj['consumed']):reject()
        losers=self.losers()
        if len(losers)>1 or (losers and self.state['status']!='MATCH_COMPLETE'):reject()
        if self.state['status']=='MATCH_COMPLETE':
            loser=self.state['loser']
            values=[p for p in self.c.state['primes'].values() if self.c.owner(p)==loser]
            if losers!=[loser] or len(values)!=3 or not all(p['H']==0 for p in values) or self.state['winner']!=opponent(loser) or self.defense_open:reject()
        elif self.state['phase']!='SETUP':
            if self.c.state['active_player'] not in PLAYERS or self.state['first_player'] not in PLAYERS or not obj:reject()
        if self.defense_open:
            d=self.state['defense']; target=self.c.state['primes'].get(d['target']) or self.t.state['fields'].get(d['target'])
            if not target or self.state['phase']!='ACTIVE' or self.c.owner(target)!=d['owner'] or d['owner']==self.c.state['active_player'] or d['options']!=self.legal_options(d['target']):reject()

    def project(self, view, authority):
        owner=effective_view_owner(self.s.manifest,authority)
        for identity,p in self.c.state['primes'].items():
            if identity in view['objects']:view['objects'][identity]['fields'].update(self.values.projection(p))
        for identity,f in self.t.state['fields'].items():
            if f['ordinary'] and identity in view['objects']:
                view['objects'][identity]['fields'].update({k:f[k] for k in ('native_maximum','current_magnitude','current_color','availability','color_revision')})
        obj=self.state['compensation']
        for player in PLAYERS:
            hand=view['objects'].get(player+'_hand')
            if hand:
                hand['fields']['capacity']=10
                if obj and obj['owner']==player and not obj['consumed']:
                    hand['fields']['count']+=1
                    if owner==player:
                        hand['fields']['contents'].append(obj['id'])
                        view['objects'][obj['id']]={'identity':obj['id'],'semantic_id':obj['id'],'kind':'SETUP_COMPENSATION',
                            'owner':player,'fields':{'draw':1,'single_use':True,'resource_cost':0,'final_catalog_id':'OPEN','timing':'OPEN'}}
            if player in view['objects']:
                view['objects'][player]['fields']['authority_window']=('DEFENSE' if self.defense_open and self.state['defense']['owner']==player else
                    'ACTIVE' if not self.defense_open and self.state['phase']=='ACTIVE' and self.c.state['active_player']==player and self.state['status']=='RUNNING' else None)
        if 'match' in view['objects']:
            fields=view['objects']['match']['fields']
            fields.update({k:copy.deepcopy(self.state[k]) for k in ('phase','status','turn','first_player','winner','loser','failed_normal_draws','exhaustion','defense')})
            fields.update(active_player=self.c.state['active_player'],refresh_boundary='OWN_TURN_BEGINNING',
                          mulligan_enabled=True,mulligan_procedure='OPEN',ordinary_utility_resource_cost=0)
        return view
