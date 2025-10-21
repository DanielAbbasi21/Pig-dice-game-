# dice/game.py
"""Game engine coordinating players, rules and dice.


This class contains no I/O; the CLI in ``main.py`` handles printing.
"""
from __future__ import annotations
import itertools as it
import uuid
from dataclasses import dataclass, field
from typing import List, Optional, Tuple


from .dice_hand import DiceHand
from .player import Player
from .computer import Computer, Intelligence
from .rules import evaluate_roll, turn_points_gain, Outcome
from .highscore import HighScore




@dataclass
class Game:
   players: List[Player]
   target: int = 100
   dice: DiceHand = field(default_factory=DiceHand)
   highs: Optional[HighScore] = None


   def __post_init__(self) -> None:
       self.highs = self.highs or HighScore()
       self.turn_total = 0
       self.turns_taken = 0
       self._current_idx = 0
       self._winner: Optional[Player] = None
       self._cheat_queue: List[Tuple[int, int]] = []


   # ---- lifecycle ----
   @classmethod
   def vs_computer(cls, human_name: str = "You", ai_level: str = "medium", target: int = 100) -> "Game":
       level = {"easy": 15, "medium": 20, "hard": 25}.get(ai_level, 20)
       p1 = Player(str(uuid.uuid4()), human_name)
       bot = Computer(str(uuid.uuid4()), "Computer", Intelligence(level))
       return cls([p1, bot], target=target)


   def start(self) -> None:
       for p in self.players:
           p.reset_score()
       self.turn_total = 0
       self.turns_taken = 0
       self._current_idx = 0
       self._winner = None
       self._cheat_queue.clear()


   # ---- properties ----
   def current_player(self) -> Player:
       return self.players[self._current_idx]


   def opponent(self) -> Player:
       return self.players[1 - self._current_idx]


   def winner(self) -> Optional[Player]:
       return self._winner


   # ---- helpers ----
   def _next_player(self) -> None:
       self._current_idx = 1 - self._current_idx
       self.turn_total = 0


   def set_cheat(self, next_rolls: List[Tuple[int, int]]) -> None:
       self._cheat_queue = list(next_rolls)


   def _roll_dice(self) -> Tuple[int, int]:
       if self._cheat_queue:
           return self._cheat_queue.pop(0)
       d1, d2 = self.dice.roll()
       return int(d1), int(d2)


   # ---- actions ----
   def roll(self) -> Tuple[int, int, str]:
       if self._winner:
           return (0, 0, f"Game over. {self._winner.name} already won.")


       d1, d2 = self._roll_dice()
       outcome = evaluate_roll(d1, d2)
       message = ""


       if outcome is Outcome.CONTINUE:
           gain = turn_points_gain(d1, d2)
           self.turn_total += gain
           message = "\n"f"Rolled {d1}+{d2} → +{gain} this turn (total {self.turn_total})."
       elif outcome is Outcome.AUTO_HOLD:
           message = "\n"f"Rolled {d1}+{d2} (single 1) → auto-hold {self.turn_total}."
           self.hold(auto=True)
       else:  # BUST_ALL
           self.current_player().reset_score()
           message = "\n"f"Rolled {d1}+{d2} (double ones) → lose all saved points!"
           self._next_player()
           self.turns_taken += 1
       return d1, d2, message


   def hold(self, auto: bool = False) -> str:
       if self._winner:
           return "\n"f"Game over. {self._winner.name} already won."
       player = self.current_player()
       player.add_points(self.turn_total)
       msg = f"{player.name} holds {self.turn_total}. New score: {player.score}."
       if player.score >= self.target:
           self._winner = player
           msg += "\n"f" \n{player.name} wins!"
           # update highscores
           if self.highs:
               self.highs.record_game(player.pid, player.name, True, self.turns_taken + 1, player.score)
               self.highs.record_game(self.opponent().pid, self.opponent().name, False, self.turns_taken + 1, self.opponent().score)
       self._next_player()
       self.turns_taken += 1
       return msg
