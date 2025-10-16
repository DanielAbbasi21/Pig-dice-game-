import unittest
from dice.dice import Die


class DummyRng:
   def __init__(self, seq):
       self._it = iter(seq)
   def randint(self, a, b):  # noqa: ARG002
       return next(self._it)


class TestDie(unittest.TestCase):
   def test_roll_in_range(self):
       d = Die()
       for _ in range(50):
           v = d.roll()
           self.assertTrue(1 <= v <= 6)


   def test_injected_rng_sequence(self):
       d = Die(rng=DummyRng([6, 5, 4]))
       self.assertEqual(d.roll(), 6)
       self.assertEqual(d.roll(), 5)
       self.assertEqual(d.roll(), 4)


   def test_sides_respected(self):
       d = Die(sides=8, rng=DummyRng([8, 1]))
       self.assertEqual(d.roll(), 8)
       self.assertEqual(d.roll(), 1)
