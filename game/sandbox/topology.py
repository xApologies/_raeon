"""Pass-3 application State extension, invoked by source-declared Genesis effects.

All mutable realization, field, and support state lives in the atomic candidate.
Pass-3B authority supplies the missing mapping without changing source QMOs.
"""
import copy
from collections import Counter
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
    return {'schema': POSE_ABI, 'frame': 'configuration-realization-v1',
            'xy_scale': 1000, 'x': value['x'], 'y': value['y'],
            'quaternion_wxyz': q, 'mapping_status': 'REALIZED'}


class Extension:
    def __init__(self, service, modules):
        self.s = service
        self.corpus = modules['corpus'].Corpus(service.h.root)
        self.realization = modules['realization'].Realization(service.h.root, self.corpus)

    @property
    def state(self):
        return self.s.state['topology']

    def initialize(self):
        self.s.state['topology'] = {'abi': ABI, 'source_lock': self.corpus.lock_hash,
            'realization_lock': self.realization.hash, 'spaces': {}, 'poses': {}, 'fields': {}, 'links': {}, 'emergents': {}}
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

    def deactivate(self, space):
        identity = space['active_field']
        if identity:
            self.state['fields'][identity]['active'] = False
        space['active_field'] = None
        space['capture'] = None
        space['lifecycle'] = 'CONFIGURING' if space['members'] else 'EMPTY'

    def synchronize(self):
        self.corpus.verify()
        self.realization.verify()
        for name, collection in self.s.state['collections'].items():
            if collection['kind'] != 'CONFIGURATION_SPACE':
                continue
            space = self.state['spaces'].setdefault(name, {'members': [], 'membership_revision': 0,
                'pose_revision': 0, 'active_field': None, 'lifecycle': 'EMPTY', 'capture': None})
            if space['members'] != collection['members']:
                # No new capacity/addition policy for derived or subsumed spaces.
                if space['lifecycle'] == 'SUBSUMED' or (set(collection['members'])-set(space['members']) and
                        (space['active_field'] or space.get('derived'))):
                    reject()
                self.deactivate(space)
                for identity in set(space['members']) - set(collection['members']):
                    old_pose = self.state['poses'].get(identity)
                    if old_pose and old_pose['value'] is not None:
                        old_pose['value'] = None
                        old_pose['revision'] += 1
                space['membership_revision'] += 1
                space['members'] = list(collection['members'])
            for identity in space['members']:
                self.state['poses'].setdefault(identity, {'revision': 0, 'value': None})
            if space['lifecycle'] != 'SUBSUMED' and not space['active_field']:
                space['lifecycle'] = 'CONFIGURING' if space['members'] else 'EMPTY'
                evaluations = self.query_verified(name).get('realizations', [])
                space['capture'] = evaluations[0] if len(evaluations) == 1 else None
        self.update_emergents()

    def owned_space(self, name, expected):
        collection = self.s.owned(name, ['CONFIGURATION_SPACE'])
        space = self.state['spaces'].get(name)
        if not space or space['membership_revision'] != expected or space['lifecycle'] == 'SUBSUMED':
            reject()
        return collection, space

    def admit(self, spec):
        self.corpus.verify()
        self.realization.verify()
        args = self.s.context['arguments']
        if spec.get('abi') != ABI:
            reject()
        collection, space = self.owned_space(args['space'], args['membership_revision'])
        if spec['operation'] == 'set_poses':
            if space['active_field'] or space.get('derived'):
                reject()  # Explicit reopen is required before ordinary manipulation.
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
            if spec.get('requires') != ['owner', 'fresh_revisions', 'road_close']:reject()
            if space.get('derived'):
                reject()  # No derived split/reconstruction contract in this pass.
            return {'kind': 'extension', 'spec': spec, 'space': args['space']}
        if spec['operation'] == 'resolve':
            if spec.get('requires') != ['exact_membership', 'complete_query', 'shape_capture',
                    'orientation_capture', 'source_edges', 'fresh_revisions', 'road_close']:
                reject()
            if space['active_field'] or space.get('derived'):
                reject()
            result = self.query(args['space'])
            ready = [r for r in result['realizations'] if r['can_lock']]
            if not result['complete_search'] or len(ready) != 1:
                reject()
            return {'kind':'extension', 'spec':spec, 'space':args['space'],
                    'realization':ready[0], 'dependency':result['dependency']}
        if spec['operation'] == 'merge':
            self.owned_space(args['other'], args['other_membership_revision'])
            if spec.get('requires') != ['resolved_supports', 'disjoint_instances', 'source_valid', 'road_close']:
                reject()
            preview = self.preview_merge(args['space'],args['other'])
            if preview['permission'] != 'VALID':
                reject()
            return {'kind':'extension','spec':spec,'space':args['space'], 'other':args['other'], 'preview':preview}
        # Emergence is passive after committed support changes, not a player spell.
        reject()

    def region(self, name):
        found=[n for n,c in self.s.state['collections'].items()
               if c['kind']=='CONFIGURATION_REGION' and name in c['members']]
        if len(found)!=1:reject()
        return found[0]

    def transport(self, identity, source, target):
        card=self.s.state['cards'][identity]
        self.s.unit={'mode':'transport','name':card['binding'],'source':source,'target':target}
        self.s.run_unit('transport')
        if not self.s.unit.get('closed'):reject()
        successor=self.s.b.resources[self.s.unit['successor']]
        self.s.b.bindings[card['binding']]=successor['resource_id']
        self.s.unit=None
        return successor

    def round_trip(self, identity, name):
        region=self.region(name)
        self.transport(identity,name,region)
        return self.transport(identity,region,name)

    def remove_edge(self, source, target):
        a=self.s.b.resources[self.s.b.bindings[source]]['payload']['identity']
        b=self.s.b.resources[self.s.b.bindings[target]]['payload']['identity']
        self.s.b.relations=[r for r in self.s.b.relations if not
            (self.s.b.resources[r]['payload']['source']==a and self.s.b.resources[r]['payload']['target']==b
             and self.s.b.resources[r]['payload']['relation']=='contains')]

    def create_field(self, name, qmo, proof, supports=None):
        space=self.state['spaces'][name]
        self.s.state['serial']+=1
        identity='field_'+digest([self.s.h.identity,self.s.state['serial']])[:48]
        owner=self.s.state['collections'][name]['owner']
        semantic={'id':identity,'kind':'LOCAL_MANIFOLD_FIELD','owner':owner,'public':{},'private':{}}
        definition=self.s.definition(identity,semantic,qmo)
        definition.update(qmo_source=copy.deepcopy(qmo),qmo_record_sha256=digest(qmo),
                          representation_id='RAEON:SOURCE-QMO-REFERENCE:v1:'+qmo['id'])
        obj=self.s.instantiate(identity,definition)
        self.s.add_edge(name,identity)
        field={'id':identity,'native_identity':obj['payload']['identity'],'qmo':qmo['id'],
               'native_color':qmo['native_color'],'space':name,'members':list(space['members']),
               'active':True,'ordinary':qmo['type']=='LocalManifoldQMO',
               'manifold_id':qmo.get('manifold_id'),'proof':copy.deepcopy(proof),'supports':supports or [],
               'source_sha256':digest(qmo),'realization_lock':self.realization.hash}
        self.state['fields'][identity]=field
        space.update(active_field=identity,lifecycle='RESOLVED',capture=None)
        self.s.h._fault('after_field')
        return field

    def expected_emergents(self):
        supports=sorted((f for f in self.state['fields'].values() if f['active'] and f['ordinary']),key=lambda f:f['id'])
        result={}
        for index,a in enumerate(supports):
            for b in supports[index+1:]:
                pair=self.corpus.pairs.get(tuple(sorted((a['manifold_id'],b['manifold_id']))))
                if not pair or pair['emergent_status']!='VALID':continue
                key='emergent_'+digest([a['id'],b['id'],pair['emergent_qmo']])[:48]
                result[key]={'id':key,'qmo':pair['emergent_qmo'],'supports':[a['id'],b['id']],
                    'spaces':[a['space'],b['space']],'pair_key':pair['pair_key'],
                    'native_color':self.corpus.qmos[pair['emergent_qmo']]['native_color'],
                    'directly_targetable':False,'slot_cost':0,'active':True,
                    'source_sha256':digest(self.corpus.qmos[pair['emergent_qmo']])}
        return result

    def update_emergents(self):
        expected=self.expected_emergents()
        if expected!=self.state['emergents']:
            for identity,old in self.state['emergents'].items():
                if identity not in expected:
                    for support in old['supports']:self.remove_edge(support,identity)
            for identity,entry in expected.items():
                if identity in self.state['emergents']:continue
                qmo=self.corpus.qmos[entry['qmo']]
                semantic={'id':identity,'kind':'EMERGENT_FIELD','owner':None,'public':{},'private':{}}
                definition=self.s.definition(identity,semantic,qmo)
                definition.update(qmo_source=copy.deepcopy(qmo),qmo_record_sha256=digest(qmo),
                                  representation_id='RAEON:SOURCE-QMO-REFERENCE:v1:'+qmo['id'])
                self.s.instantiate(identity,definition)
                for support in entry['supports']:self.s.add_edge(support,identity)
            self.state['emergents']=expected
            self.s.h._fault('after_emergents')

    def transform(self, plan):
        op=plan['spec']['operation'];name=plan['space'];space=self.state['spaces'][name]
        if op=='set_poses':
            for identity,value in plan['poses'].items():
                successor=self.round_trip(identity,name)
                record=self.state['poses'][identity]
                record['value']=value;record['revision']+=1
                self.s.state['cards'][identity]['history'].append({'from':name,'to':name,
                    'pose_revision':record['revision'],'version':successor['payload']['native']['instance_id']})
                self.s.h._fault('after_pose')
            space['pose_revision']+=1
        elif op=='reopen':
            for identity in space['members']:
                successor=self.round_trip(identity,name)
                self.s.state['cards'][identity]['history'].append({'from':name,'to':name,
                    'reason':'reopen','version':successor['payload']['native']['instance_id']})
                value=self.state['poses'][identity]['value']
                if value and 'symbolic' in value:
                    # Keep canonical coordinates but relinquish the live lock.
                    value.pop('symbolic');value['mapping_status']='REALIZED'
                    self.state['poses'][identity]['revision']+=1
            self.deactivate(space)
            space['pose_revision']+=1
        elif op=='resolve':
            if plan['dependency']!=self.query(name)['dependency']:reject()
            proof=plan['realization']
            for identity,target in proof['targets'].items():
                successor=self.round_trip(identity,name)
                record=self.state['poses'][identity]
                record['value']=self.realization.locked_pose(target);record['revision']+=1
                self.s.state['cards'][identity]['history'].append({'from':name,'to':name,
                    'pose_revision':record['revision'],'version':successor['payload']['native']['instance_id']})
                self.s.h._fault('after_lock_pose')
            space['pose_revision']+=1
            proof=copy.deepcopy(proof)
            proof['dependency']=self.query(name)['dependency']
            for edge in proof['edges']:
                edge['a_revision']=self.state['poses'][edge['a']]['revision']
                edge['b_revision']=self.state['poses'][edge['b']]['revision']
            self.create_field(name,self.corpus.base[proof['manifold_id']],proof)
        elif op=='merge':
            other=plan['other'];region=self.region(name)
            if self.region(other)!=region:reject()
            sources=[name,other];fields=[self.state['spaces'][n]['active_field'] for n in sources]
            self.s.state['serial']+=1
            target='fusion_space_'+digest([self.s.h.identity,self.s.state['serial']])[:48]
            owner=self.s.state['collections'][name]['owner']
            semantic={'id':target,'kind':'CONFIGURATION_SPACE','owner':owner,'public':{'derived':True},'private':{}}
            self.s.instantiate(target,self.s.definition(target,semantic,plan['preview']))
            members=list(plan['preview']['members'])
            # Exact population is preserved; capacity/addition policy remains OPEN.
            self.s.state['collections'][target]={'owner':owner,'kind':'CONFIGURATION_SPACE','members':[], 'capacity':None}
            self.state['spaces'][target]={'members':members,'membership_revision':1,'pose_revision':1,
                'active_field':None,'lifecycle':'CONFIGURING','capture':None,'derived':True,'sources':sources}
            for source in sources:
                old=self.state['spaces'][source]
                old['subsumed_members']=list(old['members']);old['subsumed_field']=old['active_field']
                for identity in old['members']:
                    card=self.s.state['cards'][identity]
                    successor=self.transport(identity,source,target)
                    self.remove_edge(source,card['binding']);self.s.add_edge(target,card['binding'])
                    card['location']=target
                    card['history'].append({'from':source,'to':target,'version':successor['payload']['native']['instance_id']})
                    # Composition preserves support-local frames, not an invented puzzle.
                    self.state['poses'][identity]['support_frame']=source
                    self.s.h._fault('after_merge_card')
                self.deactivate(old)
                old.update(members=[],lifecycle='SUBSUMED',subsumed_by=target,membership_revision=old['membership_revision']+1)
                self.s.state['collections'][source]['members']=[]
                self.s.state['collections'][region]['members'].remove(source)
                self.remove_edge(region,source)
            self.s.state['collections'][target]['members']=members
            self.s.state['collections'][region]['members'].append(target)
            self.s.add_edge(region,target)
            qmo=self.corpus.qmos[plan['preview']['result_qmo']]
            self.create_field(target,qmo,{'pair_key':plan['preview']['pair_key'],
                'composition':'disjoint-union-of-locked-support-frames','frames':sources},fields)
        else:reject()

    def validate(self):
        if self.state['abi']!=ABI or self.state['source_lock']!=self.corpus.lock_hash or self.state['realization_lock']!=self.realization.hash:
            reject()
        if self.state['links'] or self.state['emergents']!=self.expected_emergents():reject()
        for name,space in self.state['spaces'].items():
            collection=self.s.state['collections'][name]
            if space['members']!=collection['members']:reject()
            if space['lifecycle']=='SUBSUMED':
                if space['members'] or space['active_field'] or not space.get('subsumed_by'):reject()
                continue
            field=self.state['fields'].get(space['active_field'])
            if field:
                if not field['active'] or field['space']!=name or field['members']!=space['members'] or space['lifecycle']!='RESOLVED':reject()
                qmo=self.corpus.qmos.get(field['qmo'])
                if not qmo or digest(qmo)!=field['source_sha256'] or qmo['native_color']!=field['native_color']:reject()
                if field['ordinary']:
                    proof=field['proof']
                    if not proof['can_lock'] or proof['dependency']!=self.query(name)['dependency']:reject()
                    for identity,target in proof['targets'].items():
                        if self.state['poses'][identity]['value']!=self.realization.locked_pose(target):reject()
                    if Counter(self.s.state['cards'][i]['catalog'] for i in space['members'])!=Counter(qmo['generators']):reject()
                elif not space.get('derived') or len(field['supports'])!=2:reject()
            elif space['active_field'] or space['lifecycle']!=('CONFIGURING' if space['members'] else 'EMPTY'):reject()
        for identity,record in self.state['poses'].items():
            if identity not in self.s.state['cards'] or type(record['revision']) is not int or record['revision']<0:reject()
        for field in self.state['fields'].values():
            if field['active'] and self.state['spaces'][field['space']]['active_field']!=field['id']:reject()

    def query(self, name, budget=60):
        self.corpus.verify()
        self.realization.verify()
        return self.query_verified(name, budget)

    def query_verified(self, name, budget=60):
        space = self.state['spaces'][name]
        copies = {i: self.s.state['cards'][i]['catalog'] for i in space['members']}
        result = self.corpus.candidates_verified(list(copies.values()), budget)
        result['partial_relationships'] = self.corpus.potential_edges(copies)
        result['source_lock'] = self.corpus.lock_hash
        result['reason'] = 'POSE_REQUIRED'
        result['realizations'] = []
        for candidate in result['candidates']:
            evaluated=self.realization.evaluate(candidate['manifold_id'],copies,self.state['poses'],space.get('capture'))
            if evaluated:result['realizations'].append(evaluated)
        result['realization_lock']=self.realization.hash
        live=[e for r in result['realizations'] for e in r['edges'] if e['live']]
        result['partial_relationships']['authoritative_live_edges']=live
        ready=[r for r in result['realizations'] if r['can_lock']]
        if ready and result['complete_search']:
            result.update(permission='ELIGIBLE',pose_closure='CAPTURED',reason=None)
        elif result['realizations']:
            result['reason']='SHAPE_CAPTURE_REQUIRED' if not any(r['shape_capture'] for r in result['realizations']) else 'ORIENTATION_CAPTURE_REQUIRED'
        if space['active_field']:
            result.update(permission='RESOLVED',pose_closure='LOCKED',witness=copy.deepcopy(self.state['fields'][space['active_field']]['proof']))
        result['dependency'] = {'space': name, 'members': list(space['members']),
            'membership_revision': space['membership_revision'], 'pose_revision': space['pose_revision'],
            'poses': {i: self.state['poses'][i]['revision'] for i in space['members']}, 'abi': ABI}
        return result

    def preview_merge(self, left, right):
        if left==right or any(n not in self.state['spaces'] for n in (left,right)):reject()
        collections=self.s.state['collections']
        if collections[left]['owner']!=collections[right]['owner']:reject()
        spaces=[self.state['spaces'][n] for n in (left,right)]
        result={'effect':'OBSERVED','permission':'POLICY_GATED','reason':'RESOLVED_SUPPORTS_REQUIRED',
                'members':spaces[0]['members']+spaces[1]['members'],'width_delta_if_admitted':-1,
                'result_capacity':None,'frame_mapping':None,'sources':[left,right]}
        fields=[self.state['fields'].get(s['active_field']) for s in spaces]
        if not all(f and f['active'] and f['ordinary'] for f in fields):return result
        if set(spaces[0]['members']) & set(spaces[1]['members']):
            result['reason']='SHARED_PHYSICAL_INSTANCE';return result
        pair=self.corpus.pair(fields[0]['manifold_id'],fields[1]['manifold_id'])
        result.update(permission=pair.get('fusion_status','OPEN'),reason=pair.get('fusion_reason','SOURCE_PAIR_ABSENT'))
        if result['permission']=='VALID':
            result.update(result_qmo=pair['fusion_result_qmo'],pair_key=pair['pair_key'],
                          frame_mapping='preserve locked support-local frames')
        return result

    def project(self, view, authority):
        self.corpus.verify()
        self.realization.verify()
        for name, space in self.state['spaces'].items():
            if name not in view['objects']:
                continue
            fields = view['objects'][name]['fields']
            fields.update(state=space['lifecycle'], active_field=space['active_field'],
                          membership_revision=space['membership_revision'], pose_revision=space['pose_revision'])
            # Only public deployed members; hidden Hand/Deck identities never feed hints.
            fields['topology'] = self.query_verified(name)
            fields['topology']['dependency'].update(view=authority['view_id'])
            for identity in space['members']:
                if identity not in view['objects']:
                    continue
                card = self.s.state['cards'][identity]
                view['objects'][identity]['fields'].update(qmo=copy.deepcopy(self.corpus.fgs[card['catalog']]),
                    qmo_sha256=digest(self.corpus.fgs[card['catalog']]), pose=copy.deepcopy(self.state['poses'][identity]))
        visible_spaces=set(view['objects']) & set(self.state['spaces'])
        for identity,field in self.state['fields'].items():
            if field['active'] and field['space'] in visible_spaces:
                view['objects'][identity]={'identity':field['native_identity'],'semantic_id':identity,
                    'kind':'LOCAL_MANIFOLD_FIELD','owner':self.s.state['collections'][field['space']]['owner'],
                    'fields':{'qmo':field['qmo'],'native_color':field['native_color'],'space':field['space'],
                              'state':'RESOLVED','ordinary':field['ordinary'],'members':list(field['members'])}}
        for identity,emergent in self.state['emergents'].items():
            if all(s in visible_spaces for s in emergent['spaces']):
                view['objects'][identity]={'identity':self.s.b.resources[self.s.b.bindings[identity]]['payload']['identity'],
                                          'semantic_id':identity,'kind':'EMERGENT_FIELD',
                                          'owner':None,'fields':copy.deepcopy(emergent)}
        return view
