import unittest
from dice.player import Player


class TestPlayer(unittest.TestCase):
   def test_player_rename_and_score_ops(self):
       p = Player("pid-1", "Mikael")
       self.assertEqual(p.name, "Mikael")
       self.assertEqual(p.score, 0)


       p.rename("Mikaela")
       self.assertEqual(p.name, "Mikaela")


       p.add_points(10)
       self.assertEqual(p.score, 10)


       p.add_points(-5)  # should not reduce score
       self.assertEqual(p.score, 10)


       p.reset_score()
       self.assertEqual(p.score, 0)
