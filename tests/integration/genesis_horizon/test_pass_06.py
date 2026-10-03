"""Executed Genesis headless matches and explicit Pass-06 boundary regressions."""
import copy
import json
import unittest

from pass_06_support import HeadlessFixture,DRAW,RECOVERY,TRANSDUCTION,WHITE
from raeon_genesis_horizon.adapter import HorizonError


class Pass06(unittest.TestCase):
    def setUp(self):
        self.f=HeadlessFixture();self.h=self.f.horizon

    def tearDown(self):self.f.close()

    def refuse(self,op,args=None,player='player_1',effect=None):
        request=self.f.request(op,args,player,effect);before=self.f.snapshot()
        with self.assertRaises(HorizonError) as raised:self.h.execute(request,self.f.players[player])
        self.assertEqual(raised.exception.code,'ADMISSION_REJECTED')
        self.assertEqual(self.f.snapshot(),before)

    def begin(self,utilities=(),enemy_utilities=(),manifolds=(),enemy_manifolds=()):
        a=self.f.setup_player(utilities=utilities,manifolds=manifolds)
        b=self.f.setup_player('player_2',utilities=enemy_utilities,manifolds=enemy_manifolds)
        self.f.setup();self.f.keep();self.f.start()
        return a,b

    def test_mulligan_zero_seven_repeat_replay_and_privacy(self):
        f=self.f;f.setup_player();f.setup_player('player_2');f.setup()
        self.assertTrue(all(f.tempo.state['mulligan_pending'].values()))
        self.refuse('P6_BEGIN_TURN',effect={'policy':'TRUSTED_MATCH_CONTROL'})
        original={p:f.members(p+'_hand') for p in ('player_1','player_2')}
        before=set(f.members('player_1_deck')+original['player_1'])
        f.mulligan([],seed='pass06-mulligan-zero-seed')
        self.assertEqual(f.members('player_1_hand'),original['player_1'])
        self.assertEqual(set(f.members('player_1_hand')+f.members('player_1_deck')),before)
        f.mulligan(original['player_2'],'player_2',seed='pass06-mulligan-seven-seed')
        self.assertEqual(len(f.members('player_2_hand')),7)
        history=f.tempo.state['history']
        self.assertEqual([r['event'] for r in history[-3:]],['MULLIGAN_RETURNED','MULLIGAN_SHUFFLED','MULLIGAN_REDRAWN'])
        self.assertEqual((history[-3]['count'],history[-1]['count'],history[-1]['penalty']),(7,7,0))
        cards=self.h._backend.application_values['cards']
        for identity in original['player_2']:self.assertTrue(any(v['from']=='player_2_hand' and v['to']=='player_2_deck' for v in cards[identity]['history']))
        self.refuse('P6_MULLIGAN',{'cards':[]},effect={'policy':'TRUSTED_MULLIGAN_SHUFFLE','seed':'pass06-mulligan-repeat'})
        f.start();state=copy.deepcopy(self.h._backend.application_values);f.restart();self.h=f.horizon
        self.assertEqual(self.h._backend.application_values,state)
        view=self.h._view(f.players['player_1']);public=self.h._view(dict(f.players['player_1'],view_id='public'))
        for identity in f.members('player_2_hand')+f.members('player_1_deck')+f.members('player_2_deck'):
            self.assertNotIn(identity,json.dumps(view));self.assertNotIn(identity,json.dumps(public))
        self.assertEqual(view['objects']['match']['fields']['mulligan_procedure'],'RETURN_TO_DECK_SHUFFLE_REDRAW_SAME_COUNT')

    def test_draw_capacity_order_and_compensation_own_active_single_use(self):
        f=self.f;self.begin([DRAW+'0',DRAW+'1',DRAW+'2'],[DRAW+'2'])
        cards=[f.utility(DRAW+str(n)) for n in range(3)]
        before=f.members('player_1_deck');grave=f.members('player_1_graveyard')
        f.play(cards[2]);self.assertEqual(len(f.members('player_1_hand')),10)
        self.assertEqual(f.members('player_1_deck'),before[2:]);self.assertEqual(f.members('player_1_graveyard'),grave)
        before=f.members('player_1_deck')
        for card in cards:f.play(card)
        self.assertEqual(f.members('player_1_deck'),before)
        self.assertEqual(f.tempo.state['failed_normal_draws']['player_1'],0)
        fg=[i for i in f.members('player_1_hand') if self.h._backend.application_values['cards'][i]['category']=='Field Generator'][:3]
        for identity in fg:f.perform('COMMIT_FG',{'cards':[identity],'destination':'player_1_config_A'})
        before=f.members('player_1_deck');f.play(cards[2])
        self.assertEqual(f.members('player_1_deck'),before[3:]);self.assertEqual(len(f.members('player_1_hand')),10)
        obj=f.tempo.state['compensation'];args={'object':obj['id']}
        self.refuse('P6_USE_COMPENSATION',args,'player_2',f.effect(obj['id']))
        f.next_turn();self.assertEqual(f.tempo.state['phase'],'ACTIVE')
        draw=f.utility(DRAW+'2','player_2');f.play(draw,player='player_2')
        self.assertEqual(self.h._view(f.players['player_2'])['objects']['player_2_hand']['fields']['count'],10)
        before=f.members('player_2_deck')
        f.perform('P6_USE_COMPENSATION',args,'player_2',effect=f.effect(obj['id']))
        self.assertEqual(len(f.members('player_2_hand')),10);self.assertEqual(f.members('player_2_deck'),before[1:])
        self.assertTrue(f.tempo.state['compensation']['consumed'])
        self.refuse('P6_USE_COMPENSATION',args,'player_2',f.effect(obj['id']))
        self.refuse('EFFECT_DRAW',{'utility':draw},'player_2',f.effect(draw))
        before=f.members('player_1_deck');f.next_turn();self.assertEqual(f.members('player_1_deck'),before)
        self.assertEqual(len(f.members('player_1_hand')),10)

    def test_complete_prime_match_deterministic_replay_restart_and_terminal(self):
        from pass_06_matches import prime_match
        f=self.f;record=prime_match(f,checkpoint_last=True);self.h=f.horizon
        self.assertTrue(record['all_road_audits']);self.assertGreater(record['road_count'],0)
        other=HeadlessFixture()
        try:
            replay=prime_match(other)
            self.assertEqual(record['root'],replay['root'])
            self.assertEqual(f.horizon._backend.application_values,other.horizon._backend.application_values)
            self.assertEqual(f.horizon._backend.transport_record(),other.horizon._backend.transport_record())
            self.assertEqual(record['history'],replay['history'])
            before=other.snapshot();request=other.request('P6_NORMAL_DRAW',player='player_2',effect={'policy':'TRUSTED_MATCH_CONTROL'})
            before=other.snapshot()
            with self.assertRaises(HorizonError):other.horizon.execute(request,other.players['player_2'])
            self.assertEqual(other.snapshot(),before)
        finally:other.close()

    def test_complete_exhaustion_match_stages_order_defense_and_terminal(self):
        from pass_06_matches import exhaustion_match
        record=exhaustion_match(self.f)
        self.assertTrue(record['all_road_audits'])
        stages=record['stages'];self.assertGreaterEqual(len(stages),10)
        self.assertTrue(all(s['target']==stages[0]['target'] for s in stages[:8]))
        self.assertEqual([s['slot'][-1] for s in stages[-3:]],['1','2','3'])
        self.assertEqual(self.f.tempo.state['pending_failed_draws'],[])
        self.assertFalse(self.f.tempo.defense_open)
        values=copy.deepcopy(self.h._backend.application_values)
        self.f.close();self.f=HeadlessFixture();self.h=self.f.horizon
        replay=exhaustion_match(self.f)
        self.assertEqual(record['root'],replay['root']);self.assertEqual(record['stages'],replay['stages'])
        self.assertEqual(self.h._backend.application_values,values)
        self.refuse('P6_NORMAL_DRAW',effect={'policy':'TRUSTED_MATCH_CONTROL'})

    def test_transduction_restore_six_native_amounts(self):
        f=self.f;(primes,_),_=self.begin([TRANSDUCTION+'restore/'+str(n) for n in range(6)])
        card=f.utility(TRANSDUCTION+'restore/0')
        self.refuse('P6_UTILITY',dict(f.utility_args(card,target=primes[0],direction='RESTORE'),target_kind='field'),effect=f.effect(card))
        expected=0
        for n in range(6):
            card=f.utility(TRANSDUCTION+'restore/'+str(n));before=len(f.color.state['history'])
            f.play(card,target=primes[0],direction='RESTORE');expected+=n+1
            self.assertEqual(f.q(primes[0]),expected)
            self.assertEqual(len(f.color.state['history']),before+1)
            self.assertTrue(f.color.audit_road(self.h._backend.road_history[f.color.state['history'][-1]['road_index']])['pass'])
            self.assertEqual(f.color.state['history'][-1]['amount'],n+1)
        self.refuse('P6_UTILITY',f.utility_args(card,target=primes[0],direction='DEGRADE'),effect=f.effect(card))

    def test_transduction_degrade_six_native_amounts_and_zero_cost(self):
        f=self.f;_,(enemy,_)=self.begin([TRANSDUCTION+'degrade/'+str(n) for n in range(6)])
        targets=[enemy[0]]*3+[enemy[1],enemy[2],enemy[1]]
        for n,target in enumerate(targets):
            card=f.utility(TRANSDUCTION+'degrade/'+str(n));old=copy.deepcopy(f.color.state['primes'][target])
            f.play(card,target=target,direction='DEGRADE')
            self.assertEqual(f.color.state['primes'][target]['H'],max(0,old['H']-n-1))
            self.assertEqual(f.color.state['history'][-1]['amount'],n+1)
            if f.tempo.defense_open:f.pass_defense()
        self.assertFalse(any(k in f.tempo.state for k in ('mana','energy','action_points')))

    def test_transduction_universal_six_both_resolution_choices(self):
        f=self.f;(primes,_),(enemy,_)=self.begin([TRANSDUCTION+'universal/'+str(n) for n in range(6)])
        for n in range(6):
            card=f.utility(TRANSDUCTION+'universal/'+str(n));old=f.q(primes[0])
            f.play(card,target=primes[0],direction='RESTORE');self.assertEqual(f.q(primes[0]),old+n+1)
            target=enemy[0] if n<3 else enemy[1] if n in (3,5) else enemy[2]
            f.play(card,target=target,direction='DEGRADE');self.assertEqual(f.color.state['history'][-1]['direction'],'DEGRADE')
            self.assertEqual(f.color.state['history'][-1]['amount'],n+1)
            if f.tempo.defense_open:f.pass_defense()

    def test_draw_deck_survey_selection_open_boundary_exchange_and_deep_survey(self):
        f=self.f;self.begin([DRAW+str(n) for n in (0,1,3,4,5,6)])
        draw1,draw2,survey,select,exchange,deep=[f.utility(DRAW+str(n)) for n in (0,1,3,4,5,6)]
        before=f.members('player_1_deck');f.play(draw1)
        self.assertEqual(f.members('player_1_deck'),before[1:])
        # Commit ordinary Hand FGs through the established configuration law.
        cards=self.h._backend.application_values['cards']
        for identity in [i for i in f.members('player_1_hand') if cards[i]['category']=='Field Generator'][:2]:
            f.perform('COMMIT_FG',{'cards':[identity],'destination':'player_1_config_A'})
        before=f.members('player_1_deck');f.play(draw2)
        self.assertEqual(f.members('player_1_deck'),before[2:])
        f.look(survey);inspection=self.h._view(f.players['player_1'])['inspection']
        self.assertEqual([row['identity'] for row in inspection],f.members('player_1_deck')[:3])
        for authority in [f.players['player_2'],dict(f.players['player_1'],view_id='public')]:self.assertNotIn('inspection',self.h._view(authority))
        before=f.members('player_1_deck');order=list(reversed(before[:3]));f.play(survey,order)
        self.assertEqual(f.members('player_1_deck'),order+before[3:])
        before=f.members('player_1_deck');f.play(select,[before[1]])
        self.assertIn(before[1],f.members('player_1_hand'))
        remainder={before[0],before[2]};self.assertEqual(set(f.members('player_1_deck')[-2:]),remainder)
        self.assertEqual(f.tempo.state['unordered_bottom']['player_1'],[sorted(remainder)])
        self.refuse('P6_OPEN_GUARD',{'item':'P6-OPEN-002'})
        self.refuse('P6_UTILITY',f.utility_args(deep,[f.members('player_1_deck')[0]]),effect=dict(f.effect(deep),seed='deep-survey-capacity'))
        fg=next(i for i in f.members('player_1_hand') if cards[i]['category']=='Field Generator')
        f.perform('COMMIT_FG',{'cards':[fg],'destination':'player_1_config_B'})
        f.look(deep);self.assertEqual(len(self.h._view(f.players['player_1'])['inspection']),7)
        before=f.members('player_1_deck');chosen=before[6];f.play(deep,[chosen])
        self.assertEqual(set(f.members('player_1_deck')),set(before)-{chosen})
        self.assertEqual(f.tempo.state['unordered_bottom']['player_1'],[])
        discard=[i for i in f.members('player_1_hand') if cards[i]['category']=='Field Generator'][:2]
        before=f.members('player_1_deck');hand_count=len(f.members('player_1_hand'));f.play(exchange,discard)
        self.assertEqual(f.members('player_1_deck'),before[2:]);self.assertEqual(len(f.members('player_1_hand')),hand_count)
        self.assertTrue(set(discard)<=set(f.members('player_1_graveyard')))
        names=[e['event'] for e in f.tempo.state['history']]
        self.assertEqual(names[-3:],['EXCHANGE_TO_GRAVEYARD','DRAW_RESOLVED','UTILITY_RESOLVED'])

    def test_short_deck_effects_and_unresolved_selection_order_guard(self):
        f=self.f;f.setup_player(utilities=[DRAW+'3',DRAW+'4',DRAW+'5',DRAW+'6']);f.setup_player('player_2')
        # Actual setup transactions, keeping the constructed inventory intact.
        candidates=[i for i in f.members('player_1_deck') if self.h._backend.application_values['cards'][i]['category']=='Field Generator']
        for start in range(0,len(candidates)-5,3):
            group=candidates[start:min(start+3,len(candidates)-5)]
            f.perform('BATCH_TO_HAND',{'cards':group});f.perform('RETIRE_CARDS',{'cards':group})
        f.setup();f.keep();f.start()
        self.assertEqual(len(f.members('player_1_deck')),1)
        survey,select,exchange,deep=[f.utility(DRAW+str(n)) for n in (3,4,5,6)]
        for card in (survey,deep):
            f.look(card);self.assertEqual(len(self.h._view(f.players['player_1'])['inspection']),1)
        before=f.members('player_1_deck');f.play(select,before)
        self.assertEqual(f.members('player_1_deck'),[]);self.assertEqual(f.tempo.state['unordered_bottom']['player_1'],[])
        f.play(survey,[]);f.play(deep,[])
        discard=[i for i in f.members('player_1_hand') if self.h._backend.application_values['cards'][i]['category']=='Field Generator'][:2]
        before=len(f.members('player_1_hand'));f.play(exchange,discard)
        self.assertEqual(len(f.members('player_1_hand')),before-2)
        self.assertEqual(f.tempo.state['failed_normal_draws']['player_1'],2)

    def test_recovery_six_effects_capacity_identity_topology_and_prime_refusal(self):
        f=self.f;primes,_=f.setup_player(utilities=[RECOVERY+str(n) for n in range(6)]+[DRAW+'0']);f.setup_player('player_2')
        cards=self.h._backend.application_values['cards']
        grave=[i for i in f.members('player_1_deck') if cards[i]['category']=='Field Generator'][:6]
        utility=next(i for i in f.members('player_1_deck') if cards[i]['catalog']==DRAW+'0')
        for group in (grave[:3],grave[3:],[utility]):
            f.perform('BATCH_TO_HAND',{'cards':group});f.perform('RETIRE_CARDS',{'cards':group})
        f.setup();f.keep();f.start()
        recovery=[f.utility(RECOVERY+str(n)) for n in range(6)]
        topology=copy.deepcopy(f.ext.state)
        f.play(recovery[0],[grave[0]]);self.assertIn(grave[0],f.members('player_1_hand'))
        self.refuse('P6_UTILITY',f.utility_args(recovery[1],grave[1:3]),effect=f.effect(recovery[1]))
        for i in [v for v in f.members('player_1_hand') if cards[v]['category']=='Field Generator']:
            f.perform('COMMIT_FG',{'cards':[i],'destination':'player_1_config_A'})
        f.play(recovery[1],grave[1:3]);self.assertTrue(set(grave[1:3])<=set(f.members('player_1_hand')))
        for i in grave[1:3]:f.perform('COMMIT_FG',{'cards':[i],'destination':'player_1_config_B'})
        before=copy.deepcopy(f.ext.state['fields']);f.play(recovery[2],grave[3:]);self.assertEqual(f.ext.state['fields'],before)
        for i in grave[3:]:f.perform('COMMIT_FG',{'cards':[i],'destination':'player_1_config_C'})
        f.play(recovery[3],[utility]);self.assertIn(utility,f.members('player_1_hand'))
        self.refuse('P6_UTILITY',f.utility_args(recovery[4],[primes[0]]),effect=f.effect(recovery[4]))
        # Destroy ordinary committed supports with the accepted whole-space retirement.
        group=list(f.members('player_1_config_C'));other=list(f.members('player_1_config_A'))
        f.perform('RETIRE_SUPPORT',{'cards':group});f.perform('RETIRE_SUPPORT',{'cards':other})
        f.play(recovery[4],[other[0]]);self.assertIn(other[0],f.members('player_1_hand'))
        remaining=group;before=f.members('player_1_deck');f.play(recovery[5],list(reversed(remaining)))
        self.assertEqual(f.members('player_1_deck'),list(reversed(remaining))+before)
        self.assertEqual(f.ext.state['fields'],topology['fields'])
        self.assertFalse(any(space['lifecycle']=='RESOLVED' for space in f.ext.state['spaces'].values()))

    def reserved(self,family,pointer,count):
        handles=['source:data/cycles/cycle_01/utilities/'+family+'.json#/values/'+pointer+'/'+str(n) for n in range(count)]
        f=self.f;self.begin(handles)
        for handle in handles:
            card=f.utility(handle)
            self.refuse('P6_UTILITY',f.utility_args(card),effect=f.effect(card))
            self.refuse('P6_LOOK_UTILITY',{'utility':card},effect=f.effect(card))
        registry=f.tempo.next_contract['utilities']
        self.assertEqual(len(registry),51);self.assertEqual(sum(row['admission']=='MATURE' for row in registry.values()),32)

    def test_reserved_activation_seven_nonadmitted(self):self.reserved('activation','ranks',7)
    def test_reserved_sandbox_six_nonadmitted(self):self.reserved('sandbox_activation','ranks',6)
    def test_reserved_stability_six_nonadmitted(self):self.reserved('stability','slots',6)

    def test_white_reactivation_identity_own_active_and_open_guards(self):
        f=self.f;(primes,_),_=self.begin([WHITE],[TRANSDUCTION+'degrade/5'])
        white=f.utility(WHITE);target=primes[2];original=copy.deepcopy(f.color.state['primes'][target])
        self.refuse('P6_UTILITY',f.utility_args(white,target=target,direction='RESTORE'),effect=f.effect(white))
        f.next_turn();attack=f.utility(TRANSDUCTION+'degrade/5','player_2')
        f.play(attack,target=target,direction='DEGRADE',player='player_2')
        self.assertEqual(f.color.state['primes'][target]['state'],'INACTIVE')
        self.refuse('P6_UTILITY',f.utility_args(white,target=target,direction='RESTORE'),effect=f.effect(white))
        f.next_turn();f.play(white,target=target,direction='RESTORE')
        p=f.color.state['primes'][target]
        self.assertEqual((p['H'],p['N'],p['R']),(1,0,0))
        for key in ('id','identity_key','slot','rank','family'):self.assertEqual(p[key],original[key])
        for item in f.tempo.next_contract['open_items']:self.refuse('P6_OPEN_GUARD',{'item':item['id']})
        catalog=f.tempo.next_contract['utilities']
        trans=[r for r in catalog.values() if r['family']=='transduction']
        self.assertEqual(len(trans),18)
        self.assertEqual(sorted(r['effect']['magnitude'] for r in trans if r['effect']['directions']==['RESTORE']),list(range(1,7)))

    def test_defense_rollback_restart_timeout_privacy_and_configuration(self):
        f=self.f;(primes,fields),(enemy,_)=self.begin([TRANSDUCTION+'degrade/0'],manifolds=['M-G-01'],enemy_manifolds=['M-G-01'])
        # Ordinary lifecycle remains executable in a P6 ACTIVE window.
        group=f.groups['player_1_config_A'];f.perform('REOPEN_CONFIGURATION',f.space_args(group[0]))
        self.assertEqual(f.ext.state['spaces'][group[0]]['lifecycle'],'CONFIGURING')
        f.perform('SET_FG_POSES',f.poses(group));f.perform('RESOLVE_CONFIGURATION',f.space_args(group[0]))
        self.assertEqual(f.ext.state['spaces'][group[0]]['lifecycle'],'RESOLVED')
        old_field=f.ext.state['spaces'][group[0]]['active_field']
        addition=next(i for i in f.members('player_1_hand') if self.h._backend.application_values['cards'][i]['category']=='Field Generator')
        f.perform('COMMIT_FG',{'cards':[addition],'destination':group[0]})
        space=f.ext.state['spaces'][group[0]]
        self.assertEqual(space['lifecycle'],'CONFIGURING');self.assertIsNone(space['active_field'])
        self.assertFalse(f.ext.state['fields'][old_field]['active'])
        self.assertTrue(all('symbolic' not in (f.ext.state['poses'][i]['value'] or {}) for i in space['members']))
        self.assertIn(addition,space['members'])
        card=f.utility(TRANSDUCTION+'degrade/0');args=f.utility_args(card,target=enemy[0],direction='DEGRADE')
        request=f.request('P6_UTILITY',args,effect=f.effect(card));before=f.snapshot()
        transport=copy.deepcopy(self.h._backend.transport_record())
        def fault(point):
            if point=='after_color_target':raise RuntimeError('actual color candidate rollback')
        self.h.fault_hook=fault
        try:
            with self.assertRaises(RuntimeError):self.h.execute(request,f.players['player_1'])
        finally:self.h.fault_hook=lambda _:None
        self.assertEqual(f.snapshot(),before)
        self.assertEqual(self.h._backend.transport_record(),transport)
        self.h.execute(request,f.players['player_1']);self.assertTrue(f.tempo.defense_open)
        self.assertEqual(f.color.state['primes'][enemy[0]]['H'],6)
        for p in ('player_1','player_2'):
            view=json.dumps(self.h._view(f.players[p]))
            other='player_2' if p=='player_1' else 'player_1'
            self.assertTrue(all(i not in view for i in f.members(other+'_hand')+f.members(other+'_deck')))
            self.assertNotIn('segment_path',view)
        request=f.request('P6_DEFENSE_PASS',{'window':f.tempo.state['defense']['id'],'reason':'TIMEOUT'},'player_2',{'policy':'TRUSTED_DEFENSE_TIMEOUT'})
        root=self.h._state['root'];values=copy.deepcopy(self.h._backend.application_values)
        f.restart();self.h=f.horizon;self.assertEqual(self.h._state['root'],root);self.assertEqual(self.h._backend.application_values,values)
        self.h.execute(request,f.players['player_2']);self.assertFalse(f.tempo.defense_open)
        self.assertEqual(f.tempo.state['defense']['reason'],'TIMEOUT')
        b=self.h._backend
        for path in (b.local_capacity.ledger_path,b.road_engine.capacity.ledger.path,
                     b.road_engine.portal.ledger.path,b.road_engine.ledger.path):
            previous='0'*64
            for line in path.read_text(encoding='utf8').splitlines():
                entry=json.loads(line);self.assertEqual(entry['prev_hash'],previous)
                previous=entry['entry_hash']

    def test_simultaneous_consequence_boundary_draw_native_candidate(self):
        f=self.f;(primes,_),(enemy,_)=self.begin([TRANSDUCTION+'degrade/5'])
        card=f.utility(TRANSDUCTION+'degrade/5')
        # Controlled consequence-boundary fixture, not an added card or public
        # operation: simultaneous inactive consequences are delivered on actual
        # native Roads inside a compiled atomic candidate before its terminal
        # check. This exercises the tie law without inventing a gameplay cause.
        inside=[]
        def consequences(point):
            if point!='after_color_target' or inside:return
            inside.append(True)
            for target in primes+enemy:
                p=f.color.state['primes'][target]
                if p['H']==0:continue
                amount=f.q(target)+p['H']
                f.tempo.transfer({'source':card,'target':target,'target_kind':'prime','amount':amount,'direction':'DEGRADE',
                    'operation':'TEST_SIMULTANEOUS_CONSEQUENCE','result':f.tempo.values.degrade(p,amount),
                    'origin':'player_1_hand','destination':p['slot']})
        self.h.fault_hook=consequences
        try:f.play(card,target=enemy[0],direction='DEGRADE')
        finally:self.h.fault_hook=lambda _:None
        self.assertEqual((f.tempo.state['status'],f.tempo.state['result'],f.tempo.state['winner'],f.tempo.state['loser']),('MATCH_COMPLETE','DRAW',None,None))
        self.assertEqual(f.tempo.losers(),['player_1','player_2']);self.assertFalse(f.tempo.defense_open)
        self.assertTrue(all(f.color.audit_road(r)['pass'] for r in self.h._backend.road_history))
        self.refuse('P6_UTILITY',f.utility_args(card,target=enemy[0],direction='DEGRADE'),effect=f.effect(card))

    def test_selection_unordered_bottom_cannot_be_drawn_or_observed_inventedly(self):
        f=self.f;f.setup_player(utilities=[DRAW+'0',DRAW+'4',DRAW+'6']);f.setup_player('player_2')
        cards=self.h._backend.application_values['cards']
        candidates=[i for i in f.members('player_1_deck') if cards[i]['category']=='Field Generator']
        for start in range(0,len(candidates)-8,3):
            group=candidates[start:min(start+3,len(candidates)-8)]
            f.perform('BATCH_TO_HAND',{'cards':group});f.perform('RETIRE_CARDS',{'cards':group})
        f.setup();f.keep();f.start();self.assertEqual(len(f.members('player_1_deck')),3)
        select=f.utility(DRAW+'4');draw=f.utility(DRAW+'0');deep=f.utility(DRAW+'6')
        top=f.members('player_1_deck');f.play(select,[top[1]])
        self.assertEqual(f.tempo.state['unordered_bottom']['player_1'],[sorted([top[0],top[2]])])
        self.refuse('P6_UTILITY',f.utility_args(draw),effect=f.effect(draw))
        self.refuse('P6_LOOK_UTILITY',{'utility':deep},effect=f.effect(deep))
        self.refuse('SHUFFLE_DECK',effect={'seed':'unaccepted-shuffle-bypass'})
