"""Bounded generic State collections invoked by verified Genesis admissions.

No application operation names, card counts, categories, or board limits occur
here. Those policies are attributes of the compiled application handlers. This
service owns native instance/version transport and candidate collection updates;
only Horizon's atomic root publication makes a candidate visible.
"""
from __future__ import annotations

import copy
import hashlib
from collections import Counter

from .toolchain import canonical, digest, file_hash
from .application import read_json, effective_view_owner, relation_visible
from .values import IntegerInterpreter


def deny():
    raise ValueError('ADMISSION_REJECTED')


def validate_arguments(arguments, schema):
    if not isinstance(arguments, dict) or set(arguments) != set(schema):
        deny()
    for name, rule in schema.items():
        value = arguments[name]
        if rule['type'] == 'text':
            if type(value) is not str or not 0 < len(value) <= rule.get('maximum', 256):
                deny()
        elif rule['type'] == 'texts':
            if type(value) is not list or len(value) > rule['maximum']:
                deny()
            if any(type(v) is not str or not 0 < len(v) <= 256 for v in value):
                deny()
        elif rule['type'] == 'integer':
            if type(value) is not int or not rule['minimum'] <= value <= rule['maximum']:
                deny()
        else:
            deny()


class Collections:
    ABI = 'state-collections-v1'

    def __init__(self, horizon, manifest, directory):
        self.h = horizon
        self.b = horizon._backend
        self.manifest = manifest
        self.directory = directory
        self.config = read_json(horizon.root / directory / manifest['collections']['config'])
        self.catalog = read_json(horizon.root / directory / manifest['collections']['catalog'])
        self.verify_catalog()
        self.ints = IntegerInterpreter(horizon.upstream, horizon.root / 'game/core/genesis_horizon/src/values')
        self.context = None
        self.admitted = None
        self.closed = False
        self.unit = None

    def verify_catalog(self):
        for relative, expected in self.catalog['sources'].items():
            path = (self.h.root / relative).resolve()
            if not path.is_relative_to(self.h.root) or file_hash(path) != expected:
                deny()
        for handle, record in self.catalog['records'].items():
            if record['handle'] != handle or record['source'] not in self.catalog['sources']:
                deny()
            value = read_json(self.h.root / record['source'])
            for part in record['pointer'].split('/')[1:]:
                value = value[int(part)] if isinstance(value, list) else value[part]
            if value != record['record'] or digest(value) != record['record_sha256']:
                deny()
            if record['source_sha256'] != self.catalog['sources'][record['source']]:
                deny()

    @property
    def state(self):
        return self.b.application_values

    def initialize(self):
        if self.state:
            deny()
        collections = {}
        for name, definition in self.b.application_definitions.items():
            semantic = definition['semantic']
            kind = semantic['kind']
            if kind in self.config['containers']:
                collections[name] = {'owner': semantic['owner'], 'kind': kind, 'members': [],
                                     'capacity': self.config['containers'][kind]['capacity']}
        self.b.application_values = {'abi': self.ABI, 'catalog': digest(self.catalog),
                                     'cards': {}, 'collections': collections, 'inventories': {},
                                     'grants': {}, 'rng': {}, 'serial': 0, 'inspections': {}}
        for name, collection in collections.items():
            if collection['kind'] in self.config['region_children']:
                child_kind = self.config['region_children'][collection['kind']]
                collection['members'] = [n for n, c in collections.items()
                                         if c['owner'] == collection['owner'] and c['kind'] == child_kind]

    def inspection_scope(self, authority):
        owner = effective_view_owner(self.manifest, authority)
        if owner is None or authority.get('application_id') != self.manifest['id']:
            return None
        return {'application_id': self.manifest['id'], 'view_id': authority['view_id'], 'owner': owner}

    def begin(self, intent, authority):
        validate_arguments(intent['arguments'], self.manifest['operations'][intent['operation']]['arguments'])
        self.context = {'intent': copy.deepcopy(intent), 'owner': authority.get('player_role'),
                        'actor': authority['actor'], 'arguments': copy.deepcopy(intent['arguments']),
                        'inspection_scope': self.inspection_scope(authority)}
        grant = self.state['grants'].get(intent['arguments'].get('grant'))
        expected = {'application': self.manifest['id'], 'match': self.h.identity,
                    'actor': authority['actor'], 'owner': authority.get('player_role'),
                    'operation': intent['operation'], 'expected_revision': self.h._state['revision'],
                    'arguments': {k: v for k, v in intent['arguments'].items() if k != 'grant'}}
        if not grant or grant['used'] or grant['scope'] != expected:
            deny()
        self.context['grant'] = grant
        self.admitted, self.closed, self.unit = None, False, None

    def end(self):
        self.context = self.admitted = self.unit = None

    def resolve(self, value):
        if isinstance(value, str):
            if value.startswith('$arg.'):
                return self.context['arguments'][value[5:]]
            if value.startswith('$grant.'):
                return self.context['grant']['effect'][value[7:]]
            return value.replace('{owner}', self.context['owner'])
        return value

    def owned(self, name, kinds=None):
        value = self.state['collections'].get(name)
        if not value or value['owner'] != self.context['owner'] or (kinds and value['kind'] not in kinds):
            deny()
        return value

    def compare(self, operation, left, right):
        if not self.ints.run(operation, left, right):
            deny()

    def admit(self, geo, attrs):
        if not self.context or self.b.phase != 'application' or not self.b.executing_source or 'COLLECTION_TRANSACTION' not in (self.b.authority or {}).get('operations', []):
            deny()
        expected_source = self.directory + '/' + self.manifest['operations'][self.context['intent']['operation']]['source']
        if self.b.executing_source != expected_source or geo['payload']['binding'] != self.config['root']:
            deny()
        if attrs.get('abi') != self.ABI or self.admitted:
            deny()
        spec = copy.deepcopy(attrs['action'])
        effect = self.context['grant']['effect']
        if effect.get('source') != spec['effect_source']:
            deny()
        plan = {'spec': spec, 'kind': spec['kind']}
        if spec['kind'] == 'materialize':
            owner = self.context['owner']
            roster = self.resolve(spec['records'])
            if owner in self.state['inventories']:
                deny()
            self.compare('equal', len(roster), spec['count'])
            for handle, count in Counter(roster).items():
                record = self.catalog['records'].get(handle)
                if not record or record['category'] not in spec['categories']:
                    deny()
                self.compare('at_most', count, record['copy_limit'])
            destination = self.resolve(spec['destination'])
            self.owned(destination, spec['destination_kinds'])
            plan.update(records=roster, destination=destination)
        elif spec['kind'] == 'permutation':
            source = self.resolve(spec['source'])
            self.owned(source, spec['source_kinds'])
            if self.context['owner'] not in self.state['inventories']:
                deny()
            seed = effect.get('seed')
            if type(seed) is not str or not 16 <= len(seed) <= 256:
                deny()
            previous = self.state['rng'].get(source)
            if previous and previous['seed'] != seed:
                deny()
            plan.update(source=source, seed=seed)
        elif spec['kind'] in ['transfer', 'inspect', 'reorder']:
            if spec['kind'] == 'inspect' and self.context['inspection_scope'] is None:
                deny()
            selection = spec['selection']
            source = self.resolve(selection.get('source'))
            if selection['mode'] == 'top':
                container = self.owned(source, selection['source_kinds'])
                count = self.resolve(selection['count'])
                self.compare('at_most', count, len(container['members']))
                selected = container['members'][:count]
            else:
                selected = self.resolve(selection['items'])
            if len(set(selected)) != len(selected):
                deny()
            self.compare('at_most', spec.get('minimum', 1), len(selected))
            self.compare('at_most', len(selected), spec['maximum'])
            if 'exact' in spec:
                self.compare('equal', len(selected), spec['exact'])
            cards = []
            for identity in selected:
                card = self.state['cards'].get(identity)
                if not card or card['owner'] != self.context['owner']:
                    deny()
                container = self.owned(card['location'], selection['source_kinds'])
                if source and source != card['location']:
                    deny()
                if identity not in container['members'] or card['category'] not in spec['categories']:
                    deny()
                if spec.get('whole_collection') and set(container['members']) != set(selected):
                    deny()
                cards.append(card)
            if spec['kind'] == 'transfer':
                destination = self.resolve(spec['destination'])
                target = self.owned(destination, spec['destination_kinds'])
                if any(card['location'] == destination for card in cards):
                    deny()
                size = self.ints.run('add', len(target['members']), len(cards))
                if target['capacity'] is not None:
                    self.compare('at_most', size, target['capacity'])
                plan['destination'] = destination
            if spec['kind'] == 'reorder':
                if not source or set(selected) != set(self.owned(source)['members'][:len(selected)]):
                    deny()
            plan.update(selected=selected, source=source)
        elif spec['kind'] == 'extend_collection':
            parent = self.resolve(spec['parent'])
            region = self.owned(parent, spec['parent_kinds'])
            self.compare('at_most', self.ints.run('add', len(region['members']), 1), spec['maximum'])
            variant = self.resolve(spec['variant'])
            if variant not in spec['variants'] or effect.get('variant') != variant:
                deny()
            plan.update(parent=parent, variant=variant, capacity=spec['variants'][variant])
        else:
            deny()
        self.admitted = plan
        return self.b._put('ADMISSION', {'source': geo['resource_id'], 'operation': 'COLLECTION_TRANSACTION',
                                       'plan': digest(plan), 'admitted': True}, [geo['resource_id']])

    def run_unit(self, name):
        return self.h._run(self.directory + '/' + self.manifest['collections']['units'][name], 100000)

    def add_edge(self, source, target):
        self.unit = {'source': source, 'target': target, 'mode': 'relation'}
        self.run_unit('relate')
        self.unit = None

    def instantiate(self, name, definition):
        self.unit = {'mode': 'instantiate', 'name': name, 'definition': definition}
        self.run_unit('instantiate')
        self.unit = None
        return self.b.resources[self.b.bindings[name]]

    def definition(self, name, semantic, record):
        value = copy.deepcopy(self.b.profile['definitions'][self.config['representation_template']])
        value.update(mmo_id='STATE:' + digest([self.h.identity, name]), semantic=semantic,
                     provenance_commitment=digest(record))
        return value

    def transform(self, geo, admission, attrs):
        if not self.admitted or not self.context or self.closed or admission['payload'].get('plan') != digest(self.admitted):
            deny()
        if self.b.executing_source != self.directory + '/' + self.manifest['operations'][self.context['intent']['operation']]['source']:
            deny()
        plan, owner = self.admitted, self.context['owner']
        spec = plan['spec']
        if plan['kind'] == 'materialize':
            identities = []
            for handle in plan['records']:
                record = self.catalog['records'][handle]
                self.state['serial'] += 1
                name = 'copy_' + digest([self.h.identity, self.state['serial']])[:48]
                semantic = {'id': name, 'kind': self.config['item_kind'], 'owner': owner, 'public': {}, 'private': {}}
                obj = self.instantiate(name, self.definition(name, semantic, record))
                identity = obj['payload']['identity']
                card = {'id': identity, 'binding': name, 'owner': owner, 'catalog': handle,
                        'category': record['category'], 'catalog_commitment': digest(record),
                        'location': plan['destination'], 'history': [{'from': None, 'to': plan['destination'],
                        'version': obj['payload']['native']['instance_id']}]}
                self.state['cards'][identity] = card
                self.state['collections'][plan['destination']]['members'].append(identity)
                self.add_edge(plan['destination'], name)
                identities.append(identity)
            self.state['inventories'][owner] = identities
        elif plan['kind'] == 'permutation':
            source = plan['source']
            rng = self.state['rng'].setdefault(source, {'algorithm': 'sha256-counter-fisher-yates-rejection-v1',
                                                       'seed': plan['seed'], 'counter': 0})
            members = self.state['collections'][source]['members']
            for i in range(len(members) - 1, 0, -1):
                bound = i + 1
                ceiling = 2**256 - 2**256 % bound
                while True:
                    raw = int.from_bytes(hashlib.sha256(canonical([rng['algorithm'], rng['seed'], rng['counter']])).digest(), 'big')
                    rng['counter'] += 1
                    if raw < ceiling:
                        break
                j = raw % bound
                members[i], members[j] = members[j], members[i]
        elif plan['kind'] == 'transfer':
            for identity in plan['selected']:
                card = self.state['cards'][identity]
                source, target = card['location'], plan['destination']
                self.state['collections'][source]['members'].remove(identity)
                self.h._fault('after_removal')
                self.unit = {'mode': 'transport', 'name': card['binding'], 'source': source, 'target': target}
                self.run_unit('transport')
                if not self.unit.get('closed'):
                    deny()
                successor = self.b.resources[self.unit['successor']]
                self.b.bindings[card['binding']] = successor['resource_id']
                self.unit = None
                a = self.b.resources[self.b.bindings[source]]['payload']['identity']
                self.b.relations = [ref for ref in self.b.relations if not
                    (self.b.resources[ref]['payload']['source'] == a and
                     self.b.resources[ref]['payload']['target'] == identity and
                     self.b.resources[ref]['payload']['relation'] == 'contains')]
                self.add_edge(target, card['binding'])
                card['location'] = target
                card['history'].append({'from': source, 'to': target,
                                        'version': successor['payload']['native']['instance_id']})
            members = self.state['collections'][plan['destination']]['members']
            if spec['placement'] == 'top':
                members[:0] = plan['selected']
            else:
                members.extend(plan['selected'])
        elif plan['kind'] == 'inspect':
            self.state['inspections'][self.context['actor']] = {'revision': self.h._state['revision'] + 1,
                                                              'scope': dict(self.context['inspection_scope']),
                                                              'items': plan['selected']}
        elif plan['kind'] == 'reorder':
            self.state['collections'][plan['source']]['members'][:len(plan['selected'])] = plan['selected']
        elif plan['kind'] == 'extend_collection':
            self.state['serial'] += 1
            name = 'space_' + digest([self.h.identity, self.state['serial']])[:48]
            semantic = {'id': name, 'kind': spec['child_kind'], 'owner': owner,
                        'public': copy.deepcopy(spec['public']), 'private': {}}
            semantic['public'].update(rank=plan['variant'], capacity=plan['capacity'])
            self.instantiate(name, self.definition(name, semantic, spec))
            self.state['collections'][name] = {'owner': owner, 'kind': spec['child_kind'],
                                               'members': [], 'capacity': plan['capacity']}
            self.state['collections'][plan['parent']]['members'].append(name)
            self.add_edge(plan['parent'], name)
        else:
            deny()
        self.context['grant']['used'] = True
        self.context['grant']['outcome_request'] = self.context['intent']['request_id']
        self.validate()
        self.closed = True
        return geo

    def validate(self):
        if self.state.get('abi') != self.ABI or self.state.get('catalog') != digest(self.catalog):
            deny()
        found = []
        for name, collection in self.state['collections'].items():
            if name not in self.b.bindings or len(set(collection['members'])) != len(collection['members']):
                deny()
            if collection['capacity'] is not None and len(collection['members']) > collection['capacity']:
                deny()
            if collection['kind'] in self.config['region_children']:
                if any(c not in self.state['collections'] or self.state['collections'][c]['owner'] != collection['owner'] for c in collection['members']):
                    deny()
                continue
            for identity in collection['members']:
                card = self.state['cards'].get(identity)
                if not card or card['owner'] != collection['owner'] or card['location'] != name:
                    deny()
                native = self.b.resources[self.b.bindings[card['binding']]]['payload']
                if native['identity'] != identity or card['catalog_commitment'] != digest(self.catalog['records'][card['catalog']]):
                    deny()
                a = self.b.resources[self.b.bindings[name]]['payload']['identity']
                edges = [self.b.resources[r]['payload'] for r in self.b.relations]
                if sum(e['relation'] == 'contains' and e['target'] == identity and e['source'] == a for e in edges) != 1:
                    deny()
                found.append(identity)
        if len(found) != len(set(found)) or set(found) != set(self.state['cards']):
            deny()
        inventories = [i for inventory in self.state['inventories'].values() for i in inventory]
        if len(set(inventories)) != len(inventories) or set(inventories) != set(found):
            deny()

    def project(self, view, authority):
        owner = effective_view_owner(self.manifest, authority)
        for name, collection in self.state['collections'].items():
            if name not in view['objects']:
                payload = self.b.resources[self.b.bindings[name]]['payload']
                semantic = payload['semantic']
                view['objects'][name] = {'identity': payload['identity'], 'semantic_id': semantic['id'],
                                         'kind': semantic['kind'], 'owner': semantic['owner'],
                                         'fields': copy.deepcopy(semantic['public'])}
            fields = view['objects'][name]['fields']
            fields.pop('contents', None)
            fields.pop('order', None)
            fields['count'] = len(collection['members'])
            fields['state'] = self.config['populated_states'].get(collection['kind'], 'POPULATED') if collection['members'] else 'EMPTY'
            rule = self.config['containers'][collection['kind']]['visibility']
            visible = rule == 'public' or (rule == 'owner' and owner == collection['owner'])
            if visible:
                fields['contents'] = list(collection['members'])
                for identity in collection['members']:
                    if identity in self.state['cards']:
                        card = self.state['cards'][identity]
                        view['objects'][identity] = {'identity': identity, 'semantic_id': identity,
                            'kind': self.config['item_kind'], 'owner': card['owner'],
                            'fields': {'catalog': card['catalog'], 'category': card['category'], 'location': name}}
            if 'occupant' in fields:
                fields['occupant'] = collection['members'][0] if collection['members'] else None
        inspection = self.state['inspections'].get(authority['actor'])
        scope = self.inspection_scope(authority)
        if scope is not None and inspection and inspection.get('scope') == scope and inspection['revision'] == self.h._state['revision']:
            view['inspection'] = [{'identity': i, 'catalog': self.state['cards'][i]['catalog']} for i in inspection['items']]
        visible = {obj['identity'] for obj in view['objects'].values()}
        owner_id = view['objects'][owner]['identity'] if owner in view['objects'] else None
        existing = {digest(edge) for edge in view['relations']}
        for ref in self.b.relations:
            edge = self.b.resources[ref]['payload']
            if relation_visible(edge, visible, owner_id) and digest(edge) not in existing:
                view['relations'].append(copy.deepcopy(edge))
        return view
