import copy
import json
from pathlib import Path
import struct
import sys
import unittest
import zlib

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'platform/shared/python_hypervisor/src'))
from raeon_hypervisor.codec import encode, decode, HEADER
from raeon_hypervisor.errors import BoundaryError
from raeon_hypervisor.hypervisor import Hypervisor


def message(kind='INTENT'):
    return {'schema_version': 2, 'kind': kind, 'message_id': 'm1', 'application_id': 'app', 'epoch': 'e1',
            'payload': {'request_id': 'r1', 'operation': 'op', 'arguments': {}, 'expected_revision': 0}}


def raw(payload, major=2, minor=0, flags=0, size=None, checksum=None):
    return struct.pack('>8sBBHII', b'RAEONH2!', major, minor, flags, len(payload) if size is None else size,
                       zlib.crc32(payload) if checksum is None else checksum) + payload


class NeverExecute:
    """Unit-only adapter: a call into semantics is a test failure, not integration evidence."""
    epoch = 'e1'

    def execute(self, *args):
        raise AssertionError('receive must not execute')


class CodecTests(unittest.TestCase):
    def test_independent_vector(self):
        # V-01: constructed without production serializer/header helper.
        body = b'{"application_id":"app","epoch":"e1","kind":"HEARTBEAT","message_id":"m1","payload":{},"schema_version":2}'
        fixture = raw(body)
        decoded = decode(fixture)
        self.assertEqual(decoded['kind'], 'HEARTBEAT')
        self.assertEqual(encode(decoded, 'in'), fixture)
        self.assertEqual(int.from_bytes(fixture[12:16], 'big'), len(body))
        vector = json.loads((ROOT / 'platform/shared/python_hypervisor/schemas/wire-vectors.json').read_text(encoding='utf8'))
        self.assertEqual(bytes.fromhex(vector['heartbeat_v2_hex']), fixture)

    def test_versions_direction_and_lengths(self):
        # V-02,V-03,V-04,V-08.
        frame = encode(message(), 'in')
        body = frame[20:]
        for invalid in [raw(body, major=3), raw(body, minor=1), raw(body, flags=1)]:
            with self.subTest(invalid=invalid[:12]), self.assertRaisesRegex(BoundaryError, 'UNSUPPORTED_VERSION'):
                decode(invalid)
        for invalid in [frame[:19], frame[:-1], frame + b'x', raw(body, size=999999), raw(body, checksum=0), raw(body, size=1048577)]:
            with self.subTest(length=len(invalid)), self.assertRaises(BoundaryError):
                decode(invalid)
        with self.assertRaises(BoundaryError):
            decode(frame, 'out')
        with self.assertRaises(BoundaryError):
            encode(message('SNAPSHOT'), 'in')
        invalid = message()
        invalid['schema_version'] = 1
        with self.assertRaisesRegex(BoundaryError, 'UNSUPPORTED_VERSION'):
            decode(raw(json.dumps(invalid).encode()))

    def test_json_unicode_duplicates_constants(self):
        # V-05.
        for payload in [b'\xff', b'{', b'[]', b'{"x":1,"x":2}', b'{"x":NaN}', b'{"x":Infinity}', b'{"x":-Infinity}', b'"bad\\ud800"']:
            with self.subTest(payload=payload), self.assertRaises(BoundaryError):
                decode(raw(payload))

    def test_numeric_and_shape_validation_on_both_paths(self):
        # V-06,V-07,V-10.
        mutations = []
        for value in [True, -1, 9007199254740992, 0.5, '0', None]:
            m = message()
            m['payload']['expected_revision'] = value
            mutations.append(m)
        for value in ['', 'x' * 129, 'has space', '../path', '\ud800', 1, True]:
            m = message()
            m['message_id'] = value
            mutations.append(m)
        for key, value in [('payload', []), ('actor', 'admin'), ('kind', ['INTENT']), ('schema_version', True)]:
            m = message()
            m[key] = value
            mutations.append(m)
        m = message()
        m['payload']['grant'] = 'admin'
        mutations.append(m)
        m = message()
        m['payload']['arguments'] = []
        mutations.append(m)
        m = message()
        value = {}
        for _ in range(30):
            value = {'x': value}
        m['payload']['arguments'] = value
        mutations.append(m)
        for m in mutations:
            with self.subTest(m=m):
                with self.assertRaises(BoundaryError):
                    encode(m, 'in')
                with self.assertRaises(BoundaryError):
                    decode(raw(json.dumps(m).encode()))

    def test_fragment_assembly_and_unbound_scope(self):
        # V-09,V-11,V-14. Unit-only mock rejects any accidental execute.
        config = {'max_payload_bytes': 4096, 'inbound_per_session': 1, 'outbound_bytes_per_session': 16384, 'delta_history': 2, 'diagnostics': 2}
        bridge = Hypervisor(NeverExecute(), config)
        handle = bridge.bind_session({'actor': 'a', 'application_id': 'app', 'view_id': 'public'})
        frame = encode(message(), 'in')
        self.assertEqual(bridge.receive(handle, frame[:12])['status'], 'BUFFERED')
        self.assertEqual(bridge.receive(handle, frame[12:])['status'], 'QUEUED')
        self.assertEqual(bridge.receive(handle, frame)['code'], 'BACKPRESSURE')
        self.assertEqual(bridge.receive('forged', frame)['code'], 'UNBOUND_SESSION')
        self.assertEqual(bridge.receive(handle, raw(b'', size=4097))['code'], 'MALFORMED_FRAME')
        self.assertEqual(len(bridge.sessions[handle].buffer), 0)

    def test_outgoing_schema_and_bounded_drain(self):
        # Encode-side validation cannot emit arbitrary dictionaries as protocol.
        m = {'schema_version': 2, 'kind': 'RECEIPT', 'message_id': 'm', 'application_id': 'a', 'epoch': 'e',
             'correlation_id': 'r', 'payload': {'status': 'COMMITTED', 'request_id': 'request'}}
        self.assertEqual(decode(encode(m), 'out'), m)
        for status in ['success', True, None]:
            m['payload']['status'] = status
            with self.assertRaises(BoundaryError):
                encode(m)
        from raeon_hypervisor.session import Session
        from raeon_hypervisor.delivery import drain
        s = Session({})
        s.outgoing.extend([b'abc', b'def'])
        s.queued_bytes = 6
        self.assertEqual(drain(s, 5, 2), ())
        self.assertEqual(drain(s, 5, 4), (b'abc',))
        self.assertEqual(s.queued_bytes, 3)


if __name__ == '__main__':
    unittest.main()
