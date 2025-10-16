# dice/computer.py
"""The computer opponent and a simple, configurable strategy."""
from __future__ import annotations
from dataclasses import dataclass




@dataclass
class Intelligence:
   """Threshold-based strategy with a tiny bit of endgame awareness.


   Hold when turn_total >= risk_threshold or when holding would win.
   """


   risk_threshold: int = 20


   def should_hold(self, turn_total: int, my_score: int, opp_score: int, target: int) -> bool:  # noqa: ARG002
       if my_score + turn_total >= target:
           return True
       return turn_total >= self.risk_threshold




class ComputerError(RuntimeError):
   """Raised when the Computer is used without a brain."""




@dataclass
class Computer:
   """Computer is-a Player but delegates to an :class:`Intelligence`."""


   pid: str
   name: str
   brain: Intelligence
   score: int = 0


   # Matching Player API used by Game
   def rename(self, new_name: str) -> None:  # pragma: no cover - trivial
       self.name = new_name


   def add_points(self, pts: int) -> None:  # pragma: no cover - trivial
       self.score += max(0, int(pts))


   def reset_score(self) -> None:  # pragma: no cover - trivial
       self.score = 0


   # Decision
   def decide_hold(self, turn_total: int, my_score: int, opp_score: int, target: int) -> bool:
       if not self.brain:
           raise ComputerError("Computer has no brain configured")
       return self.brain.should_hold(turn_total, my_score, opp_score, target)
