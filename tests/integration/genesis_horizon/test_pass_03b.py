"""Positive and adversarial live topology through the real Genesis/Hypervisor path."""
import copy
import json
import os
import subprocess
import sys
from pathlib import Path
import unittest
from collections import Counter
from concurrent.futures import ThreadPoolExecutor

from pass_03b_support import FieldFixture
from support import ROOT
from raeon_genesis_horizon.toolchain import compile_paths


class Pass03B(unittest.TestCase):
    def setUp(self):
        self.f=FieldFixture();self.h=self.f.horizon;self.ext=self.f.ext

    def tearDown(self):self.f.close()

    def refuse(self, request, player='player_1'):
        before=self.f.snapshot()
        with self.assertRaises(Exception):self.h.execute(request,self.f.players[player])
        self.assertEqual(self.f.snapshot(),before)

    def test_live_base_lock_identity_native_color_and_explicit_reopen(self):
        group=self.f.prepare(['M-R-01'])[0];space,mid,ids=group
        self.f.position(group,phi=0.73,translation=(4,-7))
        before=self.f.snapshot();query=self.ext.query(space)
        self.assertTrue(query['realizations'][0]['can_lock']);self.assertEqual(self.f.snapshot(),before)
        cards=copy.deepcopy(self.h._backend.application_values['cards'])
        request,frames=self.f.resolve(group)
        self.assertEqual(frames[0]['payload']['status'],'COMMITTED')
        active=self.ext.state['spaces'][space]['active_field'];field=self.ext.state['fields'][active]
        self.assertNotEqual(active,space);self.assertEqual(field['qmo'],self.ext.corpus.base[mid]['id'])
        self.assertEqual(field['native_color'],'RED');self.assertEqual(field['members'],ids)
        self.assertIn(active,self.h._backend.bindings)
        for i in ids:
            card=self.h._backend.application_values['cards'][i]
            for k in ('id','catalog','owner','location'):self.assertEqual(card[k],cards[i][k])
            self.assertEqual(card['history'][:-1],cards[i]['history'])
            self.assertEqual(self.ext.state['poses'][i]['value']['mapping_status'],'LOCKED')
        locked=self.f.snapshot();self.h.execute(request,self.f.players['player_1']);self.assertEqual(self.f.snapshot(),locked)
        self.refuse(self.f.request('SET_FG_POSES',self.f.poses(group)))
        self.f.perform('DRAW_ONE');extra=self.f.members('player_1_hand')[0]
        self.refuse(self.f.request('COMMIT_FG',{'cards':[extra],'destination':space}))
        self.f.perform('REOPEN_CONFIGURATION',self.f.space_args(space))
        self.assertFalse(self.ext.state['fields'][active]['active'])
        self.assertIsNone(self.ext.state['spaces'][space]['active_field'])
        self.assertEqual(self.f.members(space),ids)
        self.f.position(group,angle=180)
        self.refuse(self.f.request('RESOLVE_CONFIGURATION',self.f.space_args(space)))
        self.assertEqual(self.f.members('player_1_graveyard'),[])

    def test_shape_orientation_partial_feedback_and_magnetic_hysteresis(self):
        group=self.f.prepare(['M-R-01'])[0];space=group[0]
        for kind,kwargs,reason in [('shape',{'distort':lambda s,x,y:(x,y+2 if s['slot']=='S1' else y)},'SHAPE_CAPTURE_REQUIRED'),
                                   ('orientation',{'angle':90},'ORIENTATION_CAPTURE_REQUIRED')]:
            self.f.position(group,**kwargs);query=self.ext.query(space)
            self.assertEqual(query['reason'],reason,kind)
            self.refuse(self.f.request('RESOLVE_CONFIGURATION',self.f.space_args(space)))
            self.assertFalse(self.ext.state['fields'])
        self.f.position(group);self.assertEqual(self.ext.query(space)['realizations'][0]['stage'],'MAGNETIZED')
        self.f.position(group,distort=lambda s,x,y:(x,y+0.7 if s['slot']=='S1' else y))
        result=self.ext.query(space)['realizations'][0]
        self.assertEqual(result['shape_stage'],'MAGNETIZED');self.assertFalse(result['can_lock'])
        self.f.position(group,distort=lambda s,x,y:(x,y+0.8 if s['slot']=='S1' else y))
        self.assertEqual(self.ext.query(space)['realizations'][0]['shape_stage'],'FREE')

    def test_resolution_rollback_retry_and_postcommit_delivery(self):
        group=self.f.prepare(['M-R-02'])[0];self.f.position(group)
        request=self.f.request('RESOLVE_CONFIGURATION',self.f.space_args(group[0]))
        for point in ['after_lock_pose','after_field']:
            self.h.fault_hook=lambda p: (_ for _ in ()).throw(RuntimeError('fault')) if p==point else None
            try:self.refuse(request)
            finally:self.h.fault_hook=lambda _:None
        self.h.fault_hook=lambda p: (_ for _ in ()).throw(RuntimeError('delivery')) if p=='after_commit' else None
        try:
            with self.assertRaises(Exception):self.h.execute(request,self.f.players['player_1'])
        finally:self.h.fault_hook=lambda _:None
        state=self.f.snapshot();self.assertEqual(self.h.execute(request,self.f.players['player_1'])['status'],'COMMITTED')
        self.assertEqual(self.f.snapshot(),state);self.assertEqual(len(self.ext.state['fields']),1)

    def test_stale_pose_witness_and_concurrent_resolution(self):
        group=self.f.prepare(['M-R-01'])[0];self.f.position(group)
        old=self.ext.query(group[0])['dependency']
        stale=self.f.request('RESOLVE_CONFIGURATION',self.f.space_args(group[0]))
        self.f.position(group,angle=90);self.assertNotEqual(old,self.ext.query(group[0])['dependency'])
        self.refuse(stale)
        self.f.position(group)
        requests=[self.f.request('RESOLVE_CONFIGURATION',self.f.space_args(group[0])) for _ in range(2)]
        def attempt(r):
            try:return self.h.execute(r,self.f.players['player_1'])['status']
            except Exception:return 'REJECTED'
        with ThreadPoolExecutor(2) as pool:outcomes=list(pool.map(attempt,requests))
        self.assertEqual(sorted(outcomes),['COMMITTED','REJECTED'])
        self.assertEqual(len(self.ext.state['fields']),1)

    def test_positive_fusion_exact_union_frames_width_and_subsumed_provenance(self):
        groups=self.f.ready(['M-O-01','M-O-02']);a,b=[g[0] for g in groups]
        before=self.f.snapshot();preview=self.ext.preview_merge(a,b);self.assertEqual(self.f.snapshot(),before)
        self.assertEqual(preview['permission'],'VALID')
        ids=self.f.members(a)+self.f.members(b);poses=copy.deepcopy(self.ext.state['poses'])
        histories={i:copy.deepcopy(self.h._backend.application_values['cards'][i]['history']) for i in ids}
        width=len(self.f.members('player_1_configuration'))
        request,_=self.f.perform('MERGE_CONFIGURATION',self.f.merge_args(a,b))
        new=self.ext.state['spaces'][a]['subsumed_by'];space=self.ext.state['spaces'][new]
        self.assertEqual(len(self.f.members('player_1_configuration')),width-1)
        self.assertEqual(self.f.members(new),ids);self.assertEqual(space['sources'],[a,b])
        field=self.ext.state['fields'][space['active_field']]
        self.assertEqual(field['qmo'],self.ext.corpus.pair('M-O-01','M-O-02')['fusion_result_qmo'])
        self.assertEqual(field['native_color'],'VIOLET')
        for old in (a,b):
            self.assertEqual(self.ext.state['spaces'][old]['lifecycle'],'SUBSUMED')
            self.assertEqual(self.f.members(old),[])
        for i in ids:
            self.assertEqual(self.ext.state['poses'][i]['value'],poses[i]['value'])
            self.assertEqual(self.h._backend.application_values['cards'][i]['history'][:-1],histories[i])
        committed=self.f.snapshot();self.h.execute(request,self.f.players['player_1']);self.assertEqual(self.f.snapshot(),committed)
        self.refuse(self.f.request('REOPEN_CONFIGURATION',self.f.space_args(new)))
        self.refuse(self.f.request('SET_FG_POSES',dict(self.f.space_args(new),poses=self.f.poses(groups[0])['poses'])))
        self.f.restart();self.assertEqual(self.f.horizon._backend.collections.extension.state,self.ext.state)

    def test_fusion_rollback_source_negative_owner_and_no_recursive_split(self):
        groups=self.f.ready(['M-O-01','M-O-02']);a,b=[g[0] for g in groups]
        self.refuse(self.f.request('MERGE_CONFIGURATION',self.f.merge_args(a,a)))
        self.refuse(self.f.request('MERGE_CONFIGURATION',self.f.merge_args(a,b),player='player_2'),'player_2')
        request=self.f.request('MERGE_CONFIGURATION',self.f.merge_args(a,b))
        for point in ['after_merge_card','after_field','after_emergents']:
            self.h.fault_hook=lambda p: (_ for _ in ()).throw(RuntimeError('fault')) if p==point else None
            try:self.refuse(request)
            finally:self.h.fault_hook=lambda _:None
        self.h.execute(request,self.f.players['player_1'])
        new=self.ext.state['spaces'][a]['subsumed_by']
        self.refuse(self.f.request('MERGE_CONFIGURATION',self.f.merge_args(new,'player_1_config_C')))
        self.assertNotIn('SPLIT_CONFIGURATION',self.f.manifest['operations'])

    def test_invalid_source_fusion_preserves_distinct_duplicate_copies(self):
        groups=self.f.ready(['M-R-01','M-R-02']);a,b=[g[0] for g in groups]
        handles=[self.h._backend.application_values['cards'][i]['catalog'] for g in groups for i in g[2]]
        self.assertGreater(Counter(handles)['FG-044'],1)
        self.assertEqual(len(set(groups[0][2]+groups[1][2])),6)
        preview=self.ext.preview_merge(a,b)
        self.assertEqual(preview['permission'],self.ext.corpus.pair('M-R-01','M-R-02')['fusion_status'])
        self.assertNotEqual(preview['permission'],'VALID')
        self.refuse(self.f.request('MERGE_CONFIGURATION',self.f.merge_args(a,b)))
        self.assertEqual(len(self.ext.state['fields']),2)

    def test_passive_three_pair_emergents_selective_loss_and_nontargetability(self):
        groups=self.f.ready(['M-R-01','M-R-02','M-R-03'])
        self.assertEqual(len(self.ext.state['emergents']),3)
        self.assertEqual(len(self.f.members('player_1_configuration')),3)
        before=copy.deepcopy(self.ext.state['emergents'])
        for e in before.values():
            self.assertEqual(e['slot_cost'],0);self.assertFalse(e['directly_targetable'])
            pair=[self.ext.state['fields'][f]['manifold_id'] for f in e['supports']]
            self.assertEqual(e['qmo'],self.ext.corpus.pair(*pair)['emergent_qmo'])
            self.refuse(self.f.request('RETIRE_SUPPORT',{'cards':[e['id']]}))
        a=groups[0][0];field=self.ext.state['spaces'][a]['active_field']
        survivor={k:v for k,v in before.items() if field not in v['supports']}
        self.f.perform('REOPEN_CONFIGURATION',self.f.space_args(a))
        self.assertEqual(self.ext.state['emergents'],survivor)
        self.assertEqual(len(survivor),1)
        self.assertEqual(self.f.members(a),groups[0][2])
        self.f.position(groups[0]);self.f.resolve(groups[0])
        self.assertEqual(len(self.ext.state['emergents']),3)
        self.f.perform('RETIRE_SUPPORT',{'cards':groups[0][2]})
        self.assertEqual(self.ext.state['emergents'],survivor)

    def test_emergent_instances_no_qmo_alias_and_atomic_support_publication(self):
        groups=self.f.prepare(['M-R-01','M-R-01','M-R-03'])
        for group in groups[:2]:self.f.position(group);self.f.resolve(group)
        self.f.position(groups[2]);request=self.f.request('RESOLVE_CONFIGURATION',self.f.space_args(groups[2][0]))
        self.h.fault_hook=lambda p: (_ for _ in ()).throw(RuntimeError('fault')) if p=='after_emergents' else None
        try:self.refuse(request)
        finally:self.h.fault_hook=lambda _:None
        self.h.execute(request,self.f.players['player_1'])
        emergents=self.ext.state['emergents'];self.assertEqual(len(emergents),2)
        self.assertEqual(len({e['qmo'] for e in emergents.values()}),1)
        self.assertEqual(len({tuple(e['supports']) for e in emergents.values()}),2)
        before=self.f.snapshot();self.h.execute(request,self.f.players['player_1']);self.assertEqual(self.f.snapshot(),before)
        self.refuse(self.f.request('LINK_CONFIGURATION',self.f.merge_args(groups[0][0],groups[2][0])))

    def test_configuring_resolved_checkpoint_and_public_byte_reconnect(self):
        groups=self.f.prepare(['M-R-01','M-R-02'])
        self.f.position(groups[0],angle=20)
        snapshot=copy.deepcopy(self.ext.state)
        checkpoint=self.h.checkpoint(self.f.owner)
        self.h.restore(checkpoint,self.f.owner)
        self.ext=self.h._backend.collections.extension;self.f.ext=self.ext
        self.assertEqual(self.ext.state,snapshot)
        for group in groups:self.f.position(group);self.f.resolve(group)
        self.f.perform('DRAW_ONE');hidden=self.f.members('player_1_hand')+self.f.members('player_1_deck')
        self.f.perform('INSPECT_TOP',{'source':'player_1_deck','count':1})
        public=dict(self.f.players['player_1'],view_id='public')
        self.f.players['public']=public;self.f.handles['public']=self.f.bridge.bind_session(public)
        port=self.f.hello('public')
        for who in ('public','player_2'):
            view=self.h.observe(self.f.players[who])['view'];text=json.dumps(view)
            self.assertTrue(all(i not in text for i in hidden));self.assertNotIn('inspection',view)
            private=[e for e in view['relations'] if e['relation']=='private_to']
            if who=='public':self.assertEqual(private,[])
            else:self.assertTrue(all(e['target']==view['objects'][who]['identity'] for e in private))
            self.assertIn('EMERGENT_FIELD',text);self.assertIn('MAGNETIZED',text)
            for secret in ('segment_path','effect_source','native_road','grants'):self.assertNotIn(secret,text)
        saved=copy.deepcopy(self.ext.state);self.f.restart()
        self.assertEqual(self.f.horizon._backend.collections.extension.state,saved)
        self.f.connect();self.assertEqual(self.f.hello('public').view,port.view)

    def test_genesis_positive_predicates_transform_and_road_are_required(self):
        group=self.f.prepare(['M-R-01'])[0];self.f.position(group)
        request=self.f.request('RESOLVE_CONFIGURATION',self.f.space_args(group[0]))
        source=ROOT/'game/core/raeon/application/resolve_configuration.gen'
        key=source.relative_to(ROOT).as_posix();original=self.h._builds[key];target=self.f.path/'altered.gen'
        for old,new in [('"source_edges",',''),('  transform match with permission as candidate @{"operator":"COLLECTION_TRANSACTION"}',
                            '  en candidate : GEOMETRIC = instantiate fabric region mmo @bound_match')]:
            target.write_text(source.read_text().replace(old,new),encoding='utf8')
            self.h._builds[key]=compile_paths([target],ROOT,'altered')
            try:self.refuse(request)
            finally:self.h._builds[key]=original
        run=self.h._backend.collections.run_unit
        def no_road(name):
            if name=='transport':return None
            return run(name)
        self.h._backend.collections.run_unit=no_road
        try:self.refuse(request)
        finally:self.h._backend.collections.run_unit=run
        self.h.execute(request,self.f.players['player_1'])
        self.assertEqual(len(self.ext.state['fields']),1)

    def test_dynamic_nine_spaces_and_fusion_preserve_region_identity(self):
        groups=self.f.ready(['M-O-01','M-O-02'])
        before=self.h._view(self.f.players['player_1'])['objects']['player_1_configuration']['identity']
        for rank in ['Red','Orange','Yellow','Green','Blue','Violet']:
            self.f.perform('ADD_CONFIGURATION_SPACE',{'rank':rank},effect={'variant':rank})
        self.assertEqual(len(self.f.members('player_1_configuration')),9)
        self.refuse(self.f.request('ADD_CONFIGURATION_SPACE',{'rank':'Red'},effect={'variant':'Red'}))
        for view in ['player_1','player_2']:
            visible=self.h._view(self.f.players[view])['objects']
            self.assertTrue(all(s in visible for s in self.f.members('player_1_configuration')))
        self.f.perform('MERGE_CONFIGURATION',self.f.merge_args(groups[0][0],groups[1][0]))
        self.assertEqual(len(self.f.members('player_1_configuration')),8)
        self.f.perform('ADD_CONFIGURATION_SPACE',{'rank':'Red'},effect={'variant':'Red'})
        self.assertEqual(len(self.f.members('player_1_configuration')),9)
        self.assertEqual(self.h._view(self.f.players['player_1'])['objects']['player_1_configuration']['identity'],before)

    def test_deterministic_replay_different_paths(self):
        def history(f):
            groups=f.ready(['M-O-01','M-O-02'])
            f.perform('MERGE_CONFIGURATION',f.merge_args(groups[0][0],groups[1][0]))
            return f.horizon._state['root'],copy.deepcopy(f.ext.state)
        a=history(self.f)
        other=FieldFixture()
        try:self.assertEqual(history(other),a)
        finally:other.close()


