"""Production package exercised through the actual Horizon and byte fence."""
import copy
import json
from pathlib import Path
import shutil
import tempfile

from support import ROOT, Port, port_decode
from raeon_genesis_horizon.adapter import Horizon
from raeon_genesis_horizon.toolchain import file_hash
from raeon_hypervisor import open, encode

PACKAGE = 'game/core/raeon/application/manifest.json'


class ProductionFixture:
    def __init__(self, realize=True):
        self.temp = tempfile.TemporaryDirectory(prefix='pass01 actual ', dir=ROOT / 'build')
        self.path = Path(self.temp.name)
        self.horizon = Horizon(self.path / 'machine')
        self.owner = {'actor': 'runtime-owner', 'realize': True, 'checkpoint': True, 'restore': True}
        self.players = {
            p: {'actor': 'trusted-' + p, 'application_id': 'raeon', 'view_id': p,
                'player_role': p, 'private_view': True, 'operations': ['OBSERVE']}
            for p in ['player_1', 'player_2']}
        self.package = {'path': PACKAGE, 'sha256': file_hash(ROOT / PACKAGE)}
        self.boot = self.horizon.boot(trusted_context={'instance_identity': 'pass01-match'})
        if realize:
            self.realization = self.horizon.realize_application(self.package, self.owner)
        self.bridge = None
        self.serial = 0

    def connect(self):
        self.bridge = open(self.horizon, self.horizon.profile['limits'])
        self.handles = {p: self.bridge.bind_session(a) for p, a in self.players.items()}

    def send(self, player, kind, payload):
        self.serial += 1
        message = {'schema_version': 2, 'kind': kind, 'message_id': 'message-' + str(self.serial),
                   'application_id': 'raeon', 'epoch': self.bridge.epoch, 'payload': payload}
        handle = self.handles[player]
        assert self.bridge.receive(handle, encode(message, 'in'))['status'] == 'QUEUED'
        result = self.bridge.step()
        assert result['status'] == 'PROCESSED', result
        return self.bridge.drain(handle)

    def hello(self, player):
        frames = self.send(player, 'HELLO', {'protocol': 2})
        assert [port_decode(f)['kind'] for f in frames] == ['WELCOME', 'SNAPSHOT']
        port = Port()
        for frame in frames:
            port.accept(frame)
        return port

    def candidate(self, modify=None, mutate_source=None, mutate_definitions=None):
        directory = self.path / ('candidate-' + str(self.serial))
        self.serial += 1
        shutil.copytree((ROOT / PACKAGE).parent, directory)
        manifest = json.loads((directory / 'manifest.json').read_text(encoding='utf8'))
        if mutate_source:
            source = directory / manifest['realize']
            source.write_text(mutate_source(source.read_text(encoding='utf8')), encoding='utf8', newline='\n')
            manifest['files'][source.name] = file_hash(source)
        if mutate_definitions:
            source = directory / manifest['definitions']
            definitions = json.loads(source.read_text(encoding='utf8'))
            mutate_definitions(definitions)
            source.write_text(json.dumps(definitions), encoding='utf8', newline='\n')
            manifest['files'][source.name] = file_hash(source)
        if modify:
            modify(manifest, directory)
        target = directory / 'manifest.json'
        target.write_text(json.dumps(manifest), encoding='utf8', newline='\n')
        self.horizon.application_roots.append(directory.resolve())
        return {'path': target.relative_to(ROOT).as_posix(), 'sha256': file_hash(target)}

    def restart(self):
        before = {p: copy.deepcopy(self.horizon._view(a)) for p, a in self.players.items()}
        checkpoint = self.horizon.checkpoint(self.owner)
        root, revision, epoch = self.horizon._state['root'], self.horizon._state['revision'], self.horizon.epoch
        storage = self.horizon.storage
        self.horizon.close()
        self.horizon = Horizon(storage)
        self.horizon.restore(checkpoint, self.owner)
        assert self.horizon._state['root'] == root
        assert self.horizon._state['revision'] == revision
        assert self.horizon.epoch != epoch
        self.connect()
        for p in self.players:
            assert self.hello(p).view == before[p]
        return {'checkpoint': checkpoint, 'root': root, 'revision': revision,
                'old_epoch': epoch, 'new_epoch': self.horizon.epoch, 'views_equal': True}

    def close(self):
        self.horizon.close()
        self.temp.cleanup()
