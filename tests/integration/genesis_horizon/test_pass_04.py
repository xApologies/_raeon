"""Real Pass-4 scenarios and adversarial transactions; no state seeding shortcuts."""
import copy
import json
from concurrent.futures import ThreadPoolExecutor
import unittest

from pass_04_support import PrimeFixture
from support import ROOT, Port, port_decode
from raeon_genesis_horizon.toolchain import compile_paths, digest


class Pass04(unittest.TestCase):
    def setUp(self):
        self.f=PrimeFixture()

    def tearDown(self):
        self.f.close()

    @property
    def h(self):return self.f.horizon

    def pair(self, prime):
        p=self.f.color.state['primes'][prime]
        return p['H'],p['C']

    def refuse(self, operation, arguments, player='player_1', effect=None):
        request=self.f.request(operation,arguments,player,effect)
        before=self.f.snapshot()
        with self.assertRaises(Exception):self.h.execute(request,self.f.players[player])
        self.assertEqual(self.f.snapshot(),before)

    def test_catalog_binding_identity_initial_states_and_fixed_slots(self):
        self.assertEqual(len(self.f.color.catalog),14)
        self.assertEqual({family:sum(r['family']==family for r in self.f.color.catalog.values()) for family in ['Restore','Degrade','Universal']},
                         {'Restore':5,'Degrade':5,'Universal':4})
        self.assertTrue(all(r['copy_limit']==1 for r in self.f.color.catalog.values()))
        primes,_=self.f.setup_player(primes=['universal_red','restore_green','degrade_white'])
        for i,(prime,rank) in enumerate(zip(primes,[1,4,7]),1):
            p=self.f.color.state['primes'][prime];self.assertEqual(self.pair(prime),(rank,0))
            self.assertEqual(p['H_max'],rank);self.assertEqual(p['C_max'],rank)
            self.assertEqual(p['state'],'HEALTHY_UNCHARGED')
            slot='player_1_prime_'+str(i);self.assertEqual(p['slot'],slot)
            self.assertNotEqual(prime,self.h._view(self.f.players['player_1'])['objects'][slot]['identity'])
            self.assertEqual(self.f.members(slot),[prime]);self.assertNotIn('H',self.h._view(self.f.players['player_1'])['objects'][slot]['fields'])
        self.assertIsNone(self.f.color.state['active_player'])
        self.refuse('RETIRE_CARDS',{'cards':primes[:1]})
        roster=self.f.neutral();handle=self.h._backend.application_values['cards'][primes[0]]['catalog'];roster[:2]=[handle,handle]
        self.refuse('INITIALIZE_INVENTORY',{'roster':roster},'player_2')

    def test_A_generate_current_color_once_through_road(self):
        primes,fields=self.f.setup_player(primes=['restore_green'],manifolds=['M-G-01'])
        prime,field=primes[0],fields[0];source=self.f.ext.state['fields'][field]
        original=copy.deepcopy({k:source[k] for k in ('qmo','native_identity','source_sha256','native_color')})
        self.assertEqual((source['native_maximum'],source['current_magnitude'],source['current_color'],source['availability']),(4,4,'GREEN','READY'))
        self.refuse('GENERATE_FIELD',self.f.generate_args(field,prime))  # No invented first player.
        self.f.active('player_1');self.f.generate(field,prime)
        self.assertEqual(self.pair(prime),(4,4));self.assertEqual(self.f.color.state['primes'][prime]['state'],'OPERATIONAL_CHARGED')
        source=self.f.ext.state['fields'][field]
        self.assertTrue(source['active']);self.assertEqual(source['availability'],'USED')
        self.assertEqual(self.f.ext.state['spaces'][source['space']]['lifecycle'],'RESOLVED')
        self.assertEqual({k:source[k] for k in original},original)
        row=self.f.color.state['history'][-1];self.assertEqual((row['source'],row['target'],row['amount']),(field,prime,4))
        road=self.h._backend.road_history[row['road_index']]
        self.assertEqual(road['status'],'CLOSED')
        self.assertEqual(self.f.color.road_commitment(road),row['road_commitment_sha256'])
        relocated=copy.deepcopy(road);relocated['timestamp_ns']+=1
        for portal in relocated['portal_receipts']:
            portal['timestamp_ns']+=1
            portal['source_segment_hashes']={'another-host/'+str(i):v for i,v in enumerate(portal['source_segment_hashes'].values())}
        self.assertNotEqual(digest(relocated),digest(road))
        self.assertEqual(self.f.color.road_commitment(relocated),row['road_commitment_sha256'])
        saved=copy.deepcopy(road)
        try:
            road['source_content_root']='tampered-content'
            with self.assertRaises(ValueError):self.f.color.validate()
        finally:
            road.clear();road.update(saved)
        self.f.color.validate()
        self.refuse('GENERATE_FIELD',self.f.generate_args(field,prime))

    def test_B_partial_repeated_spending_keeps_health_and_shield(self):
        (source,target),fields=self.f.setup_player(primes=['restore_green','universal_green'],manifolds=['M-G-01'])
        self.f.active('player_1');self.f.generate(fields[0],source)
        self.f.spend(source,target,1,'RESTORE');self.assertEqual(self.pair(source),(4,3));self.assertEqual(self.pair(target),(4,1))
        self.f.spend(source,target,2,'RESTORE');self.assertEqual(self.pair(source),(4,1));self.assertEqual(self.pair(target),(4,3))
        self.f.spend(source,target,1,'RESTORE');self.assertEqual(self.pair(source),(4,0));self.assertEqual(self.pair(target),(4,4))
        self.assertEqual(self.f.color.state['primes'][source]['state'],'HEALTHY_UNCHARGED')
        self.refuse('SPEND_PRIME',self.f.spend_args(source,target,1,'RESTORE'))

    def test_C_D_shield_first_damage_and_health_first_restore(self):
        (attacker,),af=self.f.setup_player(primes=['degrade_violet'],manifolds=['M-V-01'])
        (victim,healer),vf=self.f.setup_player('player_2',['universal_green','restore_green'],['M-Y-01','M-G-01'])
        self.f.active('player_2');self.f.generate(vf[0],victim,'player_2');self.f.generate(vf[1],healer,'player_2')
        self.f.active('player_1');self.f.generate(af[0],attacker)
        self.assertEqual(self.pair(victim),(4,3))
        self.f.spend(attacker,victim,5,'DEGRADE');self.assertEqual(self.pair(victim),(2,0))
        self.assertEqual(self.f.color.state['primes'][victim]['state'],'DAMAGED_NON_OPERATIONAL')
        self.refuse('SPEND_PRIME',self.f.spend_args(victim,healer,1,'RESTORE'),'player_2')
        self.f.spend(attacker,victim,1,'DEGRADE');self.assertEqual(self.pair(victim),(1,0))
        self.f.spend(healer,victim,4,'RESTORE','player_2');self.assertEqual(self.pair(victim),(4,1))
        self.assertEqual(self.pair(healer),(4,0))

    def test_E_same_topology_carryover_no_implicit_heal_or_refresh(self):
        (sink,healer,white),fields=self.f.setup_player(primes=['universal_green','restore_green','restore_white'],manifolds=['M-G-01','M-G-02'])
        (attacker,),af=self.f.setup_player('player_2',['degrade_yellow'],['M-Y-01'])
        self.f.active('player_2');self.f.generate(af[0],attacker,'player_2')
        old=self.f.ext.state['fields'][fields[0]];qmo=old['qmo'];space=old['space'];group=self.f.groups[space]
        self.f.spend(attacker,fields[0],3,'DEGRADE','player_2')
        self.assertEqual((old['native_color'],old['current_color'],old['current_magnitude']),('GREEN','RED',1))
        self.f.generate(fields[0],sink);self.assertEqual(self.pair(sink),(4,1))
        before=self.f.snapshot();self.f.ext.query(space);self.assertEqual(self.f.snapshot(),before)
        self.f.perform('REOPEN_CONFIGURATION',self.f.space_args(space));self.f.position(group,phi=0.71)
        self.f.resolve(group);current=self.f.ext.state['spaces'][space]['active_field'];field=self.f.ext.state['fields'][current]
        self.assertEqual((field['qmo'],field['current_magnitude'],field['availability']),(qmo,1,'USED'))
        self.assertEqual(field['color_predecessor'],fields[0]);self.assertEqual(field['native_maximum'],4)
        self.refuse('GENERATE_FIELD',self.f.generate_args(current,sink))
        self.f.generate(fields[1],healer);self.f.spend(healer,current,3,'RESTORE')
        field=self.f.ext.state['fields'][current]
        self.assertEqual((field['current_color'],field['current_magnitude'],field['availability']),('GREEN',4,'USED'))
        self.refuse('SPEND_PRIME',self.f.spend_args(healer,current,1,'RESTORE'))
        self.refuse('REFRESH_FIELDS',{'fields':[current]})
        self.f.refresh([current]);self.assertEqual(self.f.ext.state['fields'][current]['availability'],'READY')
        self.f.generate(current,white);self.assertEqual(self.pair(white),(7,4));self.assertEqual(self.f.ext.state['fields'][current]['availability'],'USED')
        checkpoint=self.h.checkpoint(self.f.owner);self.h.restore(checkpoint,self.f.owner)
        self.f.ext=self.h._backend.collections.extension
        self.f.perform('REOPEN_CONFIGURATION',self.f.space_args(space));self.f.position(group,phi=-0.2)
        self.f.resolve(group)
        recovered=self.f.ext.state['fields'][self.f.ext.state['spaces'][space]['active_field']]
        self.assertEqual((recovered['color_predecessor'],recovered['current_magnitude'],recovered['availability']),
                         (current,4,'USED'))

    def test_F_zero_color_atomic_graveyard_and_selective_emergence_loss(self):
        (attacker,),af=self.f.setup_player(primes=['degrade_yellow'],manifolds=['M-Y-01'])
        (target_prime,),fields=self.f.setup_player('player_2',['restore_yellow'],['M-R-01','M-R-02','M-R-03'])
        self.f.active('player_1');self.f.generate(af[0],attacker)
        field=self.f.ext.state['fields'][fields[0]];ids=list(field['members']);space=field['space']
        survivors={k:copy.deepcopy(v) for k,v in self.f.ext.state['emergents'].items() if fields[0] not in v['supports']}
        self.assertTrue(any(fields[0] in v['supports'] for v in self.f.ext.state['emergents'].values()))
        request=self.f.request('SPEND_PRIME',self.f.spend_args(attacker,fields[0],1,'DEGRADE'));before=self.f.snapshot()
        for point in ['after_color_removal','after_field_destruction','after_emergents']:
            self.h.fault_hook=lambda p: (_ for _ in ()).throw(RuntimeError('fault')) if p==point else None
            try:
                with self.assertRaises(Exception):self.h.execute(request,self.f.players['player_1'])
            finally:self.h.fault_hook=lambda _:None
            self.assertEqual(self.f.snapshot(),before)
        self.h.execute(request,self.f.players['player_1'])
        field=self.f.ext.state['fields'][fields[0]]
        self.assertEqual((field['current_magnitude'],field['current_color'],field['active']),(0,None,False))
        self.assertEqual(self.f.members('player_2_graveyard'),ids);self.assertEqual(self.f.members(space),[])
        self.assertEqual(self.f.ext.state['spaces'][space]['lifecycle'],'EMPTY');self.assertIsNone(self.f.ext.state['spaces'][space]['active_field'])
        self.assertEqual(self.f.ext.state['emergents'],survivors)
        for identity in ids:
            card=self.h._backend.application_values['cards'][identity]
            self.assertEqual(card['id'],identity);self.assertEqual(card['history'][-1]['reason'],'ZERO_COLOR')
            self.assertEqual(card['location'],'player_2_graveyard')
        self.refuse('GENERATE_FIELD',self.f.generate_args(fields[0],target_prime),'player_2')
        self.assertNotIn(fields[0],self.h._view(self.f.players['player_1'])['objects'])

    def test_G_H_authority_windows_reservations_and_no_switch_refresh(self):
        (r1,u1,d1),f1=self.f.setup_player(primes=['restore_green','universal_green','degrade_green'],manifolds=['M-G-01','M-R-01'])
        (u2,d2,r2),f2=self.f.setup_player('player_2',['universal_green','degrade_green','restore_white'],['M-G-01','M-G-02'])
        self.f.active('player_1');self.f.generate(f1[0],r1)
        self.f.active('player_2');self.f.generate(f2[0],u2,'player_2');self.f.generate(f2[1],d2,'player_2')
        self.f.spend(u2,d1,1,'DEGRADE','player_2');self.assertEqual(self.pair(d1),(3,0))
        self.assertEqual(self.f.ext.state['fields'][f1[0]]['availability'],'USED')
        self.assertEqual(self.f.ext.state['fields'][f1[1]]['availability'],'READY')
        self.f.generate(f1[1],u1);self.assertEqual(self.pair(u1),(4,1))  # Reserved defense output.
        self.f.active('player_1')
        self.refuse('SPEND_PRIME',self.f.spend_args(d2,r1,1,'DEGRADE'),'player_2')
        self.refuse('SPEND_PRIME',self.f.spend_args(u2,r1,1,'DEGRADE'),'player_2')
        self.f.spend(u2,r2,1,'RESTORE','player_2');self.assertEqual(self.pair(r2),(7,1))
        self.f.refresh([f2[0]],'player_2')
        self.refuse('GENERATE_FIELD',self.f.generate_args(f2[0],d2),'player_2')
        self.f.generate(f2[0],r2,'player_2');self.assertEqual(self.pair(r2),(7,5))
        self.refuse('SPEND_PRIME',self.f.spend_args(r1,r2,1,'RESTORE'))
        self.refuse('SPEND_PRIME',self.f.spend_args(u1,r1,1,'DEGRADE'))
        self.refuse('SPEND_PRIME',self.f.spend_args(r1,r2,1,'DEGRADE'))
        self.refuse('SPEND_PRIME',self.f.spend_args(d2,r2,1,'RESTORE'),'player_2')
        self.refuse('GENERATE_FIELD',dict(self.f.generate_args(f1[0],r2)))
        self.refuse('SET_ACTIVE_PLAYER',{'active_player':'player_2'})
        for player in ['player_2','player_1']:
            self.f.active(player)
            self.assertTrue(all(self.f.ext.state['fields'][field]['availability']=='USED' for field in f1+f2))

    def test_I_inactive_stays_fixed_and_white_restores_only_one_health(self):
        (attacker,),af=self.f.setup_player(primes=['degrade_white'],manifolds=['M-V-01'])
        (victim,healer,red),vf=self.f.setup_player('player_2',['universal_green','restore_green','universal_red'],['M-G-01'])
        self.f.active('player_1');self.f.generate(af[0],attacker);self.f.generate(vf[0],healer,'player_2')
        slots={p:self.f.color.state['primes'][p]['slot'] for p in [victim,red]}
        self.f.spend(attacker,victim,4,'DEGRADE');self.assertEqual(self.pair(victim),(0,0))
        self.assertEqual(self.f.color.state['primes'][victim]['state'],'INACTIVE')
        self.refuse('SPEND_PRIME',self.f.spend_args(healer,victim,1,'RESTORE'),'player_2')
        self.refuse('WHITE_RESTORE_PRIME',{'prime':victim,'prime_revision':self.f.color.state['primes'][victim]['revision']},'player_2')
        self.f.white(victim,'player_2');self.assertEqual(self.pair(victim),(1,0))
        self.assertEqual(self.f.color.state['primes'][victim]['state'],'DAMAGED_NON_OPERATIONAL')
        self.refuse('SPEND_PRIME',self.f.spend_args(victim,healer,1,'RESTORE'),'player_2')
        self.f.spend(healer,victim,3,'RESTORE','player_2');self.assertEqual(self.pair(victim),(4,0))
        self.f.spend(attacker,red,1,'DEGRADE');self.f.white(red,'player_2')
        self.assertEqual(self.pair(red),(1,0));self.assertEqual(self.f.color.state['primes'][red]['state'],'HEALTHY_UNCHARGED')
        for p,slot in slots.items():self.assertEqual(self.f.members(slot),[p])
        self.assertEqual(self.f.members('player_2_graveyard'),[])

    def test_overflow_and_unsupported_targets_fail_without_consuming(self):
        (source,target),fields=self.f.setup_player(primes=['restore_green','universal_green'],manifolds=['M-R-01','M-G-01'])
        self.f.active('player_1');self.f.generate(fields[0],target)
        self.refuse('GENERATE_FIELD',self.f.generate_args(fields[1],target))  # Whole 4 cannot fit remaining 3.
        self.assertEqual(self.f.ext.state['fields'][fields[1]]['availability'],'READY')
        self.f.generate(fields[1],source)
        self.refuse('SPEND_PRIME',self.f.spend_args(source,target,4,'RESTORE'))
        self.refuse('SPEND_PRIME',self.f.spend_args(source,source,1,'RESTORE'))
        self.refuse('SPEND_PRIME',self.f.spend_args(source,fields[1],1,'RESTORE'))
        for amount in [0,-1,8,True,1.2]:
            args=self.f.spend_args(source,target,1,'RESTORE');args['amount']=amount
            before=self.f.snapshot()
            with self.assertRaises(Exception):self.f.request('SPEND_PRIME',args)
            self.assertEqual(self.f.snapshot(),before)
        args=self.f.spend_args(source,target,1,'RESTORE');args['target']='unknown'
        self.refuse('SPEND_PRIME',args)
        self.refuse('REFRESH_FIELDS',{'fields':[fields[0],fields[0]]},effect={'policy':'TRUSTED_MATCH_CONTROL'})

    def test_atomic_generation_spend_retry_and_lost_delivery(self):
        (source,target),fields=self.f.setup_player(primes=['restore_green','universal_green'],manifolds=['M-G-01'])
        self.f.active('player_1')
        for operation,args in [('GENERATE_FIELD',self.f.generate_args(fields[0],source)),('SPEND_PRIME',None)]:
            if args is None:args=self.f.spend_args(source,target,2,'RESTORE')
            request=self.f.request(operation,args);before=self.f.snapshot()
            for point in ['after_color_road','after_color_source','after_color_target','before_closure']:
                self.h.fault_hook=lambda p: (_ for _ in ()).throw(RuntimeError('fault')) if p==point else None
                try:
                    with self.assertRaises(Exception):self.h.execute(request,self.f.players['player_1'])
                finally:self.h.fault_hook=lambda _:None
                self.assertEqual(self.f.snapshot(),before)
            self.h.fault_hook=lambda p: (_ for _ in ()).throw(RuntimeError('lost')) if p=='after_commit' else None
            try:
                with self.assertRaises(Exception):self.h.execute(request,self.f.players['player_1'])
            finally:self.h.fault_hook=lambda _:None
            after=self.f.snapshot();receipt=self.h.execute(request,self.f.players['player_1'])
            self.assertEqual(receipt['status'],'COMMITTED');self.assertEqual(self.f.snapshot(),after)
        self.assertEqual(self.pair(source),(4,2));self.assertEqual(self.pair(target),(4,2))
        self.assertEqual(len(self.f.color.state['history']),2)

    def test_concurrent_use_spend_and_stale_object_revisions(self):
        (source,target),fields=self.f.setup_player(primes=['restore_green','universal_green'],manifolds=['M-G-01'])
        self.f.active('player_1')
        def race(operation,args):
            requests=[self.f.request(operation,args) for _ in range(2)]
            def run(request):
                try:return self.h.execute(request,self.f.players['player_1'])['status']
                except Exception:return 'REJECTED'
            with ThreadPoolExecutor(2) as pool:self.assertEqual(sorted(pool.map(run,requests)),['COMMITTED','REJECTED'])
        race('GENERATE_FIELD',self.f.generate_args(fields[0],source));self.assertEqual(self.pair(source),(4,4))
        old=self.f.spend_args(source,target,3,'RESTORE');race('SPEND_PRIME',old)
        self.assertEqual(self.pair(source),(4,1));self.assertEqual(self.pair(target),(4,3))
        old['amount']=1;self.refuse('SPEND_PRIME',old)
        self.refuse('SPEND_PRIME',self.f.spend_args(source,target,1,'RESTORE'),'player_2')

    def test_Genesis_admission_transform_and_Road_cannot_be_bypassed(self):
        (source,target),fields=self.f.setup_player(primes=['restore_green','universal_green'],manifolds=['M-G-01'])
        self.f.active('player_1')
        for operation,args in [('GENERATE_FIELD',self.f.generate_args(fields[0],source)),('SPEND_PRIME',None)]:
            if args is None:args=self.f.spend_args(source,target,1,'RESTORE')
            request=self.f.request(operation,args);before=self.f.snapshot()
            path=ROOT/'game/core/raeon/application'/self.f.manifest['operations'][operation]['source']
            key=path.relative_to(ROOT).as_posix();original=self.h._builds[key]
            changes=[('"fresh_revisions",',''),('  transform match with permission as candidate @{"operator":"COLLECTION_TRANSACTION"}',
                        '  en candidate : GEOMETRIC = instantiate fabric region mmo @bound_match')]
            for old,new in changes:
                modified=self.f.path/'mutated.gen';modified.write_text(path.read_text().replace(old,new),encoding='utf8')
                self.h._builds[key]=compile_paths([modified],ROOT,'mutated')
                try:
                    with self.assertRaises(Exception):self.h.execute(request,self.f.players['player_1'])
                finally:self.h._builds[key]=original
                self.assertEqual(self.f.snapshot(),before)
            service=self.h._backend.collections;run=service.run_unit
            service.run_unit=lambda name:None if name=='transport' else run(name)
            try:
                with self.assertRaises(Exception):self.h.execute(request,self.f.players['player_1'])
            finally:service.run_unit=run
            self.assertEqual(self.f.snapshot(),before)
            self.h.execute(request,self.f.players['player_1'])
        self.assertEqual(self.pair(target),(4,1))

    def test_selected_view_color_deltas_preserve_private_boundaries(self):
        (prime,),fields=self.f.setup_player(primes=['restore_green'],manifolds=['M-G-01'])
        self.f.active('player_1');self.f.perform('DRAW_ONE')
        hidden=self.f.members('player_1_hand')+self.f.members('player_1_deck')
        self.f.perform('INSPECT_TOP',{'source':'player_1_deck','count':1})
        self.f.players['public']=dict(self.f.players['player_1'],view_id='public')
        self.f.handles['public']=self.f.bridge.bind_session(self.f.players['public'])
        ports={who:self.f.hello(who) for who in self.f.players}
        request=self.f.request('GENERATE_FIELD',self.f.generate_args(fields[0],prime))
        owner_frames=self.f.send('player_1','INTENT',request)
        for who,port in ports.items():
            frames=owner_frames if who=='player_1' else self.f.send(who,'SYNC_REQUEST',{'view_id':port.view_id,'revision':port.revision})
            envelopes=[port.accept(frame) for frame in frames]
            self.assertIn('DELTA',[e['kind'] for e in envelopes])
            self.assertEqual(port.view,self.h._view(self.f.players[who]))
            text=json.dumps(envelopes)
            if who!='player_1':
                self.assertTrue(all(i not in text for i in hidden));self.assertNotIn('inspection',port.view)
            for key in ['segment_path','native_road','road_index','grants','effect_source']:
                self.assertNotIn(key,text)
            self.assertEqual(port.view['objects'][prime]['fields']['C'],4)
            self.assertEqual(port.view['objects'][fields[0]]['fields']['availability'],'USED')

    def test_J_checkpoint_restart_deterministic_replay_and_filtered_deltas(self):
        def story(f):
            (healer,target),fields=f.setup_player(primes=['restore_green','universal_green'],manifolds=['M-G-01'])
            (attacker,),af=f.setup_player('player_2',['degrade_yellow'],['M-Y-01'])
            f.active('player_1');f.generate(fields[0],healer);f.spend(healer,target,2,'RESTORE')
            f.active('player_2');f.generate(af[0],attacker,'player_2');f.spend(attacker,fields[0],3,'DEGRADE','player_2')
            f.refresh(af,'player_2');f.generate(af[0],attacker,'player_2')
            retry,_=f.spend(attacker,target,3,'DEGRADE','player_2')
            f.perform('DRAW_ONE');hidden=f.members('player_1_hand')+f.members('player_1_deck')
            f.perform('INSPECT_TOP',{'source':'player_1_deck','count':1})
            return healer,target,fields[0],retry,hidden
        healer,target,field,retry,hidden=story(self.f)
        self.assertEqual(self.pair(target),(3,0));self.assertEqual(self.pair(healer),(4,2))
        self.assertEqual((self.f.ext.state['fields'][field]['current_magnitude'],self.f.ext.state['fields'][field]['availability']),(1,'USED'))
        expected_root=self.h._state['root'];values=copy.deepcopy(self.h._backend.application_values);roads=copy.deepcopy(self.h._backend.road_history)
        other=PrimeFixture()
        try:
            story(other);self.assertEqual(other.horizon._state['root'],expected_root)
            self.assertEqual(other.horizon._backend.application_values,values)
        finally:other.close()
        public=dict(self.f.players['player_1'],view_id='public')
        self.f.players['public']=public;self.f.handles['public']=self.f.bridge.bind_session(public)
        for who in ['player_1','player_2','public']:
            port=self.f.hello(who);view=port.view;text=json.dumps(view)
            self.assertIn(target,view['objects']);self.assertEqual(view['objects'][target]['fields']['H'],3)
            self.assertEqual(view['objects'][field]['fields']['current_color'],'RED')
            if who!='player_1':
                self.assertNotIn('inspection',view);self.assertTrue(all(i not in text for i in hidden))
            for secret in ['segment_path','native_road','road_index','effect_source','grants']:
                self.assertNotIn(secret,text)
        hello_roads=len(self.h._backend.road_history)-len(roads)
        self.assertGreater(hello_roads,0)
        roads=copy.deepcopy(self.h._backend.road_history)
        def preserved(records):
            return [(self.f.color.road_commitment(r),r['timestamp_ns'],
                     [p['timestamp_ns'] for p in r['portal_receipts']]) for r in records]
        expected_roads=preserved(roads)
        checkpoint=self.h.checkpoint(self.f.owner);self.h.restore(checkpoint,self.f.owner)
        self.assertEqual(self.h._backend.application_values,values)
        self.assertEqual(preserved(self.h._backend.road_history),expected_roads)
        self.f.ext=self.h._backend.collections.extension
        self.f.restart();self.assertEqual(self.h._state['root'],expected_root)
        self.assertEqual(self.h._backend.application_values,values)
        current_roads=self.h._backend.road_history
        self.assertEqual(preserved(current_roads[:len(roads)]),expected_roads)
        self.assertEqual(len(current_roads)-len(roads),hello_roads)
        self.assertTrue(all(r['canonical_mmo_id']=='HORIZON:REFERENCE:request' for r in current_roads[len(roads):]))
        saved=self.f.snapshot();self.h.execute(retry,self.f.players['player_2']);self.assertEqual(self.f.snapshot(),saved)
        self.assertEqual(self.f.color.state['active_player'],'player_2')


if __name__=='__main__':unittest.main()
