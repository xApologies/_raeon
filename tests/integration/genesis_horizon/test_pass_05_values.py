"""Supplemental native INT/codec checks; full gameplay is in test_pass_05.py."""
import importlib.util
import hashlib
import json
import sys
import unittest
from support import ROOT
from raeon_genesis_horizon.toolchain import initialize
from raeon_genesis_horizon.values import IntegerInterpreter

spec=importlib.util.spec_from_file_location('pass05_nodes',ROOT/'game/primes/nodes.py')
nodes=importlib.util.module_from_spec(spec);spec.loader.exec_module(nodes)


class NodeValues(unittest.TestCase):
    def setUp(self):
        _,upstream,_=initialize(ROOT)
        self.vm=IntegerInterpreter(upstream,ROOT/'game/core/genesis_horizon/src/values')
        self.values=nodes.Values(self.vm)

    def prime(self,h,n,r,rank):
        return {'H':h,'N':n,'R':r,'H_max':rank,'revision':0,'state':nodes.state(h,n*rank+r,rank)}

    def test_exact_authority_pointer_amendments_do_not_allow_corpus_changes(self):
        sys.path.insert(0,str(ROOT/'tools'))
        from genesis_runtime_pass05 import approved_authority_pointer
        decision=json.loads((ROOT/'provenance/decisions/raeon-pass-05.json').read_text(encoding='utf8'))
        paths=['data/cycles/cycle_01/primes/working-model.json','data/cycles/cycle_01/utilities/overview.json',
               'design/cards/cycle_01/utilities/SYSTEM.md','design/game/board/SYSTEM.md','design/game/match/SYSTEM.md']
        for path in paths:
            row=decision['changes'][path];actual=hashlib.sha256((ROOT/path).read_bytes()).hexdigest()
            with self.subTest(path=path):
                self.assertTrue(approved_authority_pointer(path,row['before_sha256'],actual))
                self.assertFalse(approved_authority_pointer(path,'0'*64,actual))
                self.assertFalse(approved_authority_pointer(path,row['before_sha256'],'0'*64))
                self.assertFalse(approved_authority_pointer(path.upper(),row['before_sha256'],actual))
                for protected in ['data/qmo/cycle1/manifold_pair_relations.json','mathematics/unknown.json',
                                  'data/cycles/cycle_01/utilities/catalog.json','design/game/unknown.md']:
                    self.assertFalse(approved_authority_pointer(protected,row['before_sha256'],actual))

    def test_native_integer_no_node_cap_and_exact_canonical_encoding(self):
        n=2**100+17;p=self.prime(3,n,2,3)
        self.values.validate(p)
        result=self.values.restore(p,10**60)
        self.assertEqual(result,(3,*divmod(n*3+2+10**60,3)))
        p=self.prime(*[3,result[1],result[2],3])
        spent=self.values.spend(p,10**60)
        self.assertEqual(spent,(3,n,2))
        self.assertTrue(self.vm.receipts)
        self.assertTrue(all(r['receipt']['payload']['verified'] for r in self.vm.receipts))
        with self.assertRaises(ValueError):self.vm.run('add',2**100,1)
        self.assertEqual(self.vm.run_integer('add',2**100,1),2**100+1)

    def test_negative_node_invariants_and_legacy_charge_rejected(self):
        for changes in [{'N':-1},{'N':1.0},{'N':True},{'R':3},{'R':-1},{'H':2},{'H':0},{'C':0},{'C_max':3}]:
            p=self.prime(3,1,0,3);p.update(changes)
            with self.subTest(changes=changes),self.assertRaises(ValueError):self.values.validate(p)

    def test_native_health_first_shield_first_partial_spend_and_states(self):
        for rank in range(1,8):
            p=self.prime(rank,2,rank-1,rank);q=nodes.quantity(p)
            for amount in (1,rank,q,q+1,q+rank+1):
                h,n,r=self.values.degrade(p,amount)
                self.assertEqual((h,n*rank+r),(max(0,rank-max(0,amount-q)),max(0,q-amount)))
            for h in range(1,rank+1):
                p=self.prime(h,0,0,rank)
                result=self.values.restore(p,rank+2)
                self.assertEqual(result,(rank,*divmod(h+2,rank)))
            self.assertEqual(nodes.state(0,0,rank),'INACTIVE')
            self.assertEqual(nodes.state(rank,0,rank),'HEALTHY_UNCHARGED')
            self.assertEqual(nodes.state(rank,1,rank),'OPERATIONAL_CHARGED')
        self.assertEqual(nodes.state(1,0,3),'DAMAGED_NON_OPERATIONAL')


if __name__=='__main__':unittest.main()
