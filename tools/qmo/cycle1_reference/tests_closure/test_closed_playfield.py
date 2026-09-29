import json, sqlite3, unittest, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"closure"))
import closure_api
DB=ROOT/"database"/"RAEON_QMO_v0_2.sqlite"

class TestClosedPlayfield(unittest.TestCase):
    def setUp(self):
        self.c=sqlite3.connect(DB); self.c.row_factory=sqlite3.Row
    def tearDown(self): self.c.close()
    def test_all_1770_pairs_explicit(self):
        self.assertEqual(self.c.execute("select count(*) from manifold_pair_relations").fetchone()[0],1770)
    def test_no_null_emergent_status(self):
        self.assertEqual(self.c.execute("select count(*) from manifold_pair_relations where emergent_status is null").fetchone()[0],0)
    def test_fusion_status_domain(self):
        vals={r[0] for r in self.c.execute("select distinct fusion_status from manifold_pair_relations")}
        self.assertTrue(vals <= {"VALID","TERMINATES","NOT_APPLICABLE"})
    def test_red_yellow_total(self):
        ms={r["manifold_id"]:r["native_color"] for r in self.c.execute("select manifold_id,native_color from manifold_qmos")}
        rows=self.c.execute("select a_manifold,b_manifold from manifold_pair_relations").fetchall()
        n=sum(1 for r in rows if {ms[r["a_manifold"]],ms[r["b_manifold"]]}=={"RED","YELLOW"})
        self.assertEqual(n,165)
    def test_valid_fusion_has_derived_qmo(self):
        for r in self.c.execute("select fusion_result_qmo from manifold_pair_relations where fusion_status='VALID' limit 20"):
            self.assertIsNotNone(closure_api.derived(r["fusion_result_qmo"]))
    def test_valid_emergent_has_derived_qmo(self):
        for r in self.c.execute("select emergent_qmo from manifold_pair_relations where emergent_status='VALID' limit 20"):
            self.assertIsNotNone(closure_api.derived(r["emergent_qmo"]))
if __name__=="__main__": unittest.main()
