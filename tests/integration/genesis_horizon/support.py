"""Real runtime fixture and independent Port decoder; no fake Horizon adapter."""
import hashlib
import json
from pathlib import Path
import struct
import sys
import tempfile
import zlib

ROOT = Path(__file__).resolve().parents[3]
for relative in ['game/core/genesis_horizon/bindings/python/src', 'platform/shared/python_hypervisor/src']:
    sys.path.insert(0, str(ROOT / relative))

from raeon_genesis_horizon.adapter import Horizon
from raeon_genesis_horizon.toolchain import file_hash
from raeon_hypervisor import open, encode


def port_decode(frame):
    # Deliberately independent of the production codec.
    if frame[:8] != b'RAEONH2!' or frame[8:12] != bytes([2, 0, 0, 0]):
        raise ValueError('header')
    size = int.from_bytes(frame[12:16], 'big')
    checksum = int.from_bytes(frame[16:20], 'big')
    payload = frame[20:]
    if len(payload) != size or zlib.crc32(payload) != checksum:
        raise ValueError('integrity')
    return json.loads(payload.decode('utf8'))


class Port:
    def __init__(self):
        self.view = None
        self.revision = None
        self.epoch = None
        self.view_id = None
        self.receipts = []

    def accept(self, frame):
        envelope = port_decode(frame)
        body = envelope['payload']
        if envelope['kind'] == 'SNAPSHOT':
            self.view, self.revision, self.epoch, self.view_id = body['view'], body['revision'], body['epoch'], body['view_id']
        elif envelope['kind'] == 'DELTA':
            if (body['epoch'], body['view_id'], body['base_revision']) != (self.epoch, self.view_id, self.revision):
                raise ValueError('projection gap')
            self.view = body['changes']['replace_view']
            self.revision = body['revision']
        elif envelope['kind'] == 'RECEIPT':
            self.receipts.append(body)
        if envelope['kind'] in ('SNAPSHOT', 'DELTA'):
            payload = json.dumps(self.view, sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode()
            if hashlib.sha256(payload).hexdigest() != body['digest']:
                raise ValueError('view integrity')
        return envelope


class Fixture:
    def __init__(self, identity='acceptance', path=None):
        self.temp = tempfile.TemporaryDirectory(prefix='horizon real ', dir=ROOT / 'build') if path is None else None
        self.path = Path(path or self.temp.name)
        self.horizon = Horizon(self.path)
        self.writer = {'actor': 'writer', 'application_id': 'horizon-conformance', 'view_id': 'writer', 'private_view': True,
                       'operations': ['OBSERVE', 'RELATE_A_B', 'TRANSFORM_A'], 'realize': True, 'checkpoint': True, 'restore': True}
        self.reader = {'actor': 'reader', 'application_id': 'horizon-conformance', 'view_id': 'public', 'operations': ['OBSERVE']}
        self.boot = self.horizon.boot(trusted_context={'instance_identity': identity})
        self.package = {'path': 'tests/integration/genesis_horizon/application/manifest.json',
                        'sha256': file_hash(ROOT / 'tests/integration/genesis_horizon/application/manifest.json')}
        self.horizon.realize_application(self.package, self.writer)
        self.bridge = open(self.horizon, self.horizon.profile['limits'])
        self.handle = self.bridge.bind_session(self.writer)
        self.number = 0

    def envelope(self, kind, payload, handle=None):
        handle = handle or self.handle
        self.number += 1
        return {'schema_version': 2, 'kind': kind, 'message_id': 'message-' + str(self.number),
                'application_id': self.bridge.sessions[handle].authority['application_id'], 'epoch': self.bridge.epoch, 'payload': payload}

    def send(self, kind, payload, handle=None, budget=100000):
        handle = handle or self.handle
        result = self.bridge.receive(handle, encode(self.envelope(kind, payload, handle), 'in'))
        if result['status'] != 'QUEUED':
            raise AssertionError(result)
        step = self.bridge.step(budget)
        return step, self.bridge.drain(handle)

    def intent(self, request='r1', operation='TRANSFORM_A', revision=0):
        return {'request_id': request, 'operation': operation, 'arguments': {}, 'expected_revision': revision}

    def close(self):
        self.horizon.close()
        if self.temp:
            self.temp.cleanup()
