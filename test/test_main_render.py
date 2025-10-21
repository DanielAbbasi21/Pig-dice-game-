import unittest
import tempfile
from pathlib import Path
from dice.game import Game
from dice.player import Player
from dice.highscore import HighScore
from dice.main import render


class TestRender(unittest.TestCase):
   def test_render_has_turn_scores_and_total(self):
       with tempfile.TemporaryDirectory() as td:
           hs = HighScore(path=str(Path(td) / "hs.json"))
           g = Game(players=[Player("p1", "Mikael"), Player("p2", "Bot")], target=100, highs=hs)
           g.start()
           text = render(g)
           self.assertIn("Turn: Mikael", text)
           self.assertIn("Scores → Mikael: 0 | Bot: 0", text)
           self.assertIn("Turn total:", text)
