"""Actual byte/runtime topology tests. Gated field positives are NOT counted here."""
import copy
import json
import sqlite3
import shutil
import unittest
from collections import Counter
from concurrent.futures import ThreadPoolExecutor

from pass_02_support import CardFixture
from support import ROOT, Port, port_decode
from raeon_genesis_horizon.toolchain import digest, compile_paths


class Pass03(unittest.TestCase):
    def setUp(self):
        self.f = CardFixture()
        self.h = self.f.horizon
        self.ext = self.h._backend.collections.extension

    def tearDown(self):
        self.f.close()

    def deploy(self, handles=('FG-001', 'FG-044', 'FG-117'), space='player_1_config_A'):
        roster = list(handles)
        for i in range(1, 121):
            name = f'FG-{i:03}'
            while roster.count(name) < 2 and len(roster) < 60:
                roster.append(name)
        self.f.initialize(roster)
        cards = []
        for _ in handles:
            self.f.perform('DRAW_ONE')
            card = self.f.members('player_1_hand')[0]
            self.f.perform('COMMIT_FG', {'cards': [card], 'destination': space})
            cards.append(card)
        return cards

    def args(self, cards, space='player_1_config_A'):
        return {'space': space, 'membership_revision': self.ext.state['spaces'][space]['membership_revision'],
            'poses': [{'card': c, 'x': 1000*i, 'y': -50, 'qw': 1, 'qx': 2, 'qy': 3, 'qz': 4,
                      'pose_revision': self.ext.state['poses'][c]['revision']} for i, c in enumerate(cards)]}

    def refuse(self, request, player='player_1'):
        before = copy.deepcopy(self.h._record()), copy.deepcopy(self.h._state)
        with self.assertRaises(Exception):
            self.h.execute(request, self.f.players[player])
        self.assertEqual((self.h._record(), self.h._state), before)

    def test_corpus_full_sqlite_and_json_agree(self):
        c = self.ext.corpus
        self.assertEqual([len(c.fgs), len(c.base), len(c.qmos), len(c.pairs), len(c.compatibility)], [120,60,2094,1770,2482])
        self.assertEqual(Counter(r['native_color'] for r in c.base.values()),
                         dict(RED=15, ORANGE=13, YELLOW=11, GREEN=9, BLUE=7, VIOLET=5))
        with sqlite3.connect((ROOT / 'data/qmo/cycle1/qmo.sqlite').as_uri()+'?mode=ro', uri=True) as db:
            for address, raw in db.execute('select address,definition_json from qmos'):
                row = json.loads(raw)
                if address in c.qmos:
                    self.assertEqual(row, c.qmos[address])
                elif row.get('card_id') in c.fgs:
                    self.assertEqual(row, c.fgs[row['card_id']])
            self.assertEqual(db.execute('select count(*) from derived_qmos').fetchone()[0], 2034)
            for a,b,f,e in db.execute('select a_manifold,b_manifold,fusion_status,emergent_status from manifold_pair_relations'):
                row = c.pairs[tuple(sorted((a,b)))]
                self.assertEqual((f,e), (row['fusion_status'], row['emergent_status']))
        self.assertEqual(len(c.data['atlas']['base']) + len(c.data['atlas']['fusion']) + len(c.data['atlas']['emergent']), 2094)

    def test_pair_lookup_preserves_all_outcomes_and_addresses(self):
        c = self.ext.corpus
        self.assertEqual(c.lookup('M-R-01'), c.lookup('@qmo/raeon/cycle1/manifold/m-r-01'))
        self.assertEqual(c.lookup('M-R-01')['generators'], ['FG-001','FG-044','FG-117'])
        pair = c.pair('M-O-01','M-O-02')
        self.assertEqual(pair, c.pair('M-O-02','M-O-01'))
        self.assertEqual(pair['fusion_result_qmo'], '@qmo/raeon/derived/fusion/m-o-01+m-o-02')
        self.assertEqual(c.lookup(pair['fusion_result_qmo'])['native_color'], 'VIOLET')
        self.assertEqual(Counter(r['fusion_status'] for r in c.pairs.values()), dict(VALID=343, TERMINATES=825, NOT_APPLICABLE=602))
        self.assertEqual(Counter(r['emergent_status'] for r in c.pairs.values()), dict(VALID=1691, TERMINATES=79))
        self.assertEqual(c.pair('absent','M-O-01')['status'], 'OPEN')
        self.assertEqual(c.lookup('absent')['status'], 'OPEN')
        self.assertTrue(all(not r['directly_targetable'] and r['support_persists'] for r in c.data['emergent']))

    def test_native_hydration_duplicate_copies_and_source_bytes(self):
        ids = self.deploy(('FG-001','FG-001'))
        self.assertNotEqual(*ids)
        view = self.h._view(self.f.players['player_1'])
        self.assertEqual(view['objects'][ids[0]]['fields']['qmo'], self.ext.corpus.lookup('FG-001'))
        for identity in ids:
            card = self.h._backend.application_values['cards'][identity]
            definition = self.h._backend.application_definitions[card['binding']]
            self.assertEqual(definition['qmo_source']['occupancy'], ['C','D','E','H'])
            self.assertEqual(definition['data']['arrays']['chirality_field_3p1p1'][::4], [0,0,1,1,1,0,0,1])
            resource = self.h._backend.resources[self.h._backend.bindings[card['binding']]]
            self.assertEqual(len(self.h._backend.read_cells(resource)), 40)
        self.f.initialize(player='player_2')
        self.f.perform('DRAW_ONE',player='player_2')
        other = self.f.members('player_2_hand')[0]
        self.f.perform('COMMIT_FG',{'cards':[other],'destination':'player_2_config_A'},player='player_2')
        self.assertNotIn(other,ids)
        view = self.h._view(self.f.players['player_2'])
        self.assertEqual(view['objects'][other]['fields']['qmo'],view['objects'][ids[0]]['fields']['qmo'])
        self.ext.corpus.verify()

    def test_pose_bytes_full_3d_canonical_equivalence_and_identity(self):
        ids = self.deploy(('FG-001',))
        before = copy.deepcopy(self.h._backend.application_values['cards'][ids[0]])
        request, frames = self.f.perform('SET_FG_POSES', self.args(ids))
        self.assertEqual(frames[0]['payload']['status'], 'COMMITTED')
        record = self.ext.state['poses'][ids[0]]
        self.assertEqual(record['value']['quaternion_wxyz'], [1,2,3,4])
        args = self.args(ids)
        args['poses'][0].update(qw=-2,qx=-4,qy=-6,qz=-8)
        self.f.perform('SET_FG_POSES', args)
        self.assertEqual(record['value']['quaternion_wxyz'], [1,2,3,4])
        after = self.h._backend.application_values['cards'][ids[0]]
        self.assertEqual(after['id'], before['id'])
        self.assertEqual(after['location'], before['location'])
        self.assertEqual(after['history'][:len(before['history'])], before['history'])
        self.assertEqual(record['revision'], 2)
        self.assertEqual(self.ext.corpus.fgs['FG-001']['chirality_parity'], 1)

    def test_numeric_bounds_zero_rotation_and_no_z_or_reflection_input(self):
        ids = self.deploy(('FG-001',))
        for key,value in [('x',True),('x',1.2),('x',2**60),('qy',1000001),('z',1),('reflection',True)]:
            args = self.args(ids);args['poses'][0][key] = value
            with self.assertRaises(ValueError):
                self.f.request('SET_FG_POSES', args)
        args = self.args(ids);args['poses'][0].update(qw=0,qx=0,qy=0,qz=0)
        self.refuse(self.f.request('SET_FG_POSES',args))

    def test_owner_membership_stale_and_no_individual_extraction(self):
        ids = self.deploy(('FG-001',))
        self.refuse(self.f.request('SET_FG_POSES', self.args(ids), player='player_2'), 'player_2')
        args = self.args(ids);args['membership_revision'] -= 1
        self.refuse(self.f.request('SET_FG_POSES', args))
        args = self.args(ids);args['poses'][0]['pose_revision'] += 1
        self.refuse(self.f.request('SET_FG_POSES', args))
        self.refuse(self.f.request('SET_FG_POSES',self.args(ids, 'player_1_config_B')))
        self.refuse(self.f.request('COMMIT_FG', {'cards':ids, 'destination':'player_1_config_B'}))

    def test_batch_atomic_rollback_retry_and_post_commit_delivery(self):
        ids = self.deploy(('FG-001','FG-002'))
        malformed = self.args(ids)
        malformed['poses'][1]['card'] = 'not-deployed'
        self.refuse(self.f.request('SET_FG_POSES',malformed))
        request = self.f.request('SET_FG_POSES',self.args(ids))
        before = copy.deepcopy(self.h._record()), copy.deepcopy(self.h._state)
        self.h.fault_hook = lambda point: (_ for _ in ()).throw(RuntimeError('injected')) if point == 'after_pose' else None
        try:
            self.refuse(request)
        finally:
            self.h.fault_hook = lambda _: None
        self.assertEqual((self.h._record(),self.h._state), before)
        self.h.execute(request, self.f.players['player_1'])
        committed = copy.deepcopy(self.h._record()), copy.deepcopy(self.h._state)
        self.h.execute(request, self.f.players['player_1'])
        self.assertEqual((self.h._record(),self.h._state), committed)
        request = self.f.request('SET_FG_POSES',self.args(ids))
        self.h.fault_hook = lambda point: (_ for _ in ()).throw(RuntimeError('injected')) if point == 'after_commit' else None
        try:
            with self.assertRaises(Exception):self.h.execute(request,self.f.players['player_1'])
        finally:self.h.fault_hook = lambda _: None
        self.assertEqual(self.h.execute(request,self.f.players['player_1'])['status'],'COMMITTED')
        self.assertTrue(all(self.ext.state['poses'][i]['revision']==2 for i in ids))

    def test_catalog_not_live_closure_and_read_only_exhaustive_query(self):
        ids = self.deploy()
        before = copy.deepcopy(self.h._record()), copy.deepcopy(self.h._state)
        result = self.ext.query('player_1_config_A')
        self.assertEqual(result['membership'],'MATCH')
        self.assertIn('M-R-01',[r['manifold_id'] for r in result['candidates']])
        self.assertEqual(result['pose_closure'],'UNRESOLVED')
        self.assertIsNone(result['witness'])
        self.assertEqual(len(result['partial_relationships']['edges']),3)
        self.assertEqual(result['partial_relationships']['authoritative_live_edges'],[])
        self.assertEqual((self.h._record(),self.h._state),before)
        for row in self.ext.corpus.base.values():
            query = self.ext.corpus.candidates(row['generators'])
            oracle = sorted(r['id'] for r in self.ext.corpus.data['base'] if Counter(r['generators']) == Counter(row['generators']))
            self.assertEqual(sorted(r['id'] for r in query['candidates']), oracle)
        self.refuse(self.f.request('RESOLVE_CONFIGURATION',{'space':'player_1_config_A','membership_revision':3}))
        self.assertEqual(self.ext.state['fields'],{})

    def test_small_population_duplicates_wrong_family_and_budget(self):
        c = self.ext.corpus
        for handles in [['FG-001'],['FG-001','FG-044'],['FG-001','FG-001','FG-044','FG-117'],['FG-001','FG-002','FG-003']]:
            self.assertEqual(c.candidates(handles)['candidates'],[])
        partial = c.candidates(['FG-001','FG-044','FG-117'],0)
        self.assertFalse(partial['complete_search'])
        self.assertEqual(partial['membership'],'UNRESOLVED')
        self.assertEqual(partial['pose_closure'],'BUDGET_EXHAUSTED')
        with self.assertRaises(ValueError):c.candidates([],61)

    def test_reopen_merge_preview_and_gated_mutations_preserve_copies(self):
        ids = self.deploy()
        before = copy.deepcopy(self.h._record()), copy.deepcopy(self.h._state)
        preview = self.ext.preview_merge('player_1_config_A','player_1_config_B')
        self.assertEqual(preview['members'], ids)
        self.assertIsNone(preview['result_capacity'])
        self.assertEqual((self.h._record(),self.h._state), before)
        args = dict(space='player_1_config_A',membership_revision=3,other='player_1_config_B',other_membership_revision=0)
        for operation in ['MERGE_CONFIGURATION','LINK_CONFIGURATION']:
            self.refuse(self.f.request(operation,args))
        self.f.perform('REOPEN_CONFIGURATION',dict(space='player_1_config_A',membership_revision=3))
        self.assertEqual(self.f.members('player_1_config_A'),ids)
        self.assertEqual(self.f.members('player_1_graveyard'),[])
        self.assertEqual(self.ext.state['spaces']['player_1_config_A']['lifecycle'],'CONFIGURING')

    def test_public_view_only_exposes_deployed_source_and_no_inventory_hints(self):
        ids = self.deploy(('FG-001',))
        self.f.perform('DRAW_ONE')
        hidden = self.f.members('player_1_hand') + self.f.members('player_1_deck')
        self.f.perform('INSPECT_TOP',dict(source='player_1_deck',count=1))
        public = dict(self.f.players['player_1'], view_id='public')
        before = self.h._state['root']
        view = self.h.observe(public)['view']
        text = json.dumps(view)
        self.assertTrue(all(i not in text for i in hidden))
        self.assertNotIn('inspection',view)
        self.assertIn(ids[0],view['objects'])
        self.assertNotIn('private_to',[r['relation'] for r in view['relations']])
        for secret in ['segment_path','grants','seed','native_road','effect_source']:
            self.assertNotIn(secret,text)
        self.assertEqual(self.h._state['root'],before)

    def test_concurrent_stale_pose_and_nonempty_checkpoint(self):
        ids = self.deploy(('FG-001',))
        requests = [self.f.request('SET_FG_POSES',self.args(ids)) for _ in range(2)]
        def attempt(request):
            try:return self.h.execute(request,self.f.players['player_1'])['status']
            except Exception:return 'REJECTED'
        with ThreadPoolExecutor(2) as pool:
            results = list(pool.map(attempt,requests))
        self.assertEqual(sorted(results),['COMMITTED','REJECTED'])
        saved = copy.deepcopy(self.ext.state)
        self.f.restart()
        self.assertEqual(self.f.horizon._backend.collections.extension.state,saved)

    def test_handler_predicate_omission_and_road_closure_matter(self):
        ids = self.deploy(('FG-001',))
        request = self.f.request('SET_FG_POSES', self.args(ids))
        source = ROOT / 'game/core/raeon/application/set_fg_poses.gen'
        target = self.f.path / 'altered.gen'
        original = self.h._builds[source.relative_to(ROOT).as_posix()]
        for old,new in [('"proper_rotation",',''),('  transform match with permission as candidate @{"operator":"COLLECTION_TRANSACTION"}', '  en candidate : GEOMETRIC = instantiate fabric region mmo @bound_match')]:
            target.write_text(source.read_text().replace(old,new),encoding='utf8')
            self.h._builds[source.relative_to(ROOT).as_posix()] = compile_paths([target],ROOT,'altered')
            try:self.refuse(request)
            finally:self.h._builds[source.relative_to(ROOT).as_posix()] = original
        transport = ROOT/'game/core/raeon/application/native_transport.gen'
        key = transport.relative_to(ROOT).as_posix();original = self.h._builds[key]
        target.write_text(transport.read_text().replace('  road close road1 successor as closed\n','').replace('  export closed : RECEIPT<ROAD_CLOSE>\n',''),encoding='utf8')
        with self.assertRaisesRegex(Exception, 'ROAD_UNCLOSED'):
            compile_paths([target],ROOT,'altered')

    def test_source_integrity_missing_corpus_and_exact_render_integer(self):
        root = self.f.path / 'corpus'
        lock = self.ext.corpus.lock
        for relative in ['game/qmo/cycle1.lock.json', *[v['path'] for v in lock['datasets'].values()]]:
            target = root / relative
            target.parent.mkdir(parents=True,exist_ok=True)
            shutil.copyfile(ROOT / relative,target)
        corpus = type(self.ext.corpus)(root)
        path = root / lock['datasets']['field_generators']['path']
        path.write_bytes(path.read_bytes()+b' ')
        with self.assertRaisesRegex(ValueError,'QMO_CORPUS_INTEGRITY'):corpus.verify()
        path.unlink()
        with self.assertRaises(FileNotFoundError):type(corpus)(root)
        seed = json.loads((ROOT/'data/render_specs/cycle_01/M-R-01.json').read_text())['deterministic_seed']
        self.assertEqual(seed,5720288704652931231)
        self.assertEqual(json.loads(json.dumps({'seed':seed}))['seed'],seed)

    def test_source_extension_and_checkpoint_abi_tamper_rejected(self):
        ids = self.deploy(('FG-001',))
        checkpoint = self.h.checkpoint(self.f.owner)
        contract = self.h._backend.collections.manifest['state_extension']
        old = contract['modules']['state']['sha256']
        contract['modules']['state']['sha256'] = '0'*64
        try:
            with self.assertRaisesRegex(Exception,'AUTHORITY_DENIED'):self.h._view(self.f.players['player_1'])
        finally:contract['modules']['state']['sha256'] = old
        original = self.h._binding_contract
        self.h._binding_contract = lambda *args: '0'*64
        try:
            with self.assertRaises(Exception):self.h.restore(checkpoint,self.f.owner)
        finally:self.h._binding_contract = original
        self.assertEqual(self.f.members('player_1_config_A'),ids)

    def test_public_byte_delta_and_reconnect_with_topology(self):
        ids = self.deploy(('FG-001',))
        self.f.perform('DRAW_ONE')
        hidden = self.f.members('player_1_hand')[0]
        public = dict(self.f.players['player_1'],view_id='public')
        self.f.players['public'] = public
        self.f.handles['public'] = self.f.bridge.bind_session(public)
        port = self.f.hello('public')
        self.f.perform('SET_FG_POSES',self.args(ids))
        frames = self.f.send('public','SYNC_REQUEST',{'view_id':port.view_id,'revision':port.revision})
        for frame in frames:port.accept(frame)
        self.assertEqual(port.view['objects'][ids[0]]['fields']['pose']['revision'],1)
        self.assertNotIn(hidden,json.dumps(port.view))
        self.f.connect()
        restored = self.f.hello('public')
        self.assertEqual(restored.view,port.view)

    def test_retired_recovered_copy_does_not_keep_prior_space_pose(self):
        ids = self.deploy(('FG-001',))
        self.f.perform('SET_FG_POSES',self.args(ids))
        stamp = copy.deepcopy(self.ext.query('player_1_config_A')['dependency'])
        self.f.perform('RETIRE_SUPPORT',{'cards':ids})
        self.assertIsNone(self.ext.state['poses'][ids[0]]['value'])
        self.f.perform('RECOVER_1',{'cards':ids})
        self.f.perform('COMMIT_FG',{'cards':ids,'destination':'player_1_config_B'})
        self.assertIsNone(self.ext.state['poses'][ids[0]]['value'])
        self.assertEqual(self.ext.state['poses'][ids[0]]['revision'],2)
        self.assertNotEqual(self.ext.query('player_1_config_A')['dependency'],stamp)
        self.assertEqual(self.f.members('player_1_config_B'),ids)



if __name__ == '__main__':
    unittest.main()
