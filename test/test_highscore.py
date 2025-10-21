import unittest
import tempfile
from pathlib import Path
from dice.highscore import HighScore

class TestHighScore(unittest.TestCase):
    def test_persist_and_rename(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "hs.json"
            hs = HighScore(path=str(p))
            hs.ensure("pid1", "Mikael")
            hs.record_game("pid1", "Mikael", True, turns=5, total_points=100)
            hs.rename("pid1", "Mikaela")

            hs2 = HighScore(path=str(p))
            stats = hs2.stats_for("pid1")
            self.assertEqual(stats["name"], "Mikaela")
            self.assertEqual(stats["games"], 1)
            self.assertEqual(stats["wins"], 1)
            self.assertEqual(stats["turns"], 5)
            self.assertEqual(stats["points"], 100)

            top = hs2.top(10)
            self.assertEqual(len(top), 1)
            self.assertEqual(top[0]["name"], "Mikaela")
            self.assertEqual(top[0]["wins"], 1)
