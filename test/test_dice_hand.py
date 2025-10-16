"""A small helper that rolls multiple dice at once."""
from __future__ import annotations
from typing import Tuple
from dataclasses import dataclass
from .dice import Die




@dataclass
class DiceHand:
   """A hand of N dice. Default is the two dice used in Pig variant."""


   count: int = 2


   def __post_init__(self) -> None:
       self._dice = [Die() for _ in range(self.count)]


   def roll(self) -> Tuple[int, ...]:
       """Roll all dice and return a tuple of their values."""
       return tuple(d.roll() for d in self._dice)
