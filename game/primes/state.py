"""Pass-4 application mechanics within the existing atomic State candidate.

Genesis supplies the exact admission contract and integer arithmetic. All color
delivery uses the existing native Rainbow Road unit. No scheduler lives here.
"""
import copy
import json

from raeon_genesis_horizon.toolchain import digest


ABI = 'raeon-color-prime-values-v1'
COLORS = [None, 'RED', 'ORANGE', 'YELLOW', 'GREEN', 'BLUE', 'VIOLET', 'WHITE']


def reject():
    raise ValueError('ADMISSION_REJECTED')


def prime_state(h, c, maximum):
    if h == 0:
        return 'INACTIVE'
    if h < maximum:
        return 'DAMAGED_NON_OPERATIONAL'
    return 'OPERATIONAL_CHARGED' if c else 'HEALTHY_UNCHARGED'


def restore(h, c, maximum, amount, add):
    if h == 0 or amount > (maximum-h)+(maximum-c):
        reject()  # Reactivation and undefined overflow are separate admissions.
    heal = min(amount, maximum-h)
    return add(h, heal), add(c, add(amount, -heal))


def degrade(h, c, amount, add):
    shield = min(amount, c)
    health = min(add(amount, -shield), h)
    h, c = add(h, -health), add(c, -shield)
    return h, c if h else 0


