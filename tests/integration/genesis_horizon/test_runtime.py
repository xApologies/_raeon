import copy
import json
from pathlib import Path
import tempfile
import unittest

from support import Fixture, ROOT, Port, port_decode
from raeon_genesis_horizon.adapter import Horizon, HorizonError
from raeon_genesis_horizon.toolchain import digest, file_hash, compile_paths, execute
from raeon_hypervisor import encode


class RuntimeTests(unittest.TestCase):
    def setUp(self):
        self.f = Fixture()
        self.addCleanup(self.f.close)
        self.h = self.f.horizon

    def test_native_boot_identities_and_containment(self):
        # H-01, H-04..08, H-09; actual cell reads and resolved resources.
        b = self.h._backend
        self.assertEqual(set(self.h.domains()), {'sea', 'shell', 'nexus', 'state'})
        self.assertEqual(len({d['identity'] for d in self.h.domains().values()}), 4)
        self.assertEqual(self.h.domains()['sea']['dimensions'], [9, 10, 11])
        self.assertEqual(self.h.domains()['shell']['dimensions'], [7, 8])
        ids = {k: v['identity'] for k, v in self.h.domains().items()}
        pairs = {(b.resources[r]['payload']['source'], b.resources[r]['payload']['target']) for r in b.relations}
        for left, right in [('sea', 'shell'), ('shell', 'nexus'), ('nexus', 'state')]:
            self.assertIn((ids[left], ids[right]), pairs)
        for name in ids:
            self.assertEqual(len(b.read_cells(b.resources[b.bindings[name]])), 5)
        self.assertEqual(len(b.bindings), 6)
        self.assertEqual(self.h.realize_application(self.f.package, self.f.writer)['id'], 'horizon-conformance')
        with self.assertRaises(HorizonError):
            self.h.boot()
        other = Fixture('another-machine')
        self.addCleanup(other.close)
        self.assertNotEqual(other.horizon.domains()['state']['identity'], ids['state'])
        root = other.horizon._state['root']
        self.h.execute(self.f.intent(), self.f.writer)
        self.assertEqual(root, other.horizon._state['root'])

    def test_missing_and_tampered_sources(self):
        # H-02, H-03, H-10.
        with tempfile.TemporaryDirectory(dir=ROOT / 'build') as directory:
            candidate = Horizon(Path(directory) / 'missing')
            profile = copy.deepcopy(self.h.profile)
            del profile['definitions']['sea']
            with self.assertRaises(HorizonError):
                candidate.boot(profile)
            self.assertEqual(candidate.lifecycle, 'FAULTED')
            bad = Path(directory) / 'bad.gcf'
            bad.write_bytes(b'not a fabric')
            candidate = Horizon(Path(directory) / 'tampered')
            with self.assertRaisesRegex(Exception, 'FABRIC_INTEGRITY'):
                candidate.boot(trusted_context={'fabric_path': str(bad)})
            self.assertEqual(candidate.lifecycle, 'FAULTED')
        before = self.h._state['root']
        with self.assertRaises(HorizonError):
            self.h.realize_application(self.f.package, self.f.reader)
        bad = dict(self.f.package, sha256='0' * 64)
        with self.assertRaises(HorizonError):
            self.h.realize_application(bad, self.f.writer)
        self.assertEqual(before, self.h._state['root'])

    def test_real_joint_trace_and_identity_history(self):
        # H-11..13, H-15..16, R-01..02, R-04, R-08, S-01..02, V-01,V-12.
        port = Port()
        _, frames = self.f.send('HELLO', {'protocol': 2})
        for frame in frames:
            port.accept(frame)
        initial = copy.deepcopy(port.view)
        domains = self.h.domains()
        source = file_hash(self.h._backend.fabric.path)
        revision = self.h._state['revision']
        self.h.observe(self.f.writer)
        self.assertEqual(revision, self.h._state['revision'])
        for index, op in enumerate(['RELATE_A_B', 'TRANSFORM_A']):
            result, frames = self.f.send('INTENT', self.f.intent('r' + str(index), op, index))
            self.assertEqual(result['status'], 'PROCESSED')
            decoded = [port.accept(frame) for frame in frames]
            self.assertEqual(decoded[0]['kind'], 'RECEIPT')
            self.assertEqual(decoded[0]['payload']['status'], 'COMMITTED')
            self.assertEqual(decoded[1]['kind'], 'DELTA')
            self.assertEqual(port.view, self.h.observe(self.f.writer)['view'])
        self.assertEqual(port.view['objects']['A']['identity'], initial['objects']['A']['identity'])
        for before, after in zip(initial['objects']['A']['cells'], port.view['objects']['A']['cells']):
            self.assertEqual(after['handedness'], -before['handedness'])
            self.assertEqual(after['occupancy'], 0x96 if before['occupancy'] == 0x69 else 0x69)
        self.assertEqual(len(port.view['relations']), 1)
        self.assertEqual(self.h._state['revision'], 2)
        for name, domain in domains.items():
            self.assertEqual(self.h.domains()[name]['identity'], domain['identity'])
        self.assertNotEqual(self.h.domains()['state']['version'], domains['state']['version'])
        b = self.h._backend
        native = b.resources[b.bindings['A']]['payload']['native']
        self.assertIn('parent_instance_id', native)
        self.assertGreaterEqual(len(native['history']), 2)
        self.assertEqual(file_hash(b.fabric.path), source)
        paths = [(r['source_address']['domain_id'], r['waypoints'][-1]['domain_id']) for r in b.road_history[-6:]]
        self.assertEqual(paths, [('sea', 'shell'), ('shell', 'nexus'), ('nexus', 'state'), ('state', 'nexus'), ('nexus', 'shell'), ('shell', 'sea')])
        self.assertTrue(all(r['status'] == 'CLOSED' for r in b.road_history))
        self.assertTrue(all(r['canonical_mmo_id'] == 'HORIZON:REFERENCE:request' for r in b.road_history))
        port.view['objects']['A']['cells'][0]['occupancy'] = 1
        self.assertNotEqual(port.view, self.h.observe(self.f.writer)['view'])

    def test_candidate_rollback_and_budget(self):
        # H-14,L-01. Fault after native transform but before publication.
        before = copy.deepcopy(self.h._state)
        cells = self.h._view(self.f.writer)
        def failure(point):
            if point == 'after_candidate':
                raise HorizonError('CLOSURE_FAILED')
        self.h.fault_hook = failure
        with self.assertRaisesRegex(HorizonError, 'CLOSURE_FAILED'):
            self.h.execute(self.f.intent(), self.f.writer)
        self.assertEqual(before, self.h._state)
        self.assertEqual(cells, self.h._view(self.f.writer))
        self.h.fault_hook = lambda point: None
        with self.assertRaisesRegex(HorizonError, 'BUDGET_EXCEEDED'):
            self.h.execute(self.f.intent(), self.f.writer, budget=1)
        self.assertEqual(before, self.h._state)

    def test_route_admission_and_open_resource_rejections(self):
        # R-03,R-05..07. Actual compiler/binding; never publishes candidate.
        b = self.h._backend
        source = (ROOT / 'game/core/genesis_horizon/src/road_in.gen').read_text(encoding='utf8')
        from genesis_frontend.compiler import compile_sources
        original = self.h._state['root']
        for variant in [source.replace('sea->shell', 'sea->state'),
                        source.replace('  tor p3 with g3 as c3', ''),
                        source.replace('  road close road3 g3 as closed', '').replace('  export closed : RECEIPT<ROAD_CLOSE>', ''),
                        source.replace('@{"operation":"ROUTE"}', '@{"admitted":true}')]:
            saved = copy.deepcopy(self.h._record())
            b.active_request = {'source': 'sea', 'semantic': 'negative'}
            b.authority = {'actor': 'writer', 'operations': ['ROUTE']}
            with self.assertRaises(Exception):
                execute(compile_sources([('negative.gen', variant)], name='negative'), b)
            self.h._restore_record(saved)
            self.assertEqual(self.h._state['root'], original)
        geo = b.resources[b.bindings['state']]
        b.authority = {'actor': 'writer', 'operations': ['ROUTE']}
        with self.assertRaisesRegex(Exception, 'AUTHORITY_DENIED'):
            b.admit(geo, {'operation': 'ROUTE', 'admitted': True})

    def test_retry_conflict_concurrent_scope_and_stale(self):
        # S-04..08.
        request = self.f.intent()
        encoded = encode(self.f.envelope('INTENT', request), 'in')
        for _ in range(2):
            self.assertEqual(self.f.bridge.receive(self.f.handle, encoded)['status'], 'QUEUED')
        for _ in range(2):
            self.assertEqual(self.f.bridge.step()['status'], 'PROCESSED')
        frames = self.f.bridge.drain(self.f.handle)
        receipts = [port_decode(frame)['payload'] for frame in frames if port_decode(frame)['kind'] == 'RECEIPT']
        self.assertEqual(receipts[0], receipts[1])
        self.assertEqual(self.h._state['revision'], 1)
        result, _ = self.f.send('INTENT', dict(request, operation='RELATE_A_B'))
        self.assertEqual(result['code'], 'REQUEST_ID_CONFLICT')
        result, _ = self.f.send('INTENT', self.f.intent('stale'))
        self.assertEqual(result['code'], 'STALE_PRECONDITION')
        reader = self.f.bridge.bind_session(self.f.reader)
        result, _ = self.f.send('INTENT', request, reader)
        self.assertEqual(result['code'], 'AUTHORITY_DENIED')
        self.assertEqual(self.h._state['revision'], 1)
        reconnect = self.f.bridge.bind_session(self.f.writer)
        result, frames = self.f.send('INTENT', request, reconnect)
        self.assertEqual(result['status'], 'PROCESSED')
        self.assertEqual(port_decode(frames[0])['payload'], receipts[0])

    def test_expired_retry_is_never_reexecuted(self):
        # S-11: retain the key and digest tombstone, not a forgotten volatile set.
        self.h.execute(self.f.intent(), self.f.writer)
        self.h.expire_outcome(('horizon-conformance', 'writer', 'r1'), self.f.writer)
        result, frames = self.f.send('INTENT', self.f.intent())
        self.assertEqual(result['code'], 'RETRY_EXPIRED')
        self.assertEqual(self.h._state['revision'], 1)

    def test_privacy_and_scope(self):
        # V-10,V-11,V-13; trusted context cannot be changed by caller alias.
        context = copy.deepcopy(self.f.reader)
        handle = self.f.bridge.bind_session(context)
        context['private_view'] = True
        context['view_id'] = 'writer'
        _, frames = self.f.send('HELLO', {'protocol': 2}, handle)
        snapshot = port_decode(frames[1])['payload']
        self.assertEqual(set(snapshot['view']['objects']), {'A'})
        self.assertNotIn('native', json.dumps(snapshot))
        result, _ = self.f.send('SYNC_REQUEST', {'view_id': 'writer', 'revision': 0}, handle)
        self.assertEqual(result['code'], 'AUTHORITY_DENIED')
        for field, value in [('application_id', 'another-app'), ('epoch', 'old-epoch')]:
            message = self.f.envelope('HEARTBEAT', {})
            message[field] = value
            self.assertEqual(self.f.bridge.receive(handle, encode(message, 'in'))['status'], 'REJECTED')
        forged = self.f.envelope('INTENT', dict(self.f.intent(), actor='writer'))
        with self.assertRaises(ValueError):
            encode(forged, 'in')

    def test_delivery_failure_recovery(self):
        # S-10; commit happens in Horizon before bridge output.
        def failure(point):
            if point == 'after_commit':
                raise OSError('simulated loss of return delivery')
        self.h.fault_hook = failure
        result, frames = self.f.send('INTENT', self.f.intent())
        self.assertEqual(result['status'], 'PROCESSED')
        committed = port_decode(frames[0])['payload']
        self.assertEqual(committed['status'], 'COMMITTED')
        self.assertEqual(self.h._state['revision'], 1)
        self.h.fault_hook = lambda point: None
        result, frames = self.f.send('INTENT', self.f.intent())
        self.assertEqual(port_decode(frames[0])['payload'], committed)
        self.assertEqual(self.h._state['revision'], 1)

    def test_projection_gap_receipt_clock_and_reconnect(self):
        # S-03,S-09,S-12.
        port = Port()
        _, frames = self.f.send('HELLO', {'protocol': 2})
        for frame in frames:
            port.accept(frame)
        _, frames = self.f.send('INTENT', self.f.intent('one', 'TRANSFORM_A', 0))
        port.accept(frames[0])
        self.assertEqual(port.revision, 0)
        _, frames = self.f.send('INTENT', self.f.intent('two', 'TRANSFORM_A', 1))
        with self.assertRaisesRegex(ValueError, 'gap'):
            port.accept(frames[1])
        for history in self.f.bridge.views.values():
            history.deltas.clear()
        _, frames = self.f.send('SYNC_REQUEST', {'view_id': 'writer', 'revision': 0})
        self.assertEqual(port_decode(frames[0])['kind'], 'SNAPSHOT')
        port.accept(frames[0])
        self.assertEqual(port.view, self.h._view(self.f.writer))
        before = port.revision
        self.f.send('ACK', {'delivery_sequence': self.f.bridge.sessions[self.f.handle].sequence})
        self.assertEqual(port.revision, before)

    def test_backpressure_before_mutation(self):
        # V-14,V-15; no dropped accepted effect.
        bridge = self.f.bridge
        bridge.config['inbound_per_session'] = 1
        frame = encode(self.f.envelope('INTENT', self.f.intent()), 'in')
        self.assertEqual(bridge.receive(self.f.handle, frame)['status'], 'QUEUED')
        self.assertEqual(bridge.receive(self.f.handle, frame)['code'], 'BACKPRESSURE')
        bridge.config['outbound_bytes_per_session'] = 200
        result = bridge.step()
        self.assertEqual(result['code'], 'BACKPRESSURE')
        self.assertEqual(self.h._state['revision'], 0)

    def test_checkpoint_restart_corruption_and_confinement(self):
        # L-04,L-05,L-07,L-08.
        self.h.execute(self.f.intent(), self.f.writer)
        expected = copy.deepcopy(self.h._state)
        domains = self.h.domains()
        checkpoint = self.h.checkpoint(self.f.writer)
        before_epoch = self.h.epoch
        with self.assertRaises(HorizonError):
            self.h.restore(dict(checkpoint, name='../escape'), self.f.writer)
        bad = dict(checkpoint, sha256='0' * 64)
        with self.assertRaises(HorizonError):
            self.h.restore(bad, self.f.writer)
        self.assertEqual(self.h._state, expected)
        original = self.h.storage
        self.h.close()
        restarted = Horizon(original)
        self.addCleanup(restarted.close)
        restarted.restore(checkpoint, self.f.writer)
        self.assertEqual(restarted._state, expected)
        self.assertEqual(restarted.domains(), domains)
        self.assertNotEqual(restarted.epoch, before_epoch)
        self.assertEqual(restarted.execute(self.f.intent(), self.f.writer)['revision'], 1)
        self.assertEqual(restarted._state['root'], expected['root'])

    def test_quiesce_close_and_replay(self):
        # L-02,L-03,L-06,D-01.
        other = Fixture('acceptance')
        self.addCleanup(other.close)
        for h in (self.h, other.horizon):
            for index, operation in enumerate(['RELATE_A_B', 'TRANSFORM_A']):
                h.execute(self.f.intent(str(index), operation, index), self.f.writer)
        self.assertEqual(self.h._state['root'], other.horizon._state['root'])
        self.assertEqual([x['root'] for x in self.h._state['inputs']], [x['root'] for x in other.horizon._state['inputs']])
        self.h.quiesce()
        with self.assertRaises(HorizonError):
            self.h.execute(self.f.intent('new', revision=2), self.f.writer)
        self.assertEqual(self.h.close(), self.h.close())
        for source in sorted((ROOT / 'game/core/genesis_horizon/src').glob('*.gen')):
            a = compile_paths([source], ROOT, source.stem)
            b = compile_paths([source], ROOT, source.stem)
            self.assertEqual(a.link.bytecode, b.link.bytecode)


if __name__ == '__main__':
    unittest.main()
