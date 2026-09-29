import unittest
from raeon_model.colors import Color
from raeon_model.prime import PrimeState, PrimeDirection
from raeon_model.rules import manifold_color_for_generator_count, white_only_manifold_color
from raeon_model.sandbox import Sandbox, GeneratorRef, merge_sandboxes

class TestRaeonCore(unittest.TestCase):

    def test_color_scale(self):
        self.assertEqual(int(Color.RED), 1)
        self.assertEqual(int(Color.VIOLET), 6)
        self.assertEqual(int(Color.WHITE), 7)

    def test_manifold_ladder(self):
        self.assertEqual(manifold_color_for_generator_count(3), Color.RED)
        self.assertEqual(manifold_color_for_generator_count(8), Color.VIOLET)

    def test_white_generators_do_not_make_white_by_count(self):
        self.assertEqual(white_only_manifold_color(8), Color.VIOLET)

    def test_blue_into_red_health_yellow_prime(self):
        p = PrimeState(rank=Color.YELLOW, health=Color.RED, shield=0)
        r = p.receive_friendly_color(Color.BLUE)
        self.assertEqual(p.health, 3)
        self.assertEqual(p.shield, 3)
        self.assertEqual(r["overflow"], 0)

    def test_degradation_hits_shield_then_health(self):
        p = PrimeState(rank=Color.YELLOW, health=3, shield=3)
        r = p.receive_degradation(Color.BLUE)  # 5
        self.assertEqual(r["shield_lost"], 3)
        self.assertEqual(r["health_lost"], 2)
        self.assertEqual(p.health, 1)
        self.assertFalse(p.destroyed)

    def test_spend_shield_reduces_protection(self):
        p = PrimeState(rank=Color.VIOLET, shield=Color.VIOLET,
                       direction=PrimeDirection.HYBRID)
        p.spend_transduction(Color.GREEN, "degrade")
        self.assertEqual(p.shield, Color.ORANGE)

    def test_generator_is_committed(self):
        s = Sandbox("A")
        s.add_generator(GeneratorRef("FG-009"))
        with self.assertRaises(ValueError):
            s.remove_generator("FG-009")

    def test_merge_preserves_generators(self):
        a, b = Sandbox("A"), Sandbox("B")
        a.add_generator(GeneratorRef("FG-001"))
        b.add_generator(GeneratorRef("FG-002"))
        c = merge_sandboxes("AB", a, b)
        self.assertEqual([g.card_id for g in c.generators], ["FG-001", "FG-002"])

if __name__ == "__main__":
    unittest.main()
