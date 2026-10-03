"""Pass-05 acceptance scenarios executed through the actual Genesis package."""
import copy
import json
from pathlib import Path
import shutil
import unittest
import zipfile

from support import ROOT
from pass_05_support import MatchFixture
from raeon_genesis_horizon.adapter import HorizonError
from raeon_genesis_horizon.toolchain import compile_paths,file_hash

DRAW='source:data/cycles/cycle_01/utilities/draw_deck.json#/values/slots/0'
WHITE='source:data/cycles/cycle_01/utilities/restore_prime.json#'
RECOVER_UTILITY='source:data/cycles/cycle_01/utilities/recovery.json#/values/slots/3'


class Pass05(unittest.TestCase):
    def setUp(self):
        self.f=MatchFixture();self.h=self.f.horizon

    def tearDown(self):self.f.close()

    def refuse(self,op,args=None,player='player_1',effect=None):
        request=self.f.request(op,args,player,effect);before=self.f.snapshot()
        with self.assertRaises(HorizonError) as error:self.h.execute(request,self.f.players[player])
        self.assertEqual(error.exception.code,'ADMISSION_REJECTED')
        self.assertEqual(self.f.snapshot(),before)
        return request

    def test_setup_hand_draw_compensation_capacity_and_privacy(self):
        f=self.f
        f.setup_player(utilities=[DRAW]);f.setup_player('player_2')
        decks={p:f.members(p+'_deck') for p in ('player_1','player_2')}
        self.refuse('SETUP_MATCH',{'first_player':'player_3'},effect={'policy':'TRUSTED_FAIR_BINARY_SETUP','outcome':'player_3'})
        f.setup('player_2')
        for p in decks:
            self.assertEqual(f.members(p+'_hand'),decks[p][:7]);self.assertEqual(f.members(p+'_deck'),decks[p][7:])
            self.assertEqual(self.h._backend.application_values['collections'][p+'_hand']['capacity'],10)
        state=f.tempo.state;obj=state['compensation']
        self.assertEqual((state['first_player'],state['selection'],obj['owner']),('player_2','TRUSTED_FAIR_BINARY_OUTCOME','player_1'))
        self.assertNotIn(obj['id'],self.h._backend.application_values['cards'])
        self.assertEqual(len(self.h._backend.collections.catalog['records']),185)
        public=dict(f.players['player_1'],view_id='public')
        for authority in [public,f.players['player_2']]:
            view=self.h._view(authority);serialized=json.dumps(view)
            self.assertEqual(view['objects']['player_1_hand']['fields']['count'],8)
            self.assertNotIn(obj['id'],serialized)
            self.assertTrue(all(i not in serialized for i in f.members('player_1_hand')+f.members('player_1_deck')))
        self.assertIn(obj['id'],self.h._view(f.players['player_1'])['objects'])
        self.refuse('USE_COMPENSATION',{'object':obj['id']})
        for item in ('P5-OPEN-001','P5-OPEN-002','P5-OPEN-003','P5-OPEN-008'):
            self.refuse('REQUEST_OPEN_RULE',{'item':item})
        self.assertTrue(f.tempo.rules['mulligan_enabled']);self.assertEqual(f.tempo.rules['mulligan_procedure'],'OPEN')
        f.start();self.assertEqual(f.members('player_2_hand')[-1],decks['player_2'][7])
        self.refuse('NORMAL_DRAW',player='player_2',effect={'policy':'TRUSTED_MATCH_CONTROL'})
        f.next_turn();self.assertEqual(f.tempo.state['phase'],'ACTIVE')
        utility=f.utility(DRAW)
        self.refuse('EFFECT_DRAW',{'utility':utility})
        self.refuse('DRAW_ONE')
        f.perform('EFFECT_DRAW',{'utility':utility},effect=f.effect(utility))
        self.assertEqual(self.h._view(f.players['player_1'])['objects']['player_1_hand']['fields']['count'],10)
        self.refuse('EFFECT_DRAW',{'utility':utility},effect=f.effect(utility))
        self.assertEqual(len(f.members('player_1_hand')),9)
        before_deck=f.members('player_1_deck')
        f.perform('USE_COMPENSATION',{'object':obj['id']},effect=f.effect(obj['id']))
        self.assertTrue(f.tempo.state['compensation']['consumed']);self.assertEqual(len(f.members('player_1_hand')),10)
        self.assertEqual(f.members('player_1_hand')[-1],before_deck[0])
        self.refuse('USE_COMPENSATION',{'object':obj['id']},effect=f.effect(obj['id']))
        self.assertEqual(len(f.members('player_2_deck')),52)

    def test_nodes_turn_boundaries_partial_repeat_and_current_carryover(self):
        f=self.f
        (yellow,sink),fields=f.setup_player(primes=['restore_yellow','universal_green'],manifolds=['M-G-01','M-G-02'])
        (attack,),af=f.setup_player('player_2',['degrade_yellow'],['M-Y-01'])
        f.setup()
        ready=copy.deepcopy(f.ext.state['fields'])
        f.start()
        self.assertEqual(f.ext.state['fields'],ready)  # READY refresh is idempotent, including topology.
        self.assertEqual(f.color.state['primes'][yellow]['state'],'HEALTHY_UNCHARGED')
        f.generate(fields[0],yellow);f.generate(fields[1],yellow)
        self.assertEqual(f.color.state['primes'][yellow]['state'],'OPERATIONAL_CHARGED')
        p=f.color.state['primes'][yellow]
        self.assertEqual((p['H'],p['H_max'],p['N'],p['R'],f.q(yellow)),(3,3,2,2,8))
        self.assertNotIn('C',p);self.assertNotIn('C_max',p);self.assertNotIn('availability',p)
        view=self.h._view(f.players['player_1'])['objects'][yellow]['fields']
        self.assertEqual((view['node_color'],view['remainder_color'],view['Q']),('YELLOW','ORANGE','8'))
        self.assertEqual((p['rank'],p['family']),('Yellow','Restore'))
        f.spend(yellow,sink,8,'RESTORE');self.assertEqual((f.q(yellow),f.q(sink)),(0,8))
        f.spend(sink,yellow,8,'RESTORE');self.assertEqual((f.q(yellow),f.q(sink)),(8,0))
        self.assertEqual([r['amount'] for r in f.color.state['history'][-2:]],[8,8])
        self.assertEqual(f.color.state['primes'][yellow]['rank'],'Yellow')
        for op,args in [('SET_ACTIVE_PLAYER',{'active_player':'player_2'}),('REFRESH_FIELDS',{'fields':fields})]:
            self.refuse(op,args,effect={'policy':'TRUSTED_MATCH_CONTROL'})
        f.control('END_ACTIVE');self.assertEqual(f.tempo.state['phase'],'END')
        self.assertTrue(all(f.ext.state['fields'][i]['availability']=='USED' for i in fields))
        f.control('ADVANCE_TURN');self.assertEqual(f.tempo.state['phase'],'REFRESH')
        self.assertTrue(all(f.ext.state['fields'][i]['availability']=='USED' for i in fields))
        f.start();self.assertTrue(all(f.ext.state['fields'][i]['availability']=='USED' for i in fields))
        f.generate(af[0],attack,'player_2');f.spend(attack,fields[0],2,'DEGRADE','player_2')
        self.assertEqual(f.ext.state['fields'][fields[0]]['current_magnitude'],2)
        f.pass_defense();f.next_turn()
        self.assertTrue(all(f.ext.state['fields'][i]['availability']=='READY' for i in fields))
        self.assertEqual(f.ext.state['fields'][fields[0]]['current_magnitude'],2)
        self.assertEqual(f.ext.state['fields'][af[0]]['availability'],'USED')
        f.spend(yellow,sink,1,'RESTORE');f.spend(yellow,sink,2,'RESTORE')
        p=f.color.state['primes'][yellow]
        self.assertEqual((f.q(yellow),f.q(sink),p['H']),(5,3,3))
        self.assertEqual((p['N'],p['R']),(1,2))
        self.refuse('SPEND_CHARGE',f.spend_args(yellow,yellow,1,'RESTORE'))
        f.generate(fields[0],sink)
        old=f.ext.state['fields'][fields[0]];qmo=old['qmo'];space=old['space'];group=f.groups[space]
        f.perform('REOPEN_CONFIGURATION',f.space_args(space));f.position(group,phi=.71);f.resolve(group)
        current=f.ext.state['fields'][f.ext.state['spaces'][space]['active_field']]
        self.assertEqual((current['qmo'],current['current_magnitude'],current['availability']),(qmo,2,'USED'))
        self.assertEqual(current['color_predecessor'],fields[0])
        self.assertFalse(any(k in f.tempo.state for k in ('action_points','mana','energy')))
        self.assertEqual(f.tempo.rules['phases'],['REFRESH','DRAW','ACTIVE','END'])

    def test_defense_stored_sources_pass_timeout_compound_rollback_and_destruction(self):
        f=self.f
        (healer,universal),fields=f.setup_player(primes=['restore_green','universal_green'],manifolds=['M-G-01','M-G-02','M-R-01'])
        (attack,),af=f.setup_player('player_2',['degrade_green'],['M-G-01','M-G-02'])
        f.setup();f.start();f.generate(fields[0],healer);f.generate(fields[1],universal);f.next_turn()
        for field in af:f.generate(field,attack,'player_2')
        f.spend(attack,fields[0],1,'DEGRADE','player_2')
        self.assertEqual(f.ext.state['fields'][fields[0]]['current_magnitude'],3)
        self.assertTrue(f.tempo.defense_open)
        self.assertEqual(f.tempo.state['defense']['maximum_responses'],1)
        self.assertEqual(f.tempo.state['defense']['timer_seconds'],'OPEN')
        self.refuse('REQUEST_OPEN_RULE',{'item':'P5-OPEN-004'})
        self.refuse('SPEND_CHARGE',f.spend_args(universal,attack,1,'DEGRADE'))
        wrong=f.response_args(healer,fields[1],1)
        self.refuse('DEFENSE_RESTORE',wrong)
        f.respond(healer,fields[0],1)
        self.assertFalse(f.tempo.defense_open);self.assertEqual(f.ext.state['fields'][fields[0]]['current_magnitude'],4)
        self.refuse('DEFENSE_RESTORE',f.response_args(healer,fields[0],1))
        f.spend(attack,fields[0],1,'DEGRADE','player_2');f.respond(universal,fields[0],1)
        f.spend(attack,fields[0],1,'DEGRADE','player_2');f.pass_defense()
        f.spend(attack,fields[0],1,'DEGRADE','player_2');f.pass_defense(timeout=True)
        self.assertEqual(f.ext.state['fields'][fields[0]]['current_magnitude'],2)
        f.spend(attack,fields[0],1,'DEGRADE','player_2')
        request=f.request('DEFENSE_RESTORE',f.response_args(healer,fields[0],1,fields[2]))
        before=f.snapshot();roads=len(self.h._backend.road_history)
        sources=[]
        def fail_second_source(point):
            if point=='after_color_source':
                sources.append(point)
                if len(sources)==2:raise RuntimeError('compound response fault after generated charge and Prime spend')
        self.h.fault_hook=fail_second_source
        try:
            with self.assertRaises(RuntimeError):self.h.execute(request,f.players['player_1'])
        finally:self.h.fault_hook=lambda _:None
        self.assertEqual(len(sources),2)
        self.assertEqual(f.snapshot(),before)
        self.assertEqual(f.ext.state['fields'][fields[0]]['current_magnitude'],1)
        self.assertTrue(f.tempo.defense_open)
        self.h.execute(request,f.players['player_1'])
        self.assertEqual(f.ext.state['fields'][fields[0]]['current_magnitude'],2)
        self.assertEqual(f.ext.state['fields'][fields[2]]['availability'],'USED')
        self.assertEqual(len(f.color.state['history'][-2:]),2)
        self.assertTrue(all(row['operation']=='DEFENSE_RESTORE' for row in f.color.state['history'][-2:]))
        self.assertGreater(len(self.h._backend.road_history),roads)
        history=f.tempo.state['history'];events=[row['event'] for row in history]
        self.assertLess(max(i for i,e in enumerate(events) if e=='DEGRADE_RESOLVED'),max(i for i,e in enumerate(events) if e=='DEFENSE_RESTORE_RESOLVED'))
        committed=f.snapshot();self.h.execute(request,f.players['player_1']);self.assertEqual(f.snapshot(),committed)
        ids=list(f.ext.state['fields'][fields[0]]['members'])
        f.spend(attack,fields[0],2,'DEGRADE','player_2')
        self.assertFalse(f.tempo.defense_open)
        self.assertFalse(f.ext.state['fields'][fields[0]]['active'])
        self.assertEqual(f.members('player_1_graveyard'),ids)
        self.refuse('DEFENSE_RESTORE',f.response_args(healer,fields[0],1))

    def test_field_origin_defense_health_first_and_degrade_mediator_guard(self):
        f=self.f
        (target,degrade),fields=f.setup_player(primes=['universal_green','degrade_yellow'],manifolds=['M-G-01'])
        (attack,),af=f.setup_player('player_2',['degrade_yellow'],['M-Y-01'])
        f.setup('player_2');f.start();f.generate(af[0],attack,'player_2');f.spend(attack,target,2,'DEGRADE','player_2')
        p=f.color.state['primes'][target]
        self.assertEqual((p['H'],p['N'],p['R'],p['state']),(2,0,0,'DAMAGED_NON_OPERATIONAL'))
        self.refuse('DEFENSE_RESTORE',f.response_args(degrade,target,1,fields[0]))
        self.refuse('DEFENSE_RESTORE',f.response_args(target,target,1))
        f.respond(target,target,4,fields[0])
        p=f.color.state['primes'][target]
        self.assertEqual((p['H'],p['N'],p['R'],f.q(target)),(4,0,2,2))
        self.assertEqual(f.ext.state['fields'][fields[0]]['availability'],'USED')
        f.spend(attack,target,1,'DEGRADE','player_2')
        self.assertEqual((p['H'],p['N'],p['R']),(4,0,1))
        self.assertFalse(f.tempo.defense_open)  # Self-Restore and USED field supply no option.
        f.next_turn();f.next_turn()
        f.generate(af[0],attack,'player_2');f.spend(attack,target,3,'DEGRADE','player_2')
        p=f.color.state['primes'][target]
        self.assertEqual((p['H'],p['N'],p['R'],f.q(target)),(2,0,0,0))
        self.assertTrue(f.tempo.defense_open);f.pass_defense()

    def test_zero_cost_utilities_require_hand_timing_target_and_white_exactness(self):
        f=self.f
        (attack,),af=f.setup_player(primes=['degrade_white'],manifolds=['M-V-01'])
        (victim,healer),fields=f.setup_player('player_2',['universal_green','restore_green'],['M-G-01'],[WHITE,RECOVER_UTILITY])
        f.setup();f.start();f.generate(af[0],attack);f.spend(attack,victim,4,'DEGRADE')
        self.assertFalse(f.tempo.defense_open);self.assertEqual(f.tempo.state['status'],'RUNNING')
        f.next_turn();white=f.utility(WHITE,'player_2');recovery=f.utility(RECOVER_UTILITY,'player_2')
        self.refuse('GENERATE_CHARGE',f.generate_args(fields[0],victim),'player_2')
        def args(target):return {'utility':white,'prime':target,'prime_revision':f.color.state['primes'][target]['revision']}
        self.refuse('WHITE_REACTIVATE',args(victim),'player_2')
        self.refuse('WHITE_REACTIVATE',args(healer),'player_2',f.effect(white))
        f.perform('RETIRE_CARDS',{'cards':[white]},'player_2')
        self.refuse('WHITE_REACTIVATE',args(victim),'player_2',f.effect(white))
        f.perform('RECOVER_4',{'cards':[white]},'player_2',effect=f.effect(recovery))
        resources=copy.deepcopy(f.color.state['primes']);availability=copy.deepcopy(f.ext.state['fields'])
        slot=f.color.state['primes'][victim]['slot']
        f.perform('WHITE_REACTIVATE',args(victim),'player_2',effect=f.effect(white))
        p=f.color.state['primes'][victim]
        self.assertEqual((p['H'],p['N'],p['R']),(1,0,0));self.assertEqual(f.members(slot),[victim])
        self.assertEqual(f.ext.state['fields'],availability)
        self.assertEqual(f.color.state['primes'][healer],resources[healer]);self.assertEqual(f.color.state['primes'][attack],resources[attack])
        self.assertEqual(f.tempo.rules['utility']['generic_resource_cost'],0)
        self.assertEqual(f.tempo.rules['utility']['generic_timing'],'OPEN')
        f.generate(fields[0],victim,'player_2')
        self.assertEqual((p['H'],p['N'],p['R']),(4,0,1))

    def test_three_inactive_terminal_before_defense_and_no_later_gameplay(self):
        f=self.f
        (attack,),af=f.setup_player(primes=['degrade_violet'],manifolds=['M-V-01'])
        targets,fields=f.setup_player('player_2',['universal_red','universal_orange','universal_yellow'],['M-R-01'],[WHITE])
        f.setup();f.start();f.generate(af[0],attack)
        self.refuse('REQUEST_OPEN_RULE',{'item':'P5-OPEN-005'})
        self.assertEqual(f.tempo.rules['simultaneous_terminal'],'OPEN')
        for i,target in enumerate(targets):
            f.spend(attack,target,i+1,'DEGRADE')
            self.assertEqual(f.color.state['primes'][target]['state'],'INACTIVE')
            self.assertFalse(f.tempo.defense_open)
            if i<2:self.assertEqual(f.tempo.state['status'],'RUNNING')
        self.assertEqual((f.tempo.state['status'],f.tempo.state['loser'],f.tempo.state['winner']),('MATCH_COMPLETE','player_2','player_1'))
        self.assertEqual(f.tempo.state['history'][-1]['event'],'MATCH_COMPLETE')
        self.assertEqual(f.tempo.state['defense'],{})
        white=f.utility(WHITE,'player_2')
        self.refuse('WHITE_REACTIVATE',{'utility':white,'prime':targets[0],'prime_revision':f.color.state['primes'][targets[0]]['revision']},'player_2',f.effect(white))
        self.refuse('END_ACTIVE',effect={'policy':'TRUSTED_MATCH_CONTROL'})
        self.refuse('GENERATE_CHARGE',f.generate_args(fields[0],targets[0]),'player_2')
        self.refuse('RETIRE_CARDS',{'cards':[f.members('player_1_hand')[0]]})

    def test_real_pass04_checkpoint_upgrade_and_canonical_migration(self):
        f=self.f;directory=ROOT/'tests/integration/genesis_horizon/fixtures'
        record=json.loads((directory/'pass04-checkpoint.json').read_text())
        self.assertEqual(file_hash(directory/'pass04-checkpoint.zip'),record['archive_sha256'])
        target=self.h.storage/'checkpoints'/record['checkpoint']['name'];target.mkdir(parents=True)
        with zipfile.ZipFile(directory/'pass04-checkpoint.zip') as archive:
            for entry in archive.infolist():
                path=(target/entry.filename).resolve();self.assertTrue(path.is_relative_to(target))
                path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(archive.read(entry))
        before=f.snapshot()
        with self.assertRaises(HorizonError):self.h.restore(record['checkpoint'],f.owner)
        self.assertEqual(f.snapshot(),before)
        with self.assertRaises(HorizonError):self.h.restore(record['checkpoint'],f.owner,upgrade_package=f.package)
        self.assertEqual(f.snapshot(),before)
        self.h.restore(record['checkpoint'],dict(f.owner,upgrade=True),upgrade_package=f.package)
        self.assertEqual(self.h._state['root'],record['checkpoint']['root'])
        f.ext=self.h._backend.collections.extension;f.connect();f.grant_serial=10000
        old=copy.deepcopy(f.color.state);fields=copy.deepcopy(f.ext.state['fields'])
        cards=copy.deepcopy(self.h._backend.application_values['cards'])
        f.perform('ADOPT_PASS05',effect={'policy':'TRUSTED_PASS05_MIGRATION'})
        for identity,p in old['primes'].items():
            current=f.color.state['primes'][identity]
            self.assertEqual(f.q(identity),p['C'])
            self.assertEqual((current['N'],current['R']),divmod(p['C'],p['H_max']))
            for key in ('id','slot','catalog','identity_key','family','rank','H_max','H','revision'):
                self.assertEqual(current[key],p[key])
            self.assertNotIn('C',current);self.assertNotIn('C_max',current)
        self.assertTrue(any(p['N']==1 and p['R']==0 for p in f.color.state['primes'].values()))
        self.assertEqual(f.color.state['history'],old['history']);self.assertEqual(f.ext.state['fields'],fields)
        self.assertEqual(self.h._backend.application_values['cards'],cards)
        values=copy.deepcopy(self.h._backend.application_values)
        checkpoint=self.h.checkpoint(f.owner);self.h.restore(checkpoint,f.owner)
        self.assertEqual(self.h._backend.application_values,values)
        f.ext=self.h._backend.collections.extension

    def test_exhaustion_actual_empty_deck_six_stages_and_open_seventh(self):
        f=self.f
        (prime,),fields=f.setup_player(primes=['universal_green'],manifolds=['M-R-01'])
        f.setup_player('player_2')
        # Reach the predecessor through actual admitted native transfers, never
        # by shortening a Python Deck list or inventing a small-deck format.
        capacity=self.h._backend.application_values['collections']['player_1_hand']['capacity']
        while len(f.members('player_1_deck'))>7:
            ids=f.members('player_1_deck')[:min(3,len(f.members('player_1_deck'))-7)]
            # Keep the inherited three-card transfer bound and actual Hand capacity.
            # Retire accumulated cards together so this long native scenario
            # has storage headroom even under a deeper offline extraction path.
            if len(f.members('player_1_hand'))+len(ids)>capacity:
                f.perform('RETIRE_CARDS',{'cards':f.members('player_1_hand')})
            f.perform('BATCH_TO_HAND',{'cards':ids})
        if f.members('player_1_hand'):
            f.perform('RETIRE_CARDS',{'cards':f.members('player_1_hand')})
        f.setup();self.assertEqual(f.members('player_1_deck'),[])
        primes=copy.deepcopy(f.color.state['primes']);ordinary=copy.deepcopy(f.ext.state['fields'])
        for stage in range(1,8):
            f.start()
            state=f.tempo.state
            self.assertEqual(state['failed_normal_draws']['player_1'],stage)
            self.assertEqual(state['status'],'RUNNING');self.assertEqual(state['phase'],'ACTIVE')
            result=state['exhaustion']['player_1']
            self.assertIsNone(result['target']);self.assertEqual(result['application'],'OPEN_NOT_APPLIED')
            if stage<=6:
                self.assertEqual((result['color'],result['magnitude']),(['RED','ORANGE','YELLOW','GREEN','BLUE','VIOLET'][stage-1],stage))
            else:
                self.assertIsNone(result['color']);self.assertIsNone(result['magnitude']);self.assertEqual(result['stage_7_plus'],'OPEN')
            self.assertEqual(f.color.state['primes'],primes);self.assertEqual(f.ext.state['fields'],ordinary)
            self.assertFalse(f.color.state['history'])
            if stage<7:
                f.next_turn()
                f.perform('RETIRE_CARDS',{'cards':f.members('player_2_hand')},'player_2')
                f.control('END_ACTIVE');f.control('ADVANCE_TURN')
        for item in ('P5-OPEN-006','P5-OPEN-007'):
            self.refuse('REQUEST_OPEN_RULE',{'item':item})

    def test_current_checkpoint_restart_replay_defense_order_and_road_history(self):
        def story(f):
            (healer,),fields=f.setup_player(primes=['restore_green'],manifolds=['M-G-01'])
            (attack,),af=f.setup_player('player_2',['degrade_yellow'],['M-Y-01'])
            f.setup();f.start();f.generate(fields[0],healer);f.next_turn()
            f.generate(af[0],attack,'player_2');f.spend(attack,fields[0],1,'DEGRADE','player_2')
            request=f.request('DEFENSE_RESTORE',f.response_args(healer,fields[0],1))
            return healer,fields[0],request
        f=self.f;healer,field,request=story(f)
        values=copy.deepcopy(self.h._backend.application_values);root=self.h._state['root']
        other=MatchFixture()
        try:
            story(other);self.assertEqual(other.horizon._state['root'],root)
            self.assertEqual(other.horizon._backend.application_values,values)
        finally:other.close()
        public=dict(f.players['player_1'],view_id='public')
        for authority in [public,f.players['player_1'],f.players['player_2']]:
            view=self.h._view(authority);text=json.dumps(view)
            for player in ('player_1','player_2'):
                if authority['view_id']!=player:
                    self.assertTrue(all(i not in text for i in f.members(player+'_hand')+f.members(player+'_deck')))
            self.assertNotIn('effect_source',text);self.assertNotIn('road_index',text);self.assertNotIn('segment_path',text)
        roads=copy.deepcopy(self.h._backend.road_history)
        f.restart();self.h=f.horizon
        self.assertEqual(self.h._backend.application_values,values);self.assertEqual(self.h._state['root'],root)
        restored=self.h._backend.road_history
        self.assertEqual([(f.color.road_commitment(r),r['timestamp_ns']) for r in restored[:len(roads)]],
                         [(f.color.road_commitment(r),r['timestamp_ns']) for r in roads])
        self.assertTrue(f.tempo.defense_open);self.assertEqual(f.tempo.state['phase'],'ACTIVE')
        self.h.execute(request,f.players['player_1'])
        self.assertFalse(f.tempo.defense_open);self.assertEqual(f.q(healer),3)
        events=f.tempo.state['history']
        damage=next(e for e in events if e['event']=='DEGRADE_RESOLVED')
        restore=next(e for e in events if e['event']=='DEFENSE_RESTORE_RESOLVED')
        self.assertLess(damage['revision'],restore['revision'])
        before=f.snapshot();self.h.execute(request,f.players['player_1']);self.assertEqual(f.snapshot(),before)

    def test_current_genesis_admission_closure_and_road_cannot_be_bypassed(self):
        f=self.f
        (prime,),fields=f.setup_player(primes=['restore_yellow'],manifolds=['M-G-01'])
        f.setup_player('player_2');f.setup();f.start()
        request=f.request('GENERATE_CHARGE',f.generate_args(fields[0],prime));before=f.snapshot()
        path=ROOT/'game/core/raeon/application/generate_charge.gen';key=path.relative_to(ROOT).as_posix()
        original=self.h._builds[key]
        for old,new in [('"READY_ORDINARY_SOURCE",',''),
          ('  transform match with permission as candidate @{"operator":"COLLECTION_TRANSACTION"}',
           '  en candidate : GEOMETRIC = instantiate fabric region mmo @bound_match')]:
            self.assertIn(old,path.read_text())
            changed=f.path/'mutated.gen';changed.write_text(path.read_text().replace(old,new),encoding='utf8')
            self.h._builds[key]=compile_paths([changed],ROOT,'mutated')
            try:
                with self.assertRaises(Exception):self.h.execute(request,f.players['player_1'])
            finally:self.h._builds[key]=original
            self.assertEqual(f.snapshot(),before)
        service=self.h._backend.collections;run=service.run_unit
        service.run_unit=lambda name:None if name=='transport' else run(name)
        try:
            with self.assertRaises(Exception):self.h.execute(request,f.players['player_1'])
        finally:service.run_unit=run
        self.assertEqual(f.snapshot(),before)
        self.h.execute(request,f.players['player_1'])
        self.assertEqual(f.q(prime),4)
        row=f.color.state['history'][-1];road=self.h._backend.road_history[row['road_index']]
        self.assertEqual(road['status'],'CLOSED');self.assertTrue(f.color.audit_road(road)['pass'])
        self.assertTrue(all(r['receipt']['payload']['verified'] for r in service.ints.receipts))
        # Current mathematical admission cannot be overridden by a cost flag.
        space=f.ext.state['fields'][fields[0]]['space'];group=f.groups[space]
        f.perform('REOPEN_CONFIGURATION',f.space_args(space))
        f.position(group,distort=lambda slot,x,y:(x*1.37,y*1.37))
        self.refuse('RESOLVE_CONFIGURATION',f.space_args(space),effect={'generic_resource_cost':0,'bypass_math':True})
        self.assertEqual(f.tempo.rules['utility']['generic_resource_cost'],0)

    def test_current_zero_retirement_selective_emergence_and_open_guards(self):
        f=self.f
        (attack,),af=f.setup_player(primes=['degrade_yellow'],manifolds=['M-Y-01'])
        (prime,),fields=f.setup_player('player_2',['restore_yellow'],['M-R-01','M-R-02','M-R-03'])
        f.setup();f.start();f.generate(af[0],attack)
        survivors={k:copy.deepcopy(v) for k,v in f.ext.state['emergents'].items() if fields[0] not in v['supports']}
        self.assertTrue(any(fields[0] in v['supports'] for v in f.ext.state['emergents'].values()))
        ids=list(f.ext.state['fields'][fields[0]]['members'])
        f.spend(attack,fields[0],1,'DEGRADE')
        self.assertEqual(f.ext.state['emergents'],survivors)
        self.assertEqual(f.members('player_2_graveyard'),ids);self.assertFalse(f.tempo.defense_open)
        self.refuse('GENERATE_CHARGE',f.generate_args(fields[0],prime),'player_2')
        for item in ('P5-OPEN-009','P5-OPEN-010','P5-OPEN-011','P5-OPEN-012','P5-OPEN-013',
                     'P5-OPEN-014','P5-OPEN-015','P5-OPEN-016'):
            self.refuse('REQUEST_OPEN_RULE',{'item':item})


if __name__=='__main__':unittest.main()
