# dice/player.py
"""Player model used by the game and high-score system."""
from __future__ import annotations
from dataclasses import dataclass, field




@dataclass
class Player:
   """A human player with a stable id and mutable display name."""


   pid: str
   name: str
   score: int = field(default=0, init=False)


   def rename(self, new_name: str) -> None:
       self.name = new_name.strip() or self.name


   def add_points(self, pts: int) -> None:
       self.score += max(0, int(pts))


   def reset_score(self) -> None:
       self.score = 0
