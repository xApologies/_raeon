"""Independent realization checks against the actual imported source corpora."""
import copy
import importlib.util
import math
import shutil
import tempfile
import unittest
from collections import Counter
from pathlib import Path

from support import ROOT


def load(path):
    spec=importlib.util.spec_from_file_location(path.stem,path)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    return module


class RealizationMath(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.module=load(ROOT/'game/qmo/realization.py')
        cls.corpus=load(ROOT/'game/qmo/corpus.py').Corpus(ROOT)
        cls.r=cls.module.Realization(ROOT,cls.corpus)

    def inputs(self, mid='M-R-02', phi=0, translation=(0,0), angle=0):
        w=self.r.witnesses[mid];copies={};poses={}
        for slot in w['generator_slots']:
            g=slot['field_generator'];i='copy-'+g;copies[i]=g;x,y=slot['xy']
            poses[i]={'revision':1,'value':{'x':round((math.cos(phi)*x-math.sin(phi)*y+translation[0])*10**9),
                'y':round((math.sin(phi)*x+math.cos(phi)*y+translation[1])*10**9),'xy_scale':10**9,
                'quaternion_wxyz':self.r.target(g,phi+math.radians(angle))}}
        return copies,poses

    def test_all_witness_memberships_edges_and_rotation_matrices(self):
        self.r.validate_authority()
        self.assertEqual(sum(len(w['required_cycle_edges']) for w in self.r.witnesses.values()),295)
        self.assertEqual(len(self.r.rotations),24)
        for mid in self.r.witnesses:
            c,p=self.inputs(mid);result=self.r.evaluate(mid,c,p)
            self.assertTrue(result['can_lock'],mid)
            self.assertLessEqual(result['rms_nano'],1)
            for edge in result['edges']:
                source=edge['source'];self.assertEqual(source,self.corpus.compatibility[tuple(sorted((source['a'],source['b'])))])
                self.assertIn(edge['selected_match'],source['matches'])
                selected=edge['selected_match']
                self.assertEqual(edge['a_face'],selected['a_face' if source['a']==c[edge['a']] else 'b_face'])
                self.assertEqual(edge['b_face'],selected['b_face' if source['b']==c[edge['b']] else 'a_face'])

    def test_se2_translation_rotation_exact_and_shared_yaw_targets(self):
        w=[[0,0],[1,0],[0.5,0.866025]]
        for phi,t in [(0,(0,0)),(0,(18,-31)),(1.234,(3,7)),(-2.01,(-3,-8))]:
            p=[[math.cos(phi)*x-math.sin(phi)*y+t[0],math.sin(phi)*x+math.cos(phi)*y+t[1]] for x,y in w]
            fit=self.module.se2(w,p)
            self.assertLess(fit['rms'],1e-14)
            c,p=self.inputs(phi=phi,translation=t)
            result=self.r.evaluate('M-R-02',c,p)
            self.assertTrue(result['can_lock'])
            self.assertLess(max(result['orientation_microdegrees'].values()),10)
            for target in result['targets'].values():
                q=target['quaternion_wxyz']
                self.assertEqual(math.gcd(*q),1)
                self.assertGreater(next(v for v in q if v),0)

    def test_reflection_scale_and_identity_permutation_are_not_equivalence(self):
        for operation in ('mirror','scale','permute'):
            c,p=self.inputs()
            if operation=='mirror':
                for v in p.values():v['value']['x']*=-1
            elif operation=='scale':
                for v in p.values():v['value']['x']*=2;v['value']['y']*=2
            else:
                a,b=list(p)[:2];p[a]['value'],p[b]['value']=p[b]['value'],p[a]['value']
            r=self.r.evaluate('M-R-02',c,p)
            self.assertFalse(r['shape_capture'],operation)
            self.assertFalse(r['can_lock'])

    def test_quaternion_sign_classes_and_thresholds(self):
        for row in self.r.rotations:
            q=row['quaternion_wxyz'];self.assertLess(self.module.distance(q,[-v for v in q]),0.00001)
        for angle,stage,capture in [(11.9,'MAGNETIZED',True),(12,'MAGNETIZED',True),(12.000001,'CANDIDATE',False),(12.1,'CANDIDATE',False),(29.9,'CANDIDATE',False),(30,'CANDIDATE',False),(30.000001,'FREE',False),(30.1,'FREE',False)]:
            c,p=self.inputs(angle=angle);r=self.r.evaluate('M-R-02',c,p)
            self.assertEqual(r['orientation_stage'],stage)
            self.assertEqual(r['orientation_capture'],capture)
        c,p=self.inputs();prior=self.r.evaluate('M-R-02',c,p)
        for angle,expected in [(34.9,'MAGNETIZED'),(35,'MAGNETIZED'),(35.000001,'FREE'),(35.1,'FREE')]:
            c,p=self.inputs(angle=angle);r=self.r.evaluate('M-R-02',c,p,prior)
            self.assertEqual(r['orientation_stage'],expected)
            self.assertFalse(r['can_lock'])

    def test_candidate_magnetization_release_and_shape_only_never_lock(self):
        c,p=self.inputs('M-R-01');prior=self.r.evaluate('M-R-01',c,p)
        # Move the middle labeled slot perpendicular to its band: error=2*d/3.
        middle=list(p)[1]
        for d,expected in [(0.4,'CANDIDATE'),(0.2,'MAGNETIZED'),(0.8,'FREE')]:
            q=copy.deepcopy(p);q[middle]['value']['y']=round(d*10**9)
            r=self.r.evaluate('M-R-01',c,q)
            self.assertEqual(r['shape_stage'],expected)
        for d,expected in [(0.7,'MAGNETIZED'),(0.73,'FREE')]:
            q=copy.deepcopy(p);q[middle]['value']['y']=round(d*10**9)
            r=self.r.evaluate('M-R-01',c,q,prior)
            self.assertEqual(r['shape_stage'],expected)
            self.assertFalse(r['can_lock'])
        c,p=self.inputs(angle=180);r=self.r.evaluate('M-R-02',c,p)
        self.assertEqual(r['shape_stage'],'MAGNETIZED');self.assertFalse(r['can_lock'])

    def test_simultaneous_edges_tethers_and_no_face_socket_exclusivity(self):
        c,p=self.inputs('M-R-01');r=self.r.evaluate('M-R-01',c,p)
        self.assertTrue(all(e['live'] for e in r['edges']))
        self.assertIn('COHERENCE_TETHER',[e['interaction'] for e in r['edges']])
        first=list(p)[0];p[first]['value']['quaternion_wxyz']=[0,1,0,0]
        r=self.r.evaluate('M-R-01',c,p)
        self.assertFalse(r['can_lock']);self.assertEqual(sum(e['live'] for e in r['edges']),1)
        # Every real witness captures, including repeated selected faces and non-90-degree boards.
        reused=False
        for mid in self.r.witnesses:
            c,p=self.inputs(mid);r=self.r.evaluate(mid,c,p);used=[]
            for e in r['edges']:
                m=e['selected_match'];s=e['source'];used.extend([(s['a'],m['a_face']),(s['b'],m['b_face'])])
            reused|=len(set(used))<len(used)
            self.assertTrue(r['can_lock'])
        self.assertTrue(reused)

    def test_membership_and_authority_tamper_fail_closed(self):
        c,p=self.inputs();c['extra']='FG-001'
        with self.assertRaisesRegex(ValueError,'MEMBERSHIP'):self.r.evaluate('M-R-02',c,p)
        for name in ('BASE_MANIFOLD_WITNESSES.json','ROTATION_CLASS_TABLE.json'):
            with tempfile.TemporaryDirectory(dir=ROOT/'build',prefix='r3b-') as tmp:
                root=Path(tmp)
                for rel in ['game/qmo/realization.lock.json',*self.r.lock['inputs']]:
                    target=root/rel;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(ROOT/rel,target)
                r=self.module.Realization(root,self.corpus)
                target=next(root/p for p in r.lock['inputs'] if p.endswith(name))
                target.write_bytes(target.read_bytes()+b' ')
                with self.assertRaisesRegex(ValueError,'INTEGRITY'):r.verify()
                target.unlink()
                with self.assertRaises(FileNotFoundError):self.module.Realization(root,self.corpus)
