"""Independent negative integration and seeded conservation exercises."""
import copy
import json
import random
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

from pass_02_support import CardFixture
from support import ROOT, port_decode
from raeon_genesis_horizon.toolchain import canonical, compile_paths, digest, file_hash
from raeon_genesis_horizon.adapter import HorizonError


class Adversarial(unittest.TestCase):
    def setUp(self):
        self.f = CardFixture()
        self.h = self.f.horizon

    def tearDown(self):
        self.f.close()

    def refuse(self, request, player='player_1'):
        state, native = copy.deepcopy(self.h._state), copy.deepcopy(self.h._record())
        with self.assertRaises(Exception):
            self.h.execute(request, self.f.players[player])
        self.assertEqual(self.h._state, state)
        self.assertEqual(self.h._record(), native)

    def test_input_bounds_code_and_card_only_containment(self):
        self.f.initialize()
        for count in [True, -1, 8, 2**100, '1']:
            with self.assertRaises(ValueError):
                self.f.request('INSPECT_TOP', {'source': 'player_1_deck', 'count': count})
        request = self.f.request('DRAW_ONE')
        for name, value in [('seed', 'untrusted'), ('destination', 'player_2_hand'), ('source', 'player_2_deck')]:
            bad = copy.deepcopy(request)
            bad['arguments'][name] = value
            self.refuse(bad)
        bad = self.f.request('INITIALIZE_INVENTORY', {'roster': self.f.neutral()})
        bad['arguments']['roster'] = ['FG-001'] * 61
        self.refuse(bad)
        for value in ['player_1_board', 'player_1_config_A', '"}; write_overlay fabric 0 1']:
            self.refuse(self.f.request('COMMIT_FG', {'cards': [value], 'destination': 'player_1_config_A'}))
        self.assertEqual(len(self.h._backend.application_values['cards']), 60)

    def test_setup_rollback_and_exact_idempotent_multiset(self):
        request = self.f.request('INITIALIZE_INVENTORY', {'roster': self.f.neutral()})
        self.h.fault_hook = lambda point: (_ for _ in ()).throw(RuntimeError('candidate')) if point == 'after_candidate' else None
        self.refuse(request)
        self.assertEqual(self.h._backend.application_values['cards'], {})
        self.assertEqual(self.h._backend.application_values['serial'], 0)
        self.h.fault_hook = lambda _: None
        result = self.h.execute(request, self.f.players['player_1'])
        state = copy.deepcopy(self.h._record())
        self.assertEqual(self.h.execute(request, self.f.players['player_1']), result)
        self.assertEqual(self.h._record(), state)
        cards = self.h._backend.application_values['cards']
        self.assertEqual([cards[i]['catalog'] for i in self.f.members('player_1_deck')], self.f.neutral())
        self.f.initialize(player='player_2')
        same = [c for c in cards.values() if c['catalog'] == 'FG-001']
        # After publication the old local reference remains detached; inspect live state.
        same = [c for c in self.h._backend.application_values['cards'].values() if c['catalog'] == 'FG-001']
        self.assertEqual(len(same), 4)
        self.assertEqual(len({c['id'] for c in same}), 4)
        self.assertEqual({c['owner'] for c in same}, {'player_1', 'player_2'})

    def test_concurrent_requests_and_semantic_order(self):
        self.f.initialize()
        a, b = self.f.request('DRAW_ONE'), self.f.request('DRAW_ONE')
        def attempt(request):
            try:
                return self.h.execute(request, self.f.players['player_1'])['status']
            except HorizonError as error:
                return error.code
        with ThreadPoolExecutor(max_workers=2) as pool:
            results = list(pool.map(attempt, [a, b]))
        self.assertEqual(sorted(results), ['COMMITTED', 'STALE_PRECONDITION'])
        self.assertEqual(len(self.f.members('player_1_hand')), 1)
        root = self.h._semantic_root(self.h._state)
        values = self.h._backend.application_values
        values['collections']['player_1_deck']['members'].reverse()
        self.assertNotEqual(self.h._semantic_root(self.h._state), root)
        values['collections']['player_1_deck']['members'].reverse()
        self.assertEqual(self.h._semantic_root(self.h._state), root)

    def test_native_route_and_handler_closure_cannot_be_bypassed(self):
        self.f.initialize()
        request = self.f.request('DRAW_ONE')
        original = self.h._run
        for suffix in ['draw_one.gen', 'native_transport.gen']:
            def omit(relative, budget, expected=suffix):
                if relative.endswith(expected):
                    return {'resource_id': 'omitted'}
                return original(relative, budget)
            self.h._run = omit
            self.refuse(request)
            self.h._run = original
        backend = self.h._backend
        close = backend.road_close
        def unclosed(road, geo):
            if backend.collections.unit:
                raise ValueError('CLOSURE_FAILED')
            return close(road, geo)
        backend.road_close = unclosed
        self.refuse(request)
        backend.road_close = close
        definition = self.h._state['application']['manifest']['operations']['DRAW_ONE']
        effects = definition['effects']
        definition['effects'] = []
        self.refuse(request)
        definition['effects'] = effects
        self.h.execute(request, self.f.players['player_1'])
        native = backend.resources[backend.bindings[backend.application_values['cards'][self.f.members('player_1_hand')[0]]['binding']]]
        self.assertEqual(native['payload']['native_road']['status'], 'CLOSED')

    def test_recovery_profiles_and_batch_capacity(self):
        catalog = self.h._backend.collections.catalog['records']
        utility = next(k for k, r in catalog.items() if r['category'] == 'Utility')
        roster = self.f.neutral()
        roster[0] = utility
        self.f.initialize(roster)
        for _ in range(7):
            self.f.perform('DRAW_ONE')
        cards = self.f.members('player_1_hand')
        self.f.perform('RETIRE_CARDS', {'cards': cards[:4]})
        self.refuse(self.f.request('RECOVER_1', {'cards': cards[:1]}))
        self.f.perform('RECOVER_4', {'cards': cards[:1]})
        self.f.perform('RECOVER_3', {'cards': cards[1:4]})
        self.f.perform('RETIRE_CARDS', {'cards': cards[1:4]})
        self.f.perform('RECOVER_2', {'cards': cards[1:3]})
        self.f.perform('RECOVER_5', {'cards': cards[3:4]})
        self.f.perform('RETIRE_CARDS', {'cards': cards[1:4]})
        self.f.perform('DRAW_ONE')
        self.refuse(self.f.request('RECOVER_3', {'cards': cards[1:4]}))
        self.assertEqual(len(self.f.members('player_1_graveyard')), 3)
        self.refuse(self.f.request('COMMIT_FG', {'cards': [cards[0]], 'destination': 'player_1_config_A'}))
        self.refuse(self.f.request('COMMIT_FG', {'cards': [cards[4]], 'destination': 'player_2_config_A'}))

    def test_inspection_reorder_batch_helpers_grant_limits(self):
        self.f.initialize()
        self.refuse(self.f.request('INSPECT_TOP', {'source': 'player_2_deck', 'count': 1}))
        request, _ = self.f.perform('INSPECT_TOP', {'source': 'player_1_deck', 'count': 3})
        visible = self.h._view(self.f.players['player_1'])['inspection']
        ids = [x['identity'] for x in visible]
        self.assertEqual(ids, self.f.members('player_1_deck')[:3])
        reused = copy.deepcopy(request)
        reused['request_id'] += '-again'
        reused['expected_revision'] = self.h._state['revision']
        self.refuse(reused)
        self.f.perform('REORDER_TOP', {'cards': list(reversed(ids))})
        self.assertEqual(self.f.members('player_1_deck')[:3], list(reversed(ids)))
        self.assertNotIn('inspection', self.h._view(self.f.players['player_1']))
        self.f.perform('BATCH_TO_HAND', {'cards': ids[:2]})
        self.assertEqual(self.f.members('player_1_hand'), ids[:2])
        with self.assertRaisesRegex(HorizonError, 'AUTHORITY_DENIED'):
            self.h.install_conformance_grant(object(), {}, {}, 'client-grant')

    def test_seeded_conservation_two_owners(self):
        self.f.initialize()
        self.f.initialize(player='player_2')
        expected = set(self.h._backend.application_values['cards'])
        rng = random.Random(29092026)
        for _ in range(24):
            owner = rng.choice(['player_1', 'player_2'])
            hand, grave = self.f.members(owner + '_hand'), self.f.members(owner + '_graveyard')
            choice = rng.randrange(3)
            if choice == 0 and len(hand) < 7:
                self.f.perform('DRAW_ONE', player=owner)
            elif choice == 1 and hand:
                self.f.perform('RETIRE_CARDS', {'cards': [rng.choice(hand)]}, owner)
            elif grave and len(hand) < 7:
                self.f.perform('RECOVER_1', {'cards': [rng.choice(grave)]}, owner)
            values = self.h._backend.application_values
            all_members = [i for c in values['collections'].values() for i in c['members'] if i in values['cards']]
            self.assertEqual(set(all_members), expected)
            self.assertEqual(len(all_members), 120)
            self.h._backend.collections.validate()

    def test_catalog_tamper_and_physical_path_determinism(self):
        service = self.h._backend.collections
        original = service.catalog['sources'].copy()
        first = next(iter(original))
        service.catalog['sources'][first] = '0' * 64
        with self.assertRaises(ValueError):
            service.verify_catalog()
        service.catalog['sources'] = original
        records = service.catalog['records']
        self.assertTrue(any(r['source_status'] == 'PROVISIONAL' for r in records.values()))
        self.assertTrue(all(r['printed_id'] == 'OPEN' for r in records.values() if r['category'] != 'Field Generator'))
        sources = list((ROOT / 'game/core/raeon/application').glob('*.gen'))
        with tempfile.TemporaryDirectory(prefix='different physical path ', dir=ROOT / 'build') as directory:
            other = Path(directory)
            for source in sources:
                target = other / source.relative_to(ROOT)
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(source.read_bytes())
                self.assertEqual(compile_paths([source], ROOT, source.stem).link.bytecode,
                                 compile_paths([target], other, source.stem).link.bytecode)

    def test_checkpoint_corruption_and_new_process_restore(self):
        self.f.initialize()
        request, _ = self.f.perform('DRAW_ONE')
        checkpoint = self.h.checkpoint(self.f.owner)
        storage = self.h.storage
        root = self.h._state['root']
        script = '''import json,sys
from pathlib import Path
sys.path.insert(0,str(Path(sys.argv[1])/'game/core/genesis_horizon/bindings/python/src'))
from raeon_genesis_horizon.adapter import Horizon
h=Horizon(sys.argv[2],root=sys.argv[1]); cp=json.loads(sys.argv[3]); a=json.loads(sys.argv[4])
h.restore(cp,{'restore':True}); assert h._state['root']==sys.argv[5]
before=h._state['revision'];h.execute(json.loads(sys.argv[6]),a);assert h._state['revision']==before
print(json.dumps({'root':h._state['root'],'epoch':h.epoch,'cards':len(h._backend.application_values['cards'])}));h.close()
'''
        result = subprocess.run([sys.executable, '-B', '-c', script, str(ROOT), str(storage), json.dumps(checkpoint),
                                 json.dumps(self.f.players['player_1']), root, json.dumps(request)], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        recovered = json.loads(result.stdout)
        self.assertEqual(recovered['cards'], 60)
        self.assertNotEqual(recovered['epoch'], self.h.epoch)
        source = storage / 'checkpoints' / checkpoint['name'] / 'root.json'
        saved = source.read_bytes()
        source.write_bytes(saved + b' ')
        with self.assertRaises(HorizonError):
            self.h.restore(checkpoint, self.f.owner)
        self.assertEqual(self.h._state['root'], root)
        source.write_bytes(saved)
        old_contract = self.h._binding_contract
        self.h._binding_contract = lambda: 'incompatible-binding'
        with self.assertRaises(HorizonError):
            self.h.restore(checkpoint, self.f.owner)
        self.assertEqual(self.h._state['root'], root)
        self.h._binding_contract = old_contract

    def test_semantic_replay_across_storage_and_epoch(self):
        other = CardFixture()
        self.addCleanup(other.close)
        for fixture in [self.f, other]:
            fixture.initialize()
            fixture.perform('SHUFFLE_DECK', effect={'seed': 'deterministic-replay-private'})
            fixture.perform('DRAW_ONE')
        self.assertNotEqual(self.h.epoch, other.horizon.epoch)
        self.assertEqual(self.h._state['root'], other.horizon._state['root'])
        self.assertEqual(self.h._backend.application_values, other.horizon._backend.application_values)


if __name__ == '__main__':
    unittest.main()
