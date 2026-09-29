import json, sqlite3, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
DB=ROOT/'database'/'RAEON_QMO_v0_2.sqlite'
class TestRaeonQMO(unittest.TestCase):
    def setUp(self):
        self.c=sqlite3.connect(DB); self.c.row_factory=sqlite3.Row
    def tearDown(self): self.c.close()
    def test_120_generators(self): self.assertEqual(self.c.execute('select count(*) from generator_cards').fetchone()[0],120)
    def test_60_manifolds(self): self.assertEqual(self.c.execute('select count(*) from manifold_qmos').fetchone()[0],60)
    def test_four_four(self):
        for r in self.c.execute('select occupancy,void_sites from generator_cards'):
            self.assertEqual(len(json.loads(r['occupancy'])),4); self.assertEqual(len(json.loads(r['void_sites'])),4)
    def test_distribution(self):
        got={r[0]:r[1] for r in self.c.execute('select native_color,count(*) from manifold_qmos group by native_color')}
        self.assertEqual(got,{'RED':15,'ORANGE':13,'YELLOW':11,'GREEN':9,'BLUE':7,'VIOLET':5})
    def test_sizes(self):
        for r in self.c.execute('select generator_count,generators_json from manifold_qmos'):
            self.assertEqual(r['generator_count'],len(json.loads(r['generators_json'])))
    def test_edges(self):
        rels={r[0] for r in self.c.execute('select distinct relation from edges')}
        self.assertTrue({'DERIVED_FROM','CHIRALITY_COMPATIBLE_WITH','PARTICIPATES_IN','USES_GENERATOR'} <= rels)
if __name__=='__main__': unittest.main()
