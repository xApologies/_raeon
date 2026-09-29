import json, sys, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"render"))
from render_spec import build_render_spec

class TestRenderSpec(unittest.TestCase):
    def test_yellow_spec(self):
        s=build_render_spec("M-Y-01")
        self.assertEqual(s["native_color"],"YELLOW")
        self.assertEqual(s["generator_count"],5)
        self.assertEqual(len(s["anchors"]),5)
        self.assertGreaterEqual(len(s["spline_edges"]),1)
    def test_deterministic(self):
        a=build_render_spec("M-Y-03")
        b=build_render_spec("M-Y-03")
        self.assertEqual(a,b)
    def test_all_specs_exist(self):
        cat=json.loads((ROOT/"data"/"render_catalog.json").read_text())
        self.assertEqual(len(cat),60)
        for r in cat:
            self.assertTrue((ROOT/r["render_spec"]).exists())
    def test_color_count_alignment(self):
        cat=json.loads((ROOT/"data"/"render_catalog.json").read_text())
        want={"RED":15,"ORANGE":13,"YELLOW":11,"GREEN":9,"BLUE":7,"VIOLET":5}
        got={}
        for x in cat: got[x["native_color"]]=got.get(x["native_color"],0)+1
        self.assertEqual(got,want)
if __name__=="__main__": unittest.main()
