import unittest
from unittest.mock import patch
from dice import dice_hand as dice_hand_module


class StubDie:
   def __init__(self, seq):
       self._it = iter(seq)
   def roll(self):
       return next(self._it)


class TestDiceHand(unittest.TestCase):
   def test_roll_two_dice(self):
       seqs = [[3], [5]]  # one value per die


       def factory(*args, **kwargs):
           return StubDie(seqs.pop(0))


       with patch.object(dice_hand_module, "Die", side_effect=factory):
           hand = dice_hand_module.DiceHand(count=2)
           vals = hand.roll()
           self.assertEqual(vals, (3, 5))


