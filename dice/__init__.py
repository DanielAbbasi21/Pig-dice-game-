"""Pig Dice Game package.


Expose handy top-level imports for convenience when using the package as a module.
"""
from .dice import Die
from .dice_hand import DiceHand
from .rules import Outcome, evaluate_roll, turn_points_gain
from .player import Player
from .computer import Intelligence, Computer
from .game import Game


__all__ = [
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
