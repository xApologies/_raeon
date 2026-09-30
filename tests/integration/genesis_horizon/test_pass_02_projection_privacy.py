"""Vera V-P2-01: real RAEON/Genesis/Horizon projections across the byte fence.

These eight additive regressions do not replace the original acceptance cases.
"""
import copy
import json
import unittest

from pass_02_support import CardFixture
from support import Port
from raeon_genesis_horizon.adapter import HorizonError


class ProjectionPrivacy(unittest.TestCase):
    def setUp(self):
        self.f = CardFixture()
        self.h = self.f.horizon
        for owner in ('player_1', 'player_2'):
            self.f.initialize(player=owner)
            self.f.perform('DRAW_ONE', player=owner)

    def tearDown(self):
        self.f.close()

    def bind(self, owner, view='public', private=False, actor=None):
        authority = dict(self.f.players[owner], view_id=view, private_view=private)
        if actor is not None:
            authority['actor'] = actor
        name = 'session-' + str(len(self.f.players))
        self.f.players[name] = authority
        self.f.handles[name] = self.f.bridge.bind_session(authority)
        return name

    def read(self, name, kind='HELLO', port=None):
        """Observation must preserve semantic state, including private grant data."""
        before = copy.deepcopy(self.h._state)
        values = copy.deepcopy(self.h._backend.application_values)
        port = port or Port()
        payload = {'protocol': 2} if kind == 'HELLO' else {'view_id': port.view_id, 'revision': port.revision}
        frames = self.f.send(name, kind, payload)
        messages = [port.accept(frame) for frame in frames]
        self.assertEqual(self.h._state, before)
        self.assertEqual(self.h._backend.application_values, values)
        self.assertEqual(self.h._semantic_root(self.h._state), before['root'])
        self.assertTrue(messages)
        self.assertTrue(all(m['kind'] in ('WELCOME', 'SNAPSHOT', 'DELTA') for m in messages))
        return port, messages

    def hidden_hands(self, view, messages, except_owner=None):
        text = json.dumps(messages)
        for owner in ('player_1', 'player_2'):
            fields = view['objects'][owner + '_hand']['fields']
            members = self.f.members(owner + '_hand')
            self.assertEqual(fields['count'], len(members))
            if owner == except_owner:
                self.assertEqual(fields['contents'], members)
            else:
                self.assertNotIn('contents', fields)
                self.assertNotIn('order', fields)
                self.assertFalse(any(i in text for i in members), 'hidden Hand identity in wire payload')
                self.assertFalse(any(i in view['objects'] for i in members))

    def private_edges(self, view, owner=None):
        edges = [e for e in view['relations'] if e['relation'] == 'private_to']
        if owner is None:
            self.assertEqual(edges, [], 'public projection restored private_to edges')
        else:
            self.assertTrue(edges, 'owner private metadata must remain available')
            self.assertTrue(all(e['target'] == view['objects'][owner]['identity'] for e in edges))

    def test_audited_public_view_cannot_inherit_private_hand(self):
        for owner in ('player_1', 'player_2'):
            with self.subTest(owner=owner):
                session = self.bind(owner, private=True)
                port, messages = self.read(session)
                self.hidden_hands(port.view, messages)
                port, messages = self.read(session, 'SYNC_REQUEST', port)
                self.hidden_hands(port.view, messages)

    def test_audited_same_actor_public_cannot_inherit_inspection(self):
        for owner in ('player_1', 'player_2'):
            with self.subTest(owner=owner):
                self.f.perform('INSPECT_TOP', {'source': owner + '_deck', 'count': 2}, owner)
                inspected = self.f.members(owner + '_deck')[:2]
                own, _ = self.read(owner)
                self.assertEqual([i['identity'] for i in own.view['inspection']], inspected)
                session = self.bind(owner, private=False)
                port, messages = self.read(session)
                self.assertNotIn('inspection', port.view)
                self.assertFalse(any(i in json.dumps(messages) for i in inspected))
                self.read(session, 'SYNC_REQUEST', port)
                self.f.bridge.close_session(self.f.handles[session])
                self.f.handles[session] = self.f.bridge.bind_session(self.f.players[session])
                again, messages = self.read(session)
                self.assertNotIn('inspection', again.view)
                self.assertFalse(any(i in json.dumps(messages) for i in inspected))

    def test_audited_live_merge_cannot_restore_private_relations(self):
        for owner in ('player_1', 'player_2'):
            with self.subTest(owner=owner):
                port, _ = self.read(self.bind(owner))
                self.private_edges(port.view)
                own, _ = self.read(owner)
                self.private_edges(own.view, owner)

    def test_owner_opponent_and_public_controls(self):
        for owner in ('player_1', 'player_2'):
            own, messages = self.read(owner)
            self.hidden_hands(own.view, messages, except_owner=owner)
            self.private_edges(own.view, owner)
            public, messages = self.read(self.bind(owner))
            self.hidden_hands(public.view, messages)
            self.assertNotIn('inspection', public.view)
            for player in ('player_1', 'player_2'):
                self.assertFalse(any(i in json.dumps(messages) for i in self.f.members(player + '_deck')))

    def test_public_live_geometry_delta_and_reconnect(self):
        for owner in ('player_1', 'player_2'):
            session = self.bind(owner, private=True)
            port, _ = self.read(session)
            card = self.f.members(owner + '_hand')[0]
            self.f.perform('ADD_CONFIGURATION_SPACE', {'rank': 'Red'}, owner, effect={'variant': 'Red'})
            space = self.f.members(owner + '_configuration')[-1]
            self.f.perform('COMMIT_FG', {'cards': [card], 'destination': space}, owner)
            self.f.perform('DRAW_ONE', player=owner)
            port, messages = self.read(session, 'SYNC_REQUEST', port)
            self.assertEqual([m['kind'] for m in messages], ['DELTA'])
            self.assertEqual(port.view['objects'][space]['fields']['contents'], [card])
            self.assertEqual(port.view['objects'][card]['fields']['location'], space)
            self.assertTrue(any(e['relation'] == 'contains' and e['target'] == card for e in port.view['relations']))
            self.hidden_hands(port.view, messages)
            self.private_edges(port.view)
            self.f.bridge.close_session(self.f.handles[session])
            self.f.handles[session] = self.f.bridge.bind_session(self.f.players[session])
            again, messages = self.read(session)
            self.assertEqual(again.view, port.view)
            self.hidden_hands(again.view, messages)

    def test_private_inspection_delta_reconnect_restore_and_expiry(self):
        for owner in ('player_1', 'player_2'):
            own, _ = self.read(owner)
            public_session = self.bind(owner)
            public, _ = self.read(public_session)
            request = self.f.request('INSPECT_TOP', {'source': owner + '_deck', 'count': 2}, owner)
            frames = self.f.send(owner, 'INTENT', request)
            messages = [own.accept(frame) for frame in frames]
            self.assertEqual([m['kind'] for m in messages], ['RECEIPT', 'DELTA'])
            expected = copy.deepcopy(own.view['inspection'])
            self.assertEqual([i['identity'] for i in expected], self.f.members(owner + '_deck')[:2])
            public, messages = self.read(public_session, 'SYNC_REQUEST', public)
            self.assertNotIn('inspection', public.view)
            self.assertFalse(any(i['identity'] in json.dumps(messages) for i in expected))
            self.f.bridge.close_session(self.f.handles[owner])
            self.f.handles[owner] = self.f.bridge.bind_session(self.f.players[owner])
            own, _ = self.read(owner)
            self.assertEqual(own.view['inspection'], expected)
            checkpoint = self.f.bridge.save_checkpoint(self.f.owner)
            state, epoch = copy.deepcopy(self.h._state), self.h.epoch
            self.f.bridge.restore_checkpoint(checkpoint, self.f.owner)
            self.assertEqual(self.h._state, state)
            self.assertNotEqual(self.h.epoch, epoch)
            own, _ = self.read(owner)
            self.assertEqual(own.view['inspection'], expected)
            self.assertNotIn('inspection', self.read(public_session)[0].view)
            # Public structural change advances the semantic revision without revealing the inspected cards.
            self.f.perform('ADD_CONFIGURATION_SPACE', {'rank': 'Blue'}, owner, effect={'variant': 'Blue'})
            own, messages = self.read(owner, 'SYNC_REQUEST', own)
            self.assertEqual([m['kind'] for m in messages], ['DELTA'])
            self.assertNotIn('inspection', own.view)
            self.assertFalse(any(i['identity'] in json.dumps(messages) for i in expected))

    def test_inspection_scope_includes_application_view_owner_and_actor(self):
        for owner, opponent in [('player_1', 'player_2'), ('player_2', 'player_1')]:
            self.f.perform('INSPECT_TOP', {'source': owner + '_deck', 'count': 1}, owner)
            actor = self.f.players[owner]['actor']
            record = self.h._backend.application_values['inspections'][actor]
            self.assertEqual(record['scope'], {'application_id': 'raeon', 'view_id': owner, 'owner': owner})
            other_role = self.bind(opponent, view=opponent, private=True, actor=actor)
            self.assertNotIn('inspection', self.read(other_role)[0].view)
            other_actor = self.bind(owner, view=owner, private=True, actor='another-trusted-actor')
            self.assertNotIn('inspection', self.read(other_actor)[0].view)
            for changes in [{'application_id': 'unrelated'}, {'private_view': False}, {'view_id': opponent}]:
                authority = dict(self.f.players[owner], **changes)
                before = copy.deepcopy(self.h._record())
                with self.assertRaisesRegex(HorizonError, 'AUTHORITY_DENIED'):
                    self.h.observe(authority)
                self.assertEqual(self.h._record(), before)

    def test_public_inspect_admission_rejected_atomically(self):
        for owner in ('player_1', 'player_2'):
            request = self.f.request('INSPECT_TOP', {'source': owner + '_deck', 'count': 1}, owner)
            before = copy.deepcopy(self.h._record())
            with self.assertRaisesRegex(HorizonError, 'ADMISSION_REJECTED'):
                self.h.execute(request, dict(self.f.players[owner], view_id='public'))
            self.assertEqual(self.h._record(), before)
            self.assertEqual(self.h.execute(request, self.f.players[owner])['status'], 'COMMITTED')


if __name__ == '__main__':
    unittest.main()
