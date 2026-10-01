"""Independent integer examples and exhaustive bounded Prime-state checks."""
import importlib.util
import json
from types import SimpleNamespace
import unittest
from support import ROOT

spec=importlib.util.spec_from_file_location('pass04_math',ROOT/'game/primes/state.py')
math=importlib.util.module_from_spec(spec);spec.loader.exec_module(math)


class PrimeMath(unittest.TestCase):
    def test_catalog_exact_fourteen_and_accepted_magnitudes(self):
        catalog=json.loads((ROOT/'data/cycles/cycle_01/primes/status.json').read_text())['objects']
        self.assertEqual({(p['family'],p['maximum_magnitude']) for p in catalog},
            {(f,r) for f in ['Restore','Degrade'] for r in range(3,8)} | {('Universal',r) for r in range(1,5)})
        self.assertEqual(len(catalog),14)
        self.assertEqual(math.COLORS,[None,'RED','ORANGE','YELLOW','GREEN','BLUE','VIOLET','WHITE'])

    def test_all_health_charge_restore_degrade_states_and_overflow(self):
        add=lambda a,b:a+b
        for maximum in range(1,8):
            for h in range(maximum+1):
                for c in range(maximum+1 if h==maximum else 1):
                    state='INACTIVE' if h==0 else 'DAMAGED_NON_OPERATIONAL' if h<maximum else 'OPERATIONAL_CHARGED' if c else 'HEALTHY_UNCHARGED'
                    self.assertEqual(math.prime_state(h,c,maximum),state)
                    for amount in range(1,15):
                        remaining=max(0,h+c-amount)
                        expected_h=min(h,remaining);expected_c=max(0,remaining-h)
                        self.assertEqual(math.degrade(h,c,amount,add),(expected_h,expected_c))
                        if not h or h+c+amount>2*maximum:
                            with self.assertRaises(ValueError):math.restore(h,c,maximum,amount,add)
                        else:
                            total=h+c+amount
                            self.assertEqual(math.restore(h,c,maximum,amount,add),(min(maximum,total),max(0,total-maximum)))

    def test_carryover_uses_latest_pose_revision_independent_of_record_order(self):
        old={'id':'old','ordinary':True,'space':'space','qmo':'green','members':['copy'],
             'proof':{'dependency':{'pose_revision':2}},'current_magnitude':1,'current_color':'RED',
             'availability':'READY','refresh_serial':0}
        latest=dict(old,id='latest',proof={'dependency':{'pose_revision':8}},current_magnitude=4,
                    current_color='GREEN',availability='USED',refresh_serial=1)
        for rows in [(old,latest),(latest,old)]:
            with self.subTest(order=[r['id'] for r in rows]):
                mechanics=object.__new__(math.Mechanics)
                mechanics.t=SimpleNamespace(state={'fields':{r['id']:r for r in rows}})
                mechanics.s=SimpleNamespace(state={'color_primes':{'refresh_serial':1}})
                field={'ordinary':True,'space':'space','qmo':'green','members':['copy'],'native_color':'GREEN'}
                mechanics.field_created(field)
                self.assertEqual((field['color_predecessor'],field['current_magnitude'],field['availability']),
                                 ('latest',4,'USED'))

    def test_required_examples_and_bounded_white_reactivation(self):
        add=lambda a,b:a+b
        self.assertEqual(math.degrade(4,3,5,add),(2,0))
        self.assertEqual(math.restore(1,0,4,4,add),(4,1))
        self.assertEqual(math.prime_state(1,0,4),'DAMAGED_NON_OPERATIONAL')
        self.assertEqual(math.prime_state(1,0,1),'HEALTHY_UNCHARGED')
        for rank in range(1,8):
            with self.assertRaises(ValueError):math.restore(0,0,rank,1,add)

    def test_open_scheduler_overflow_and_nonordinary_production_not_invented(self):
        contract=json.loads((ROOT/'data/game/pass-04-runtime.json').read_text())
        match=json.loads((ROOT/'data/game/match.json').read_text())['values']
        self.assertIsNone(contract['initial_active_player']);self.assertFalse(contract['automatic_refresh'])
        self.assertEqual(contract['derived_and_emergent_generation'],'OPEN')
        self.assertEqual(contract['self_spend_targeting'],'OPEN_REJECTED')
        self.assertEqual(match['match_rules']['refresh_boundary'],'OPEN')
        self.assertFalse(match['match_rules']['active_end_refreshes_fields'])
        self.assertTrue(all(v=='OPEN' for v in match['turn_match_open'].values()))


if __name__=='__main__':unittest.main()
