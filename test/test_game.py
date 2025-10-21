import unittest
import tempfile
from pathlib import Path
from dice.game import Game
from dice.player import Player
from dice.highscore import HighScore


def make_game(tmpdir, target=100):
   hs = HighScore(path=str(Path(tmpdir) / "hs.json"))
   g = Game(players=[Player("p1", "P1"), Player("p2", "P2")], target=target, highs=hs)
   g.start()
   return g


class TestGame(unittest.TestCase):
   def test_continue_then_hold(self):
       with tempfile.TemporaryDirectory() as td:
           g = make_game(td)
           g.set_cheat([(4, 5)])  # +9
           d1, d2, msg = g.roll()
           self.assertEqual((d1, d2), (4, 5))
           self.assertIn("total 9", msg)
           msg = g.hold()
           self.assertIn("holds 9", msg)
           self.assertEqual(g.players[0].score, 9)
           self.assertIs(g.current_player(), g.players[1])


   def test_single_one_auto_hold(self):
       with tempfile.TemporaryDirectory() as td:
           g = make_game(td)
           g.set_cheat([(3, 3), (1, 5)])  # +6 then single-1
           g.roll()
           _, _, msg2 = g.roll()
           self.assertIn("single 1", msg2)
           self.assertEqual(g.players[0].score, 6)
           self.assertIs(g.current_player(), g.players[1])


   def test_double_ones_resets_points(self):
       with tempfile.TemporaryDirectory() as td:
           g = make_game(td)
           g.players[0].add_points(20)
           g.set_cheat([(1, 1)])
           _, _, msg = g.roll()
           self.assertIn("double ones", msg)
           self.assertEqual(g.players[0].score, 0)
           self.assertIs(g.current_player(), g.players[1])


   def test_winning_on_hold_sets_winner(self):
       import tempfile
       with tempfile.TemporaryDirectory() as td:
           # Use a target that matches two clean +12 turns
           g = make_game(td, target=24)


           # Turn 1 (P1): 6+6 => +12, then hold -> P1 score = 12
           g.set_cheat([(6, 6)])
           g.roll()
           g.hold()


           # Turn 2 (P2): just pass the turn (hold 0) to get back to P1
           g.hold()


           # Turn 3 (P1): 6+6 => +12, then hold -> P1 score = 24 => win
           g.set_cheat([(6, 6)])
           g.roll()
           msg = g.hold()


           self.assertIn("wins", msg)
           self.assertIs(g.winner(), g.players[0])


   def test_cheat_queue_in_order(self):
       with tempfile.TemporaryDirectory() as td:
           g = make_game(td)
           g.set_cheat([(2, 3), (4, 5), (6, 6)])
           self.assertEqual(g._roll_dice(), (2, 3))
           self.assertEqual(g._roll_dice(), (4, 5))
           self.assertEqual(g._roll_dice(), (6, 6))
