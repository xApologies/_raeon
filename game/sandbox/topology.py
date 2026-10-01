"""Pass-3 application State extension, invoked by source-declared Genesis effects.

This codec stores gestures and source data. It deliberately cannot certify contact:
the accepted mapping is absent. All state lives in the candidate State/checkpoint.
"""
import copy
from math import gcd
from functools import reduce

from raeon_genesis_horizon.toolchain import digest


ABI = 'raeon-topology-values-v1'
POSE_ABI = 'xy-quaternion-integer-v1'


def reject():
    raise ValueError('ADMISSION_REJECTED')


def pose(value):
    if set(value) != {'card', 'x', 'y', 'qw', 'qx', 'qy', 'qz', 'pose_revision'}:
        reject()
    components = [value[k] for k in ('qw', 'qx', 'qy', 'qz')]
    if not any(components):
        reject()
    divisor = reduce(gcd, components)
    q = [n // divisor for n in components]
    if next(n for n in q if n) < 0:
        q = [-n for n in q]
    return {'schema': POSE_ABI, 'frame': 'configuration-local-unmapped',
            'xy_scale': 1000, 'x': value['x'], 'y': value['y'],
            'quaternion_wxyz': q, 'mapping_status': 'OPEN'}


class Extension:
    def __init__(self, service, modules):
        self.s = service
        self.corpus = modules['corpus'].Corpus(service.h.root)

    @property
    def state(self):
        return self.s.state['topology']

    def initialize(self):
        self.s.state['topology'] = {'abi': ABI, 'source_lock': self.corpus.lock_hash,
            'spaces': {}, 'poses': {}, 'fields': {}, 'links': {}, 'emergents': {}}
        self.synchronize()

    def definition(self, definition, record):
        if record.get('category') != 'Field Generator':
            return definition
        fg = self.corpus.fgs[record['handle']]
        # A..H is a source-indexed linear payload, NOT an invented cube basis.
        bits = [int(site in fg['occupancy']) for site in 'ABCDEFGH']
        definition['data'] = {'grid_shape': [8, 1, 1], 'arrays': {
            'chirality_field_3p1p1': [v for bit in bits for v in (bit, 1-bit, fg['chirality_parity'], 0)],
            'chirality_scalar': [1 if fg['chirality_parity'] else -1] * 8,
            'persistence': [1] * 8, 'resolution': [1] * 8, 'admissibility': [1] * 8}}
        definition['data_sha256'] = digest(definition['data'])
        definition['representation_id'] = 'RAEON:SOURCE-INDEXED-FG:v1:' + fg['card_id']
        definition['qmo_source'] = copy.deepcopy(fg)
        definition['qmo_record_sha256'] = digest(fg)
        definition['authority'] = 'Lossless source-indexed occupancy codec; no physical geometry mapping'
        return definition

    def synchronize(self):
        for name, collection in self.s.state['collections'].items():
            if collection['kind'] != 'CONFIGURATION_SPACE':
                continue
            space = self.state['spaces'].setdefault(name, {'members': [], 'membership_revision': 0,
                'pose_revision': 0, 'active_field': None, 'lifecycle': 'EMPTY'})
            if space['members'] != collection['members']:
                for identity in set(space['members']) - set(collection['members']):
                    old_pose = self.state['poses'].get(identity)
                    if old_pose and old_pose['value'] is not None:
                        old_pose['value'] = None
                        old_pose['revision'] += 1
                space['membership_revision'] += 1
                space['members'] = list(collection['members'])
                space['active_field'] = None
            space['lifecycle'] = 'CONFIGURING' if space['members'] else 'EMPTY'
            for identity in space['members']:
                self.state['poses'].setdefault(identity, {'revision': 0, 'value': None})

    def owned_space(self, name, expected):
        collection = self.s.owned(name, ['CONFIGURATION_SPACE'])
        space = self.state['spaces'].get(name)
        if not space or space['membership_revision'] != expected:
            reject()
        return collection, space

    def admit(self, spec):
        self.corpus.verify()
        args = self.s.context['arguments']
        if spec.get('abi') != ABI:
            reject()
        collection, space = self.owned_space(args['space'], args['membership_revision'])
        if spec['operation'] == 'set_poses':
            if spec.get('pose_schema') != POSE_ABI or spec.get('requires') != ['owner', 'membership', 'pose_revision', 'proper_rotation', 'road_close']:
                reject()
            if not 1 <= len(args['poses']) <= spec['maximum']:
                reject()
            values = {}
            for row in args['poses']:
                identity = row['card']
                card = self.s.state['cards'].get(identity)
                if identity in values or identity not in collection['members'] or not card or card['category'] != 'Field Generator':
                    reject()
                if self.state['poses'][identity]['revision'] != row['pose_revision']:
                    reject()
                values[identity] = pose(row)
            return {'kind': 'extension', 'spec': spec, 'space': args['space'], 'poses': values}
        if spec['operation'] == 'reopen':
            return {'kind': 'extension', 'spec': spec, 'space': args['space']}
        # No grant, client witness, catalog membership, or color bypasses these gates.
        if spec['operation'] in ('resolve', 'merge', 'link'):
            if spec['operation'] == 'merge':
                self.owned_space(args['other'], args['other_membership_revision'])
                if args['other'] == args['space']:
                    reject()
            reject()
        reject()

    def transform(self, plan):
        if plan['spec']['operation'] == 'set_poses':
            for identity, value in plan['poses'].items():
                card = self.s.state['cards'][identity]
                regions = [name for name, c in self.s.state['collections'].items()
                           if c['kind'] == 'CONFIGURATION_REGION' and plan['space'] in c['members']]
                if len(regions) != 1:
                    reject()
                # The Road requires distinct endpoints. Round-trip through the owning
                # region inside one candidate; logical membership never leaves the space.
                for source, target in ((plan['space'], regions[0]), (regions[0], plan['space'])):
                    self.s.unit = {'mode': 'transport', 'name': card['binding'], 'source': source, 'target': target}
                    self.s.run_unit('transport')
                    if not self.s.unit.get('closed'):
                        reject()
                    successor = self.s.b.resources[self.s.unit['successor']]
                    self.s.b.bindings[card['binding']] = successor['resource_id']
                    self.s.unit = None
                record = self.state['poses'][identity]
                record['value'] = value
                record['revision'] += 1
                card['history'].append({'from': plan['space'], 'to': plan['space'],
                    'pose_revision': record['revision'], 'version': successor['payload']['native']['instance_id']})
                self.s.h._fault('after_pose')
            self.state['spaces'][plan['space']]['pose_revision'] += 1
        space = self.state['spaces'][plan['space']]
        space['active_field'] = None
        space['lifecycle'] = 'CONFIGURING' if space['members'] else 'EMPTY'

    def validate(self):
        if self.state['abi'] != ABI or self.state['source_lock'] != self.corpus.lock_hash:
            reject()
        if self.state['fields'] or self.state['links'] or self.state['emergents']:
            reject()  # No fabricated or restored activation can bypass the missing mapping.
        for name, space in self.state['spaces'].items():
            collection = self.s.state['collections'][name]
            if space['members'] != collection['members'] or space['active_field'] is not None:
                reject()
            if space['lifecycle'] != ('CONFIGURING' if space['members'] else 'EMPTY'):
                reject()
        for identity, record in self.state['poses'].items():
            if identity not in self.s.state['cards'] or type(record['revision']) is not int or record['revision'] < 0:
                reject()

    def query(self, name, budget=60):
        space = self.state['spaces'][name]
        copies = {i: self.s.state['cards'][i]['catalog'] for i in space['members']}
        result = self.corpus.candidates(list(copies.values()), budget)
        result['partial_relationships'] = self.corpus.potential_edges(copies)
        result['source_lock'] = self.corpus.lock_hash
        result['reason'] = 'G-POSE'
        result['dependency'] = {'space': name, 'members': list(space['members']),
            'membership_revision': space['membership_revision'], 'pose_revision': space['pose_revision'],
            'poses': {i: self.state['poses'][i]['revision'] for i in space['members']}, 'abi': ABI}
        return result

    def preview_merge(self, left, right):
        if left == right or any(n not in self.state['spaces'] for n in (left, right)):
            reject()
        collections = self.s.state['collections']
        if collections[left]['owner'] != collections[right]['owner']:
            reject()
        return {'effect': 'OBSERVED', 'permission': 'POLICY_GATED', 'reason': 'G-MERGE',
                'members': self.state['spaces'][left]['members'] + self.state['spaces'][right]['members'],
                'width_delta_if_admitted': -1, 'result_capacity': None, 'frame_mapping': None,
                'sources': [left, right]}

    def project(self, view, authority):
        self.corpus.verify()
        for name, space in self.state['spaces'].items():
            if name not in view['objects']:
                continue
            fields = view['objects'][name]['fields']
            fields.update(state=space['lifecycle'], active_field=space['active_field'],
                          membership_revision=space['membership_revision'], pose_revision=space['pose_revision'])
            # Only public deployed members; hidden Hand/Deck identities never feed hints.
            fields['topology'] = self.query(name)
            fields['topology']['dependency'].update(view=authority['view_id'])
            for identity in space['members']:
                if identity not in view['objects']:
                    continue
                card = self.s.state['cards'][identity]
                view['objects'][identity]['fields'].update(qmo=copy.deepcopy(self.corpus.fgs[card['catalog']]),
                    qmo_sha256=digest(self.corpus.fgs[card['catalog']]), pose=copy.deepcopy(self.state['poses'][identity]))
        return view
