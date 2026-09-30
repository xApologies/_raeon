"""Conformance-only authority issuer, never packaged into the Platform Port API."""
import copy
import json
from pathlib import Path
import tempfile

from support import ROOT, port_decode
from pass_01_support import ProductionFixture
from raeon_genesis_horizon.adapter import Horizon
from raeon_genesis_horizon.toolchain import file_hash


PACKAGE = 'game/core/raeon/application/manifest.json'


class CardFixture(ProductionFixture):
    def __init__(self, identity='pass02-match'):
        self.temp = tempfile.TemporaryDirectory(prefix='pass02 actual ', dir=ROOT / 'build')
        self.path = Path(self.temp.name)
        self.capability = object()
        self.horizon = Horizon(self.path / 'machine')
        self.owner = {'actor': 'runtime-owner', 'realize': True, 'checkpoint': True, 'restore': True}
        self.manifest = json.loads((ROOT / PACKAGE).read_text(encoding='utf8'))
        self.players = {p: {'actor': 'trusted-' + p, 'application_id': 'raeon', 'view_id': p,
                           'player_role': p, 'private_view': True, 'operations': list(self.manifest['operations'])}
                        for p in ['player_1', 'player_2']}
        self.package = {'path': PACKAGE, 'sha256': file_hash(ROOT / PACKAGE)}
        self.boot = self.horizon.boot(trusted_context={'instance_identity': identity,
                                                      'conformance_grant_issuer': self.capability})
        self.realization = self.horizon.realize_application(self.package, self.owner)
        self.bridge = None
        self.serial = self.grant_serial = 0
        self.connect()

    @staticmethod
    def neutral():
        return [f'FG-{i:03d}' for i in range(1, 31) for _ in range(2)]

    def request(self, operation, arguments=None, player='player_1', effect=None, request_id=None):
        arguments = copy.deepcopy(arguments or {})
        self.grant_serial += 1
        source = (ROOT / 'game/core/raeon/application' / self.manifest['operations'][operation]['source']).read_text()
        line = next(line for line in source.splitlines() if 'admit match' in line)
        spec = json.loads(line.split('@', 1)[1])['action']
        scope = {'application': 'raeon', 'match': self.horizon.identity,
                 'actor': self.players[player]['actor'], 'owner': player, 'operation': operation,
                 'expected_revision': self.horizon._state['revision'], 'arguments': arguments}
        grant = self.horizon.install_conformance_grant(self.capability, scope,
                    dict({'source': spec['effect_source']}, **(effect or {})), 'grant-' + str(self.grant_serial))
        return {'request_id': request_id or 'request-' + str(self.grant_serial), 'operation': operation,
                'arguments': dict(arguments, grant=grant), 'expected_revision': scope['expected_revision']}

    def perform(self, operation, arguments=None, player='player_1', effect=None, request_id=None):
        request = self.request(operation, arguments, player, effect, request_id)
        messages = [port_decode(frame) for frame in self.send(player, 'INTENT', request)]
        if not messages or messages[0]['kind'] != 'RECEIPT':
            raise AssertionError(messages)
        return request, messages

    def initialize(self, roster=None, player='player_1'):
        return self.perform('INITIALIZE_INVENTORY', {'roster': roster or self.neutral()}, player)

    def members(self, container):
        return list(self.horizon._backend.application_values['collections'][container]['members'])
