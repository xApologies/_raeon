"""Native Pass-2 behavior through the real byte fence; no mock card engine."""
import copy
import json
import unittest

from pass_02_support import CardFixture
from support import port_decode


class Pass02(unittest.TestCase):
    def setUp(self):
        self.f = CardFixture()
        self.h = self.f.horizon

    def tearDown(self):
        self.f.close()

    def test_empty_baseline_and_native_inventory(self):
        self.assertEqual(len(self.h._backend.bindings) - 5, 37)
        self.assertEqual(len(self.h._backend.relations) - 3, 163)
        self.assertEqual(self.h._state['revision'], 0)
        self.f.initialize()
        self.f.initialize(player='player_2')
        state = self.h._backend.application_values
        self.assertEqual(len(state['cards']), 120)
        self.assertEqual(len(set(state['cards'])), 120)
        self.assertEqual(len(self.f.members('player_1_deck')), 60)
        self.assertEqual(len(self.f.members('player_2_deck')), 60)
        self.assertEqual(len(self.h._backend.bindings) - 5, 157)
        self.h._backend.collections.validate()

    def test_actual_draw_and_commit_preserve_identity(self):
        self.f.initialize()
        identity = self.f.members('player_1_deck')[0]
        old = copy.deepcopy(self.h._backend.application_values['cards'][identity])
        self.f.perform('DRAW_ONE')
        self.assertEqual(self.f.members('player_1_hand'), [identity])
        self.f.perform('COMMIT_FG', {'cards': [identity], 'destination': 'player_1_config_A'})
        card = self.h._backend.application_values['cards'][identity]
        self.assertEqual(card['id'], old['id'])
        self.assertEqual(len(card['history']), 3)
        self.assertEqual(len({h['version'] for h in card['history']}), 3)
        self.assertEqual(self.f.members('player_1_hand'), [])
        self.assertEqual(self.f.members('player_1_config_A'), [identity])
        self.assertEqual(self.h._view(self.f.players['player_1'])['objects']['player_1_config_A']['fields']['state'], 'CONFIGURING')
        road = self.h._backend.road_history[-7]
        self.assertEqual(road['status'], 'CLOSED')


if __name__ == '__main__':
    unittest.main()
