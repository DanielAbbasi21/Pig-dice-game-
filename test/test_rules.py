import unittest
from dice.rules import Outcome, evaluate_roll, turn_points_gain

class TestRules(unittest.TestCase):
    def test_double_ones_is_bust_all(self):
        self.assertEqual(evaluate_roll(1, 1), Outcome.BUST_ALL)
        self.assertEqual(turn_points_gain(1, 1), 0)

    def test_single_one_is_auto_hold(self):
        for other in range(2, 7):
            self.assertEqual(evaluate_roll(1, other), Outcome.AUTO_HOLD)
            self.assertEqual(evaluate_roll(other, 1), Outcome.AUTO_HOLD)
            self.assertEqual(turn_points_gain(1, other), 0)
            self.assertEqual(turn_points_gain(other, 1), 0)

    def test_continue_when_no_ones_and_gain_is_sum(self):
        for d1 in range(2, 7):
            for d2 in range(2, 7):
                self.assertEqual(evaluate_roll(d1, d2), Outcome.CONTINUE)
                self.assertEqual(turn_points_gain(d1, d2), d1 + d2)