"""Native closure/admission/Road negatives for the Pass06 gameplay path."""
import json
import unittest
from support import ROOT
from pass_06_support import HeadlessFixture,TRANSDUCTION
from raeon_genesis_horizon.toolchain import compile_paths


class Pass06Security(unittest.TestCase):
    def test_compiled_admission_closure_and_road_are_required(self):
        f=HeadlessFixture('pass06-source-closure')
        try:
            primes,_=f.setup_player(utilities=[TRANSDUCTION+'restore/0']);f.setup_player('player_2')
            f.setup();f.keep();f.start()
            card=f.utility(TRANSDUCTION+'restore/0')
            request=f.request('P6_UTILITY',f.utility_args(card,target=primes[0],direction='RESTORE'),effect=f.effect(card))
            before=f.snapshot();path=ROOT/'game/core/raeon/application/pass06_utility.gen';key=path.relative_to(ROOT).as_posix()
            original=f.horizon._builds[key] if key in f.horizon._builds else compile_paths([path],ROOT,path.stem)
            for old,new in [('"RAINBOW_ROAD",',''),
                ('  transform match with permission as candidate @{"operator":"COLLECTION_TRANSACTION"}',
                 '  en candidate : GEOMETRIC = instantiate fabric region mmo @bound_match')]:
                self.assertIn(old,path.read_text())
                modified=f.path/'mutated.gen';modified.write_text(path.read_text().replace(old,new),encoding='utf8')
                f.horizon._builds[key]=compile_paths([modified],ROOT,'mutated')
                try:
                    with self.assertRaises(Exception):f.horizon.execute(request,f.players['player_1'])
                finally:f.horizon._builds[key]=original
                self.assertEqual(f.snapshot(),before)
            service=f.horizon._backend.collections;run=service.run_unit
            service.run_unit=lambda name:None if name=='transport' else run(name)
            try:
                with self.assertRaises(Exception):f.horizon.execute(request,f.players['player_1'])
            finally:service.run_unit=run
            self.assertEqual(f.snapshot(),before)
            f.horizon.execute(request,f.players['player_1']);self.assertEqual(f.q(primes[0]),1)
            self.assertTrue(f.color.audit_road(f.horizon._backend.road_history[f.color.state['history'][-1]['road_index']])['pass'])
        finally:f.close()

    def test_exact_utility_registry_source_and_open_authority(self):
        contract=json.loads((ROOT/'data/game/pass-06-runtime.json').read_text())
        catalog=json.loads((ROOT/'game/core/raeon/application/catalog.json').read_text())['records']
        registry=contract['utilities']
        self.assertEqual(set(registry),{k for k,v in catalog.items() if v['category']=='Utility'})
        for handle,row in registry.items():
            self.assertEqual(row['record_sha256'],catalog[handle]['record_sha256'])
            self.assertEqual(row['source_sha256'],catalog[handle]['source_sha256'])
        self.assertEqual(sum(v['admission']=='MATURE' for v in registry.values()),32)
        self.assertEqual(sum(v['admission']=='RESERVED' for v in registry.values()),19)
        self.assertEqual(len(contract['open_items']),12)
        self.assertEqual(contract['accepted_rules']['defense_timer_seconds'],'CLIENT_TUNABLE_NOT_GENESIS_SEMANTIC')
