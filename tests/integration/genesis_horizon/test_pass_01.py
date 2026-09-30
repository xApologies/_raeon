import copy
import json
import unittest
from pathlib import Path

from pass_01_support import ProductionFixture, PACKAGE, ROOT, port_decode
from raeon_genesis_horizon.adapter import HorizonError
from raeon_genesis_horizon.toolchain import compile_paths, file_hash


class Pass01Tests(unittest.TestCase):
    def setUp(self):
        self.f = ProductionFixture(realize=False)
        self.addCleanup(self.f.close)
        self.h = self.f.horizon

    def realize(self):
        self.h.realize_application(self.f.package, self.f.owner)
        return self.h._view(self.f.players['player_1'])

    def reject(self, package=None, authority=None, expected=None):
        state, native = copy.deepcopy(self.h._state), copy.deepcopy(self.h._record())
        journal = (self.h.storage / 'root.json').read_bytes()
        with self.assertRaisesRegex(Exception, expected or '.'):
            self.h.realize_application(package or self.f.package, authority or self.f.owner)
        self.assertEqual(self.h._state, state)
        self.assertEqual(self.h._record(), native)
        self.assertEqual((self.h.storage / 'root.json').read_bytes(), journal)
        self.assertEqual(self.h._semantic_root(self.h._state), state['root'])

    def test_production_manifest_and_real_genesis(self):
        manifest = json.loads((ROOT / PACKAGE).read_text(encoding='utf8'))
        self.assertEqual(manifest['id'], 'raeon')
        self.assertFalse(manifest['test_only'])
        self.assertTrue(PACKAGE.startswith('game/'))
        before = self.h.domains()['state']
        view = self.realize()
        after = self.h.domains()['state']
        self.assertEqual(before['identity'], after['identity'])
        self.assertNotEqual(before['version'], after['version'])
        self.assertEqual(len(view['objects']), 37)
        native = self.h._backend
        instantiated = {r['name'] for r in native.native_receipts if r['operation'] == 'instantiate'}
        self.assertTrue(set(view['objects']) <= instantiated)
        self.assertEqual(len(native.road_history), 6)
        for name in view['objects']:
            resource = native.resources[native.bindings[name]]
            self.assertEqual(resource['kind'], 'GEOMETRIC')
            self.assertEqual(resource['payload']['domain'], 'state')
            self.assertEqual(len(native.read_cells(resource)), 5)

    def test_production_bytecode_is_deterministic(self):
        for source in sorted((ROOT / PACKAGE).parent.glob('*.gen')):
            a = compile_paths([source], ROOT, source.stem)
            b = compile_paths([source], ROOT, source.stem)
            self.assertEqual(a.link.bytecode, b.link.bytecode)
            self.assertTrue(a.link.receipt)

    def test_exact_topology_and_empty_containers(self):
        objects = self.realize()['objects']
        counts = {kind: sum(o['kind'] == kind for o in objects.values()) for kind in {o['kind'] for o in objects.values()}}
        self.assertEqual(counts, {'MATCH': 1, 'PLAYER': 2, 'BOARD': 2, 'ATTACHMENT_ROLE': 10,
                                 'DECK': 2, 'HAND': 2, 'GRAVEYARD': 2, 'PRIME_REGION': 2,
                                 'CONFIGURATION_REGION': 2, 'PRIME_POSITION': 6, 'CONFIGURATION_SPACE': 6})
        for p, authority in self.f.players.items():
            own = self.h._view(authority)['objects']
            for container in ['deck', 'hand', 'graveyard']:
                self.assertEqual(own[p + '_' + container]['fields']['contents'], [])
                self.assertEqual(own[p + '_' + container]['fields']['state'], 'EMPTY')
            self.assertEqual(own[p + '_hand']['fields']['normal_capacity'], 7)
            for i in (1, 2, 3):
                self.assertEqual(own[f'{p}_prime_{i}']['fields'],
                                 {'position': i, 'fixed': True, 'state': 'EMPTY', 'occupant': None})
            for letter in 'ABC':
                fields = own[p + '_config_' + letter]['fields']
                self.assertEqual(fields, {'label': letter, 'primitive': 'GEOMETRIC', 'domain': 'STATE',
                                         'qmo': False, 'permanent': True, 'universal': True,
                                         'state': 'EMPTY', 'contents': []})

    def test_explicit_relations_and_stable_unique_identity(self):
        view = self.realize()
        objects = view['objects']
        self.assertEqual(len({o['identity'] for o in objects.values()}), 37)
        self.assertEqual(len({o['semantic_id'] for o in objects.values()}), 37)
        self.assertNotIn('coordinates', json.dumps(view))
        relations = {(r['source'], r['target'], r['relation']) for r in view['relations']}
        def has(a, z, relation):
            self.assertIn((objects[a]['identity'], objects[z]['identity'], relation), relations)
        for p in self.f.players:
            b = p + '_board'
            has('match', p, 'contains'); has('match', p, 'owns'); has(p, b, 'owns')
            for role, child in [('deck','deck'),('hand','hand'),('graveyard','graveyard'),('prime','primes'),('config','configuration')]:
                port = p + '_' + role + '_port'
                has(b, port, 'contains'); has(port, p + '_' + child, 'attaches')
                has(b, p + '_' + child, 'contains')
                self.assertNotEqual(objects[port]['identity'], objects[p + '_' + child]['identity'])
            for name, obj in objects.items():
                has(name, p, 'visible_to')
                if obj['owner'] == p and name != p:
                    has(p, name, 'owns')

    def test_owner_opponent_privacy_and_no_native_leak(self):
        self.realize()
        for p, authority in self.f.players.items():
            other = 'player_2' if p == 'player_1' else 'player_1'
            view = self.h.observe(authority)['view']
            for container in ['deck', 'hand', 'graveyard']:
                self.assertIn('contents', view['objects'][p + '_' + container]['fields'])
                self.assertNotIn('contents', view['objects'][other + '_' + container]['fields'])
                self.assertNotIn('order', view['objects'][other + '_' + container]['fields'])
            for r in view['relations']:
                if r['relation'] == 'private_to':
                    self.assertEqual(r['target'], view['objects'][p]['identity'])
            serialized = json.dumps(view)
            for forbidden in ['segment_path', 'resource_id', 'native', 'receipt', 'allocator', 'C:\\', '.gos', '.gtd']:
                self.assertNotIn(forbidden, serialized)
            for forged in [dict(authority, player_role=other), dict(authority, private_view=False), dict(authority, view_id=other)]:
                with self.assertRaisesRegex(HorizonError, 'AUTHORITY_DENIED'):
                    self.h.observe(forged)
        public = self.h.observe({'actor':'spectator','application_id':'raeon','view_id':'public'})['view']
        self.assertFalse(any(r['relation'] == 'private_to' for r in public['relations']))
        for p in self.f.players:
            for container in ['deck','hand','graveyard']:
                self.assertNotIn('contents', public['objects'][p+'_'+container]['fields'])
                self.assertNotIn('order', public['objects'][p+'_'+container]['fields'])

    def test_observation_and_idempotence_do_not_duplicate(self):
        view = self.realize()
        before = copy.deepcopy(self.h._state)
        identities = {k: v['identity'] for k, v in view['objects'].items()}
        relations = copy.deepcopy(self.h._backend.relations)
        for _ in range(3):
            self.assertEqual(self.h.realize_application(self.f.package, self.f.owner), before['application'])
            self.assertEqual(self.h.observe(self.f.players['player_1'])['view'], view)
            self.assertEqual(self.h._state, before)
        self.assertEqual(self.h._backend.relations, relations)
        self.assertEqual({k: v['identity'] for k, v in self.h._view(self.f.players['player_1'])['objects'].items()}, identities)

    def test_conflicting_application_rejected(self):
        self.realize()
        self.reject(self.f.candidate(modify=lambda m, _: m.update(id='conflicting-application')))

    def test_unauthorized_realization_rejected(self):
        self.reject(authority={'actor': 'untrusted', 'realize': False})

    def test_package_and_source_hash_tamper_rejected(self):
        self.reject(dict(self.f.package, sha256='0'*64))
        self.reject(self.f.candidate(modify=lambda m, d: (d/m['realize']).write_text('tampered', encoding='utf8')))

    def test_path_escape_rejected(self):
        self.reject({'path':'data/platform/genesis-horizon-profile.json','sha256':file_hash(ROOT/'data/platform/genesis-horizon-profile.json')})
        def escape(m, directory):
            outside = directory.parent/'outside.gen'
            outside.write_text('genesis 0.1.0', encoding='utf8')
            m['realize'] = '../outside.gen'; m['files']['../outside.gen'] = file_hash(outside)
        self.reject(self.f.candidate(modify=escape))

    def test_undeclared_and_malformed_source_rejected(self):
        self.reject(self.f.candidate(modify=lambda m, _: m['files'].pop(m['realize'])))
        self.reject(self.f.candidate(mutate_source=lambda _: 'this is not Genesis'))
        self.reject(self.f.candidate(mutate_source=lambda s: s.replace('mmo @match', 'mmo @undeclared')))

    def test_duplicate_and_conflicting_identity_rejected(self):
        def duplicate(d): d['player_2']['semantic']['id'] = d['player_1']['semantic']['id']
        self.reject(self.f.candidate(mutate_definitions=duplicate))
        def collision(d): d['player_2']['mmo_id'] = d['player_1']['mmo_id']
        self.reject(self.f.candidate(mutate_definitions=collision))
        self.reject(self.f.candidate(mutate_source=lambda s: s.replace('mmo @player_2\n', 'mmo @player_1\n')), expected='DUPLICATE_INSTANCE')

    def test_missing_or_undeclared_relation_rejected(self):
        self.reject(self.f.candidate(mutate_source=lambda s: s.replace('  rel state -> match as relation_0 @{"relation":"contains"}\n','')))
        self.reject(self.f.candidate(mutate_source=lambda s: s.replace('"relation":"contains"','"relation":"unauthorized"',1)))

    def test_prepublication_failure_and_budget_roll_back(self):
        for point in ['after_candidate','before_publish']:
            def fail(actual, expected=point):
                if actual == expected: raise RuntimeError('injected prepublication failure')
            self.h.fault_hook = fail
            self.reject(expected='injected prepublication failure')
        self.h.fault_hook = lambda _: None
        before = self.h._state['root']
        with self.assertRaisesRegex(HorizonError, 'BUDGET_EXCEEDED'):
            self.h.realize_application(self.f.package, self.f.owner, budget=10)
        self.assertEqual(self.h._semantic_root(self.h._state), before)
        self.realize()

    def test_application_cannot_inherit_or_mutate_machine_domains(self):
        for name in ['sea','shell','nexus','state']:
            addition = ('  en forbidden : GEOMETRIC = instantiate fabric region mmo @bound_'+name+'\n'
                        '  admit forbidden as attack @{"operation":"INHERIT_STATE"}\n')
            self.reject(self.f.candidate(mutate_source=lambda s, a=addition: s.replace('  en match :',a+'  en match :',1)), expected='AUTHORITY_DENIED')
        self.reject(self.f.candidate(mutate_source=lambda s: s.replace('mmo @match','mmo @sea',1)), expected='AUTHORITY_DENIED')

    def test_checkpoint_restart_and_two_player_sessions(self):
        self.realize()
        self.f.connect()
        before = self.h._state['root']
        for p, authority in self.f.players.items():
            port = self.f.hello(p)
            self.assertEqual(port.view, self.h._view(authority))
        self.assertEqual(self.h._state['root'], before)
        result = self.f.restart()
        self.assertTrue(result['views_equal'])
        self.assertNotEqual(result['old_epoch'], result['new_epoch'])
        self.assertEqual(result['revision'], 0)

    def test_observation_operation_receipt_has_no_native_diagnostics(self):
        self.realize()
        self.f.connect()
        before = self.h._state['root']
        for player in self.f.players:
            request = {'request_id': 'observe-1', 'operation': 'OBSERVE', 'arguments': {}, 'expected_revision': 0}
            frames = self.f.send(player, 'INTENT', request)
            messages = [port_decode(frame) for frame in frames]
            self.assertEqual(messages[0]['kind'], 'RECEIPT')
            self.assertEqual(messages[0]['payload']['status'], 'OBSERVED')
            self.assertEqual(set(messages[0]['payload']), {'status','request_digest','request_id','revision','previous_root','root','commit_id'})
            self.assertEqual(messages[1]['kind'], 'SNAPSHOT')
            repeated = self.f.send(player, 'INTENT', request)
            self.assertEqual(port_decode(repeated[0])['payload'], messages[0]['payload'])
        self.assertEqual(self.h._state['root'], before)
        self.assertEqual(self.h._state['revision'], 0)

    def test_no_pass_two_rules_exposed(self):
        self.realize()
        manifest = self.h._state['application']['manifest']
        self.assertEqual(set(manifest['operations']), {'OBSERVE'})
        self.assertEqual(manifest['scope'], 'PASS_01_EMPTY_MATCH')
        self.assertEqual(self.h._state['revision'], 0)
        self.assertEqual(self.h._state['outcomes'], {})
        self.assertEqual(self.h._state['inputs'], [])
