import unittest
import dice

class TestInit(unittest.TestCase):
    def test_all_exports(self):
        expected = [
            "Die",
            "DiceHand",
            "Outcome",
            "evaluate_roll",
            "turn_points_gain",
            "Player",
            "Intelligence",
            "Computer",
            "Game",
        ]
        self.assertEqual(set(dice.__all__), set(expected))
        for name in expected:
            self.assertTrue(hasattr(dice, name), f"{name} is missing")

if __name__ == "__main__":
    unittest.main()