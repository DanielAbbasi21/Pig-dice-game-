from __future__ import annotations
import random
from dataclasses import dataclass




@dataclass
class Die:
   """A single die with a configurable number of sides.


   Parameters
   ----------
   sides: int
       Number of sides on the die, default 6.
   rng: random.Random | None
       Optional random number generator, useful for testing.
   """


   sides: int = 6
   rng: random.Random | None = None


   def roll(self) -> int:
       """Roll the die and return a value in ``[1, sides]``."""
       r = self.rng if self.rng is not None else random
       return r.randint(1, self.sides)