class Mechanics:
    def __init__(self, topology):
        self.t, self.s = topology, topology.s
        root = self.s.h.root
        self.contract = json.loads((root/'data/game/pass-04-runtime.json').read_text(encoding='utf8'))
        self.catalog = {r['identity_key']:r for r in json.loads(
            (root/'data/cycles/cycle_01/primes/status.json').read_text(encoding='utf8'))['objects']}
        if len(self.catalog) != 14 or self.contract['colors'] != COLORS:
            reject()
        self._route = None
        from genesis_rainbow_road import audit_road_receipt
        self.audit_road = audit_road_receipt

    @staticmethod
    def road_commitment(receipt):
        # Native receipts remain intact in road_history and checkpoint integrity.
        # Semantic State commits content/provenance without host time or paths.
        def stable(value):
            if isinstance(value, dict):
                return {key: sorted(item.values()) if key == 'source_segment_hashes' else stable(item)
                        for key,item in value.items() if key != 'timestamp_ns'}
            if isinstance(value, list):
                return [stable(item) for item in value]
            return value
        return digest({'abi':'rainbow-road-semantic-receipt-v1','receipt':stable(receipt)})

    @property
    def state(self):
        return self.s.state['color_primes']

    def initialize(self):
        self.s.state['color_primes'] = {'abi':ABI, 'active_player':None, 'authority_revision':0,
                                       'refresh_serial':0, 'primes':{}, 'history':[]}

    def add(self, a, b):
        return self.s.ints.run('add', a, b)

    def synchronize(self):
        for identity, card in self.s.state['cards'].items():
            if card['category'] != 'Prime':
                continue
            collection = self.s.state['collections'][card['location']]
            if collection['kind'] != 'PRIME_POSITION':
                if identity in self.state['primes']:
                    reject()  # Bound Primes remain in their same fixed position.
                continue
            record = self.s.catalog['records'][card['catalog']]['record']
            if record != self.catalog.get(record['identity_key']):
                reject()
            maximum = record['maximum_magnitude']
            self.state['primes'].setdefault(identity, {'id':identity, 'slot':card['location'],
                'catalog':card['catalog'], 'identity_key':record['identity_key'], 'family':record['family'],
                'rank':record['rank'], 'H_max':maximum, 'C_max':maximum, 'H':maximum, 'C':0,
                'state':'HEALTHY_UNCHARGED', 'revision':0})

    def field_created(self, field):
        if field['ordinary']:
            maximum = COLORS.index(field['native_color'])
            field.update(native_maximum=maximum, current_magnitude=maximum, current_color=COLORS[maximum],
                         availability='READY', color_revision=0, refresh_serial=self.state['refresh_serial'])
            previous = [f for f in self.t.state['fields'].values() if f['ordinary'] and
                        f['space'] == field['space'] and f['qmo'] == field['qmo'] and
                        set(f['members']) == set(field['members']) and not f.get('destruction')]
            if previous:
                old = max(previous, key=lambda f: f['proof']['dependency']['pose_revision'])
                for key in ('current_magnitude','current_color','availability','refresh_serial'):
                    field[key] = old[key]
                field['color_predecessor'] = old['id']

    def owner(self, value):
        if 'slot' in value:
            return self.s.state['cards'][value['id']]['owner']
        return self.s.state['collections'][value['space']]['owner']

    def window(self, owner):
        active = self.state['active_player']
        if active is None or owner not in ('player_1', 'player_2'):
            reject()
        return 'ACTIVE' if owner == active else 'DEFENSE'

    def prime(self, identity, revision):
        value = self.state['primes'].get(identity)
        if not value or value['revision'] != revision:
            reject()
        return value

    def field(self, identity, revision):
        value = self.t.state['fields'].get(identity)
        if not value or not value['active'] or not value['ordinary'] or value['color_revision'] != revision:
            reject()
        return value

    def target(self, args):
        if args['target'] in self.state['primes']:
            return 'prime', self.prime(args['target'], args['target_revision'])
        return 'field', self.field(args['target'], args['target_revision'])

    def admission(self, spec):
        operation = self.s.context['intent']['operation']
        if spec != self.contract['actions'].get(operation):
            reject()
        args = self.s.context['arguments']
        owner = self.s.context['owner']
        effect = self.s.context['grant']['effect']
        plan = {'kind':'extension', 'spec':copy.deepcopy(spec), 'operation':operation}
        if operation in ('SET_ACTIVE_PLAYER', 'REFRESH_FIELDS'):
            if effect.get('policy') != 'TRUSTED_MATCH_CONTROL' or self.s.context['grant']['issuer'] != 'CONFORMANCE_ONLY':
                reject()
            if operation == 'SET_ACTIVE_PLAYER':
                if args['active_player'] not in ('player_1', 'player_2'):
                    reject()
                return dict(plan, active_player=args['active_player'])
            if not args['fields'] or len(set(args['fields'])) != len(args['fields']):
                reject()
            for identity in args['fields']:
                field = self.t.state['fields'].get(identity)
                if not field or not field['ordinary'] or not field['active'] or self.owner(field) != owner:
                    reject()
            return dict(plan, fields=list(args['fields']))
        window = self.window(owner)
        if operation == 'GENERATE_FIELD':
            source = self.field(args['field'], args['field_revision'])
            target = self.prime(args['prime'], args['prime_revision'])
            if self.owner(source) != owner or self.owner(target) != owner or source['availability'] != 'READY':
                reject()
            if window == 'DEFENSE' and target['family'] == 'Degrade':
                reject()
            amount = source['current_magnitude']
            h, c = restore(target['H'], target['C'], target['H_max'], amount, self.add)
            return dict(plan, source=source['id'], target=target['id'], amount=amount, direction='RESTORE',
                        target_kind='prime', result=[h,c], origin=source['space'], destination=target['slot'])
        if operation == 'WHITE_RESTORE_PRIME':
            target = self.prime(args['prime'], args['prime_revision'])
            if effect.get('policy') != 'ADMITTED_WHITE_RESTORE_PRIME' or self.owner(target) != owner or target['state'] != 'INACTIVE':
                reject()
            return dict(plan, target=target['id'], target_kind='prime', result=[1,0], amount=1,
                        direction='RESTORE', source=None, origin=owner+'_primes', destination=target['slot'])
        if operation != 'SPEND_PRIME':
            reject()
        source = self.prime(args['prime'], args['prime_revision'])
        kind, target = self.target(args)
        direction, amount = args['direction'], args['amount']
        if self.owner(source) != owner or source['state'] != 'OPERATIONAL_CHARGED' or not 0 < amount <= source['C']:
            reject()
        record = self.catalog[source['identity_key']]
        if direction not in record['directions']:
            reject()
        friendly = self.owner(target) == owner
        if not ((direction == 'RESTORE' and friendly) or (direction == 'DEGRADE' and not friendly and window == 'ACTIVE')):
            reject()
        if source['id'] == target['id']:
            reject()  # Self-targeting/spend recycling has no supplied authority.
        if kind == 'prime':
            if target['state'] == 'INACTIVE':
                reject()
            result = restore(target['H'],target['C'],target['H_max'],amount,self.add) if direction == 'RESTORE' else degrade(target['H'],target['C'],amount,self.add)
        else:
            if direction == 'RESTORE' and amount > target['native_maximum']-target['current_magnitude']:
                reject()  # Require an explicit smaller amount; never discard excess.
            result = self.add(target['current_magnitude'], amount if direction == 'RESTORE' else -min(amount,target['current_magnitude']))
        return dict(plan, source=source['id'], target=target['id'], target_kind=kind, amount=amount,
                    direction=direction, result=result, remaining=self.add(source['C'],-amount),
                    origin=source['slot'], destination=target['slot'] if kind == 'prime' else target['space'])

    def route_allowed(self, name, source, target):
        # An exact, ephemeral route capability is minted only inside an already
        # admitted candidate. The generic native binder never receives game rules.
        return self._route == (name,source,target) and self.s.admitted is not None and self.s.context is not None

    def deliver(self, plan):
        self.s.state['serial'] += 1
        name = 'color_'+digest([self.s.h.identity,self.s.state['serial']])[:48]
        record = {'source':plan['source'], 'target':plan['target'], 'amount':plan['amount'],
                  'direction':plan['direction'], 'operation':plan['operation']}
        semantic = {'id':name, 'kind':'COLOR_TRANSFER', 'owner':self.s.context['owner'], 'public':{}, 'private':{}}
        self.s.instantiate(name,self.s.definition(name,semantic,record))
        source_binding = self.s.state['cards'][plan['source']]['binding'] if plan['source'] in self.s.state['cards'] else plan['source']
        if source_binding:
            self.s.add_edge(source_binding,name)
        before = len(self.s.b.road_history)
        self._route = (name,plan['origin'],plan['destination'])
        self.s.unit = {'mode':'transport', 'name':name, 'source':plan['origin'], 'target':plan['destination']}
        try:
            self.s.run_unit('transport')
            if not self.s.unit.get('closed') or len(self.s.b.road_history) != before+1:
                reject()
            successor = self.s.b.resources[self.s.unit['successor']]
            self.s.b.bindings[name] = successor['resource_id']
            road = self.s.b.road_history[-1]
            if road.get('status') != 'CLOSED':
                reject()
            self.state['history'].append(dict(record, transfer=name, road_commitment_sha256=self.road_commitment(road),
                road_index=before, revision=self.s.h._state['revision']+1))
        finally:
            self.s.unit = None
            self._route = None
        self.s.h._fault('after_color_road')

    def set_prime(self, value, h, c):
        value.update(H=h,C=c,state=prime_state(h,c,value['H_max']),revision=value['revision']+1)

    def destroy_field(self, field):
        name = field['space']
        target = self.owner(field)+'_graveyard'
        # Reuse the established card-transfer unit, top placement and identity
        # history law. Only the source-field's exact support membership is moved.
        ids = list(self.s.state['collections'][name]['members'])
        for identity in ids:
            card = self.s.state['cards'][identity]
            self.s.state['collections'][name]['members'].remove(identity)
            self.s.h._fault('after_color_removal')
            self._route = (card['binding'],name,target)
            try:
                successor = self.t.transport(identity,name,target)
            finally:
                self._route = None
            self.t.remove_edge(name,card['binding'])
            self.s.add_edge(target,card['binding'])
            card['location'] = target
            card['history'].append({'from':name,'to':target,'reason':'ZERO_COLOR',
                                    'version':successor['payload']['native']['instance_id']})
        self.s.state['collections'][target]['members'][:0] = ids
        field['active'] = False
        field['availability'] = 'USED'
        field['destruction'] = 'ZERO_COLOR'
        self.t.remove_edge(name,field['id'])
        self.t.deactivate(self.t.state['spaces'][name])
        self.s.h._fault('after_field_destruction')

    def transform(self, plan):
        op = plan['operation']
        if op == 'SET_ACTIVE_PLAYER':
            self.state['active_player'] = plan['active_player']
            self.state['authority_revision'] += 1
            return
        if op == 'REFRESH_FIELDS':
            self.state['refresh_serial'] += 1
            for identity in plan['fields']:
                f = self.t.state['fields'][identity]
                f.update(availability='READY',color_revision=f['color_revision']+1,
                         refresh_serial=self.state['refresh_serial'])
            return
        self.deliver(plan)
        if op == 'GENERATE_FIELD':
            source = self.t.state['fields'][plan['source']]
            source.update(availability='USED',color_revision=source['color_revision']+1)
        elif op == 'SPEND_PRIME':
            source = self.state['primes'][plan['source']]
            self.set_prime(source,source['H'],plan['remaining'])
        self.s.h._fault('after_color_source')
        if plan['target_kind'] == 'prime':
            self.set_prime(self.state['primes'][plan['target']],*plan['result'])
        else:
            target = self.t.state['fields'][plan['target']]
            target.update(current_magnitude=plan['result'],current_color=COLORS[plan['result']],
                          color_revision=target['color_revision']+1)
            if plan['result'] == 0:
                self.destroy_field(target)
        self.s.h._fault('after_color_target')

    def validate(self):
        if (self.state['abi'] != ABI or self.state['active_player'] not in (None,'player_1','player_2') or
            any(type(self.state[k]) is not int or self.state[k] < 0 for k in ('authority_revision','refresh_serial'))):
            reject()
        for identity, p in self.state['primes'].items():
            card = self.s.state['cards'][identity]
            record = self.s.catalog['records'][card['catalog']]['record']
            if (card['category'] != 'Prime' or p['id'] != identity or p['slot'] != card['location'] or
                self.s.state['collections'][p['slot']]['kind'] != 'PRIME_POSITION' or
                any(p[k] != v for k,v in {'catalog':card['catalog'],'identity_key':record['identity_key'],
                    'family':record['family'],'rank':record['rank'],'H_max':record['maximum_magnitude'],
                    'C_max':record['maximum_magnitude']}.items())):
                reject()
            if (any(type(p[k]) is not int for k in ('H','C','revision')) or not 0 <= p['H'] <= p['H_max'] or
                not 0 <= p['C'] <= p['C_max'] or (p['H'] < p['H_max'] and p['C'] != 0) or p['revision'] < 0 or
                p['state'] != prime_state(p['H'],p['C'],p['H_max'])):
                reject()
        for f in self.t.state['fields'].values():
            if not f['ordinary']:
                continue
            qmo = self.t.corpus.qmos[f['qmo']]
            if f['source_sha256'] != digest(qmo) or f['native_color'] != qmo['native_color']:
                reject()
            maximum = COLORS.index(qmo['native_color'])
            if (f['native_maximum'] != maximum or type(f['color_revision']) is not int or f['color_revision'] < 0 or
                type(f['refresh_serial']) is not int or not 0 <= f['refresh_serial'] <= self.state['refresh_serial'] or
                type(f['current_magnitude']) is not int or
                not 0 <= f['current_magnitude'] <= maximum or f['current_color'] != COLORS[f['current_magnitude']] or
                f['availability'] not in ('READY','USED') or (f['active'] and f['current_magnitude'] == 0)):
                reject()
        for row in self.state['history']:
            road = self.s.b.road_history[row['road_index']]
            if self.road_commitment(road) != row['road_commitment_sha256'] or not self.audit_road(road)['pass']:
                reject()

    def project(self, view):
        for identity,p in self.state['primes'].items():
            if identity in view['objects']:
                view['objects'][identity]['fields'].update({k:copy.deepcopy(p[k]) for k in
                    ('slot','identity_key','family','rank','H_max','C_max','H','C','state','revision')})
        for identity,f in self.t.state['fields'].items():
            if f['ordinary'] and identity in view['objects']:
                view['objects'][identity]['fields'].update({k:f[k] for k in
                    ('native_maximum','current_magnitude','current_color','availability','color_revision')})
        if 'match' in view['objects']:
            view['objects']['match']['fields'].update(active_player=self.state['active_player'],
                authority_revision=self.state['authority_revision'],refresh_boundary='OPEN')
        for owner in ('player_1','player_2'):
            if owner in view['objects']:
                view['objects'][owner]['fields']['authority_window'] = None if self.state['active_player'] is None else self.window(owner)
        return view