def execute_field(mid):
    """One native runtime lifetime per cold witness execution."""
    f=FieldFixture('positive-'+mid)
    check=unittest.TestCase()
    try:
        row=f.ext.corpus.base[mid]
        group=f.ready([mid])[0]
        space=f.ext.state['spaces'][group[0]];field=f.ext.state['fields'][space['active_field']]
        check.assertEqual(space['lifecycle'],'RESOLVED')
        check.assertEqual(field['qmo'],row['id']);check.assertEqual(field['native_color'],row['native_color'])
        check.assertEqual(len(field['proof']['edges']),row['generator_count'])
        check.assertTrue(all(e['live'] for e in field['proof']['edges']))
        return {'manifold':mid,'qmo':field['qmo'],'color':field['native_color'],
                'field':field['id'],'root':f.horizon._state['root'],'status':'PASS'}
    finally:f.close()


class AllBaseFields(unittest.TestCase):
    def test_all_60_source_witnesses_resolve_through_actual_package(self):
        base=json.loads((ROOT/'data/qmo/manifolds/objects.json').read_text())
        results=[]
        for row in base:
            with self.subTest(manifold=row['manifold_id']):
                child=subprocess.run([sys.executable,'-B',str(Path(__file__).resolve()),'--field',row['manifold_id']],
                    cwd=ROOT,env=dict(os.environ,PYTHONFAULTHANDLER='1',PYTHONDONTWRITEBYTECODE='1'),
                    capture_output=True,text=True,encoding='utf8')
                self.assertEqual(child.returncode,0,child.stdout+child.stderr)
                result=json.loads(child.stdout)
                self.assertEqual(result['manifold'],row['manifold_id'])
                self.assertEqual(result['status'],'PASS')
                results.append(result)
                print('positive native field '+row['manifold_id']+': PASS',file=sys.stderr,flush=True)
        self.assertEqual(len(results),60)
        target=ROOT/'build/genesis_runtime/evidence/pass-03b-all-base-fields.json'
        target.parent.mkdir(parents=True,exist_ok=True)
        target.write_text(json.dumps({'status':'PASS','run':60,'process_isolation':True,'cases':results},indent=2)+'\n',encoding='utf8')


if __name__=='__main__':
    if len(sys.argv)==3 and sys.argv[1]=='--field':
        print(json.dumps(execute_field(sys.argv[2])))
    else:unittest.main()
