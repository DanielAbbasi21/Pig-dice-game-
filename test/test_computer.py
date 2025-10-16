import unittest
from dice.computer import Intelligence, Computer, ComputerError


class TestComputer(unittest.TestCase):
   def test_intelligence_threshold_and_endgame(self):
       brain = Intelligence(risk_threshold=20)
       self.assertFalse(brain.should_hold(15, 50, 0, 100))
       self.assertTrue(brain.should_hold(20, 50, 0, 100))
       self.assertTrue(brain.should_hold(12, 90, 0, 100))  # would win


   def test_computer_decide_hold(self):
       brain = Intelligence(risk_threshold=10)
       bot = Computer("pid-bot", "Computer", brain)
       self.assertFalse(bot.decide_hold(5, 0, 0, 100))
       self.assertTrue(bot.decide_hold(11, 0, 0, 100))


   def test_computer_without_brain_raises(self):
       bot = Computer("pid-bot", "Computer", brain=None)  # type: ignore[arg-type]
       with self.assertRaises(ComputerError):
           bot.decide_hold(10, 0, 0, 100)
