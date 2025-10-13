# dice/rules.py
"""Pure game rules for the two-dice Pig variant used in the assignment.


Rules summary (this module encodes only *outcomes* of a roll):
- Double ones (1+1): player loses their saved score, turn ends.
- Single one (1 with 2-6): auto-hold current turn total, turn ends.
- Otherwise: add sum to turn total and continue.
"""
from __future__ import annotations
from enum import Enum, auto




class Outcome(Enum):
   """Outcome of a two-dice roll under our rules."""


   BUST_ALL = auto()  # 1+1 -> lose all saved points
   AUTO_HOLD = auto()  # single 1 -> save current turn total automatically
   CONTINUE = auto()  # add both dice to turn total and continue




def evaluate_roll(d1: int, d2: int) -> Outcome:
   """Classify a two-dice roll into an :class:`Outcome`.


   Parameters
   ----------
   d1, d2:
       Values of the two dice, 1..6.
   """
   if d1 == 1 and d2 == 1:
       return Outcome.BUST_ALL
   if d1 == 1 or d2 == 1:
       return Outcome.AUTO_HOLD
   return Outcome.CONTINUE




def turn_points_gain(d1: int, d2: int) -> int:
   """Return the points to add to *turn total* from a roll.


   Zero on BUST or AUTO_HOLD, otherwise the sum of the dice.
   """
   return 0 if 1 in (d1, d2) else d1 + d2