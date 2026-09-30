"""Admitted state transitions, refusal atomicity, visibility, and replay."""
import copy
import hashlib
import json
import unittest

from pass_02_support import CardFixture
from support import port_decode
from raeon_genesis_horizon.toolchain import digest, canonical
from raeon_genesis_horizon.adapter import HorizonError


class Transactions(unittest.TestCase):
    def setUp(self):
        self.f = CardFixture()
        self.h = self.f.horizon

    def tearDown(self):
        self.f.close()

    def rejected(self, operation, arguments=None, player='player_1', effect=None, alter=None):
        request = self.f.request(operation, arguments, player, effect)
        if alter:
            alter(request)
        before = copy.deepcopy(self.h._record())
        root, revision = self.h._state['root'], self.h._state['revision']
        # Direct owner boundary preserves typed failure; successful scenarios use byte fence.
        with self.assertRaises(Exception):
            self.h.execute(request, self.f.players[player])
        self.assertEqual(self.h._record(), before)
        self.assertEqual(self.h._state['root'], root)
        self.assertEqual(self.h._state['revision'], revision)
        self.assertEqual(self.h._semantic_root(self.h._state), root)
        return request

    def test_catalog_roster_limits_unknown_and_no_reset(self):
        records = self.h._backend.collections.catalog['records']
        self.assertEqual(len(records), 185)
        utility = next(k for k, r in records.items() if r['category'] == 'Utility')
        prime = next(k for k, r in records.items() if r['category'] == 'Prime')
        for extra in [['FG-001'] * 3, [utility] * 4, [prime] * 2, ['NO-CARD']]:
            roster = self.f.neutral()
            roster[-len(extra):] = extra
            self.rejected('INITIALIZE_INVENTORY', {'roster': roster})
        self.rejected('INITIALIZE_INVENTORY', {'roster': self.f.neutral()[:-1]})
        roster = self.f.neutral()
        roster[-4:] = [utility, utility, utility, prime]
        self.f.initialize(roster)
        self.rejected('INITIALIZE_INVENTORY', {'roster': self.f.neutral()})
        self.assertEqual(len(self.h._backend.application_values['cards']), 60)

    def test_shuffle_independent_full_vector_and_idempotency(self):
        self.f.initialize()
        before = self.f.members('player_1_deck')
        seed = 'trusted-private-seed-pass02'
        # Independent index oracle: no runtime implementation imported.
        indexes = list(range(60))
        counter = 0
        for i in range(59, 0, -1):
            width = i + 1
            while True:
                payload = json.dumps(['sha256-counter-fisher-yates-rejection-v1', seed, counter], separators=(',', ':')).encode()
                value = int.from_bytes(hashlib.sha256(payload).digest(), 'big')
                counter += 1
                if value < (1 << 256) // width * width:
                    break
            index = value % width
            indexes[i], indexes[index] = indexes[index], indexes[i]
        request, messages = self.f.perform('SHUFFLE_DECK', effect={'seed': seed})
        self.assertEqual(self.f.members('player_1_deck'), [before[i] for i in indexes])
        self.assertEqual(self.h._backend.application_values['rng']['player_1_deck']['counter'], 59)
        after = copy.deepcopy(self.h._record())
        again = self.h.execute(request, self.f.players['player_1'])
        self.assertEqual(again, messages[0]['payload'])
        self.assertEqual(self.h._record(), after)
        leaked = json.dumps(self.h._view(self.f.players['player_1'])) + json.dumps(messages)
        self.assertNotIn(seed, leaked)
        self.assertTrue(all(identity not in leaked for identity in before))
        self.rejected('SHUFFLE_DECK', effect={'seed': 'changed-private-seed'})

    def test_hand_capacity_empty_deck_and_forged_arguments(self):
        self.rejected('DRAW_ONE')
        self.f.initialize()
        for _ in range(7):
            self.f.perform('DRAW_ONE')
        self.rejected('DRAW_ONE')
        self.assertEqual(len(self.f.members('player_1_deck')), 53)
        self.rejected('DRAW_ONE', alter=lambda r: r['arguments'].update(top='fake'))
        self.rejected('DRAW_ONE', alter=lambda r: r['arguments'].update(grant='client-grant'))
        self.rejected('DRAW_ONE', alter=lambda r: r.update(expected_revision=False))

    def test_failed_candidate_rolls_back_grant_rng_membership(self):
        self.f.initialize()
        for point in ['after_removal', 'after_candidate', 'before_publish']:
            request = self.f.request('DRAW_ONE')
            before = copy.deepcopy(self.h._record())
            state = copy.deepcopy(self.h._state)
            def fail(actual, expected=point):
                if actual == expected:
                    raise RuntimeError('injected-' + expected)
            self.h.fault_hook = fail
            with self.assertRaisesRegex(RuntimeError, 'injected'):
                self.h.execute(request, self.f.players['player_1'])
            self.assertEqual(self.h._record(), before)
            self.assertEqual(self.h._state, state)
            self.h.fault_hook = lambda _: None
            self.h.execute(request, self.f.players['player_1'])
        request = self.f.request('SHUFFLE_DECK', effect={'seed': 'private-seed-for-rollback'})
        before = copy.deepcopy(self.h._record())
        self.h.fault_hook = lambda p: (_ for _ in ()).throw(RuntimeError('rollback')) if p == 'before_publish' else None
        with self.assertRaisesRegex(RuntimeError, 'rollback'):
            self.h.execute(request, self.f.players['player_1'])
        self.assertEqual(self.h._record(), before)

    def test_delivery_loss_retry_conflict_and_stale_revision(self):
        self.f.initialize()
        request = self.f.request('DRAW_ONE')
        self.h.fault_hook = lambda p: (_ for _ in ()).throw(RuntimeError('delivery')) if p == 'after_commit' else None
        with self.assertRaisesRegex(RuntimeError, 'delivery'):
            self.h.execute(request, self.f.players['player_1'])
        self.h.fault_hook = lambda _: None
        root = self.h._state['root']
        self.assertEqual(self.h.execute(request, self.f.players['player_1'])['root'], root)
        conflicting = copy.deepcopy(request)
        conflicting['arguments']['grant'] = 'changed'
        with self.assertRaisesRegex(HorizonError, 'REQUEST_ID_CONFLICT'):
            self.h.execute(conflicting, self.f.players['player_1'])
        self.rejected('DRAW_ONE', alter=lambda r: r.update(expected_revision=r['expected_revision'] - 1))
        self.assertEqual(len(self.f.members('player_1_hand')), 1)

    def test_live_private_views_and_detached_values(self):
        self.f.initialize()
        self.f.initialize(player='player_2')
        self.f.perform('DRAW_ONE')
        identity = self.f.members('player_1_hand')[0]
        own = self.h._view(self.f.players['player_1'])
        other = self.h._view(self.f.players['player_2'])
        self.assertIn(identity, json.dumps(own))
        self.assertNotIn(identity, json.dumps(other))
        for player in self.f.players:
            text = json.dumps(self.h._view(self.f.players[player]))
            self.assertTrue(all(i not in text for i in self.f.members(player + '_deck')))
        own['objects']['player_1_hand']['fields']['contents'].clear()
        self.assertEqual(self.f.members('player_1_hand'), [identity])
        self.f.perform('RETIRE_CARDS', {'cards': [identity]})
        self.assertNotIn(identity, json.dumps(self.h._view(self.f.players['player_1'])))
        self.f.perform('INSPECT_TOP', {'source': 'player_1_graveyard', 'count': 1})
        self.assertEqual(self.h._view(self.f.players['player_1'])['inspection'][0]['identity'], identity)
        self.assertNotIn(identity, json.dumps(self.h._view(self.f.players['player_2'])))

    def test_dynamic_regions_native_capacity_and_repeat_color(self):
        initial = {k: v['identity'] for k, v in self.h._view(self.f.players['player_1'])['objects'].items()}
        self.f.initialize()
        for rank, capacity in [('Red', 3), ('Orange', 4), ('Yellow', 5), ('Green', 6), ('Blue', 7), ('Violet', 8)]:
            self.f.perform('ADD_CONFIGURATION_SPACE', {'rank': rank}, effect={'variant': rank})
            members = self.f.members('player_1_configuration')
            self.assertEqual(self.h._backend.application_values['collections'][members[-1]]['capacity'], capacity)
        self.assertEqual(len(self.f.members('player_1_configuration')), 9)
        self.rejected('ADD_CONFIGURATION_SPACE', {'rank': 'Red'}, effect={'variant': 'Red'})
        self.f.perform('ADD_CONFIGURATION_SPACE', {'rank': 'Red'}, 'player_2', effect={'variant': 'Red'})
        self.f.perform('ADD_CONFIGURATION_SPACE', {'rank': 'Red'}, 'player_2', effect={'variant': 'Red'})
        for name, identity in initial.items():
            self.assertEqual(self.h._view(self.f.players['player_1'])['objects'][name]['identity'], identity)
        red = self.f.members('player_1_configuration')[3]
        for _ in range(3):
            self.f.perform('DRAW_ONE')
            card = self.f.members('player_1_hand')[0]
            self.f.perform('COMMIT_FG', {'cards': [card], 'destination': red})
        self.f.perform('DRAW_ONE')
        self.rejected('COMMIT_FG', {'cards': self.f.members('player_1_hand'), 'destination': red})
        self.rejected('ADD_CONFIGURATION_SPACE', {'rank': 'Blue'}, 'player_2', effect={'variant': 'Red'})

    def test_retirement_recovery_order_and_whole_support(self):
        self.f.initialize()
        for _ in range(4):
            self.f.perform('DRAW_ONE')
        selected = self.f.members('player_1_hand')
        self.f.perform('RETIRE_CARDS', {'cards': selected[:3]})
        self.f.perform('RETIRE_CARDS', {'cards': selected[3:]})
        self.assertEqual(self.f.members('player_1_graveyard'), selected[3:] + selected[:3])
        deck_before = self.f.members('player_1_deck')
        ordered = [selected[2], selected[0], selected[3]]
        self.f.perform('RECOVER_6', {'cards': ordered})
        self.assertEqual(self.f.members('player_1_deck'), ordered + deck_before)
        self.assertEqual(self.f.members('player_1_graveyard'), [selected[1]])
        self.f.perform('RECOVER_1', {'cards': [selected[1]]})
        self.f.perform('COMMIT_FG', {'cards': [selected[1]], 'destination': 'player_1_config_A'})
        self.f.perform('DRAW_ONE')
        identity = self.f.members('player_1_hand')[0]
        self.f.perform('COMMIT_FG', {'cards': [identity], 'destination': 'player_1_config_A'})
        self.rejected('RETIRE_CARDS', {'cards': [identity]})
        self.rejected('RETIRE_SUPPORT', {'cards': [identity]})
        self.f.perform('RETIRE_SUPPORT', {'cards': [identity, selected[1]]})
        self.rejected('RECOVER_6', {'cards': [identity, identity]})
        self.rejected('RECOVER_4', {'cards': [identity]})
        self.assertEqual(self.f.members('player_1_config_A'), [])

    def test_structural_prime_slots_without_combat(self):
        records = self.h._backend.collections.catalog['records']
        primes = [k for k, r in records.items() if r['category'] == 'Prime'][:4]
        roster = self.f.neutral()
        roster[:4] = primes
        self.f.initialize(roster)
        cards = self.f.members('player_1_deck')[:4]
        for i in range(3):
            self.f.perform('BIND_PRIME', {'cards': [cards[i]], 'destination': 'player_1_prime_' + str(i+1)})
        self.rejected('BIND_PRIME', {'cards': cards[3:], 'destination': 'player_1_prime_1'})
        self.rejected('BIND_PRIME', {'cards': cards[3:], 'destination': 'player_1_prime_4'})
        self.rejected('BIND_PRIME', {'cards': cards[3:], 'destination': 'player_2_prime_1'})
        self.rejected('RETIRE_CARDS', {'cards': cards[:1]})
        self.f.perform('DRAW_ONE')
        self.rejected('RETIRE_CARDS', {'cards': cards[3:]})
        for i in range(3):
            fields = self.h._view(self.f.players['player_1'])['objects']['player_1_prime_' + str(i+1)]['fields']
            self.assertEqual(fields['occupant'], cards[i])
            self.assertNotIn('H', fields)
            self.assertNotIn('C', fields)

    def test_checkpoint_nonempty_preserves_native_state_and_retry(self):
        self.f.initialize()
        request, _ = self.f.perform('SHUFFLE_DECK', effect={'seed': 'checkpoint-private-seed'})
        for _ in range(6):
            self.f.perform('ADD_CONFIGURATION_SPACE', {'rank': 'Red'}, effect={'variant': 'Red'})
        state = copy.deepcopy(self.h._backend.application_values)
        result = self.f.restart()
        self.h = self.f.horizon
        self.assertEqual(self.h._backend.application_values, state)
        self.assertEqual(self.h.execute(request, self.f.players['player_1'])['status'], 'COMMITTED')
        self.assertTrue(result['views_equal'])


if __name__ == '__main__':
    unittest.main()
