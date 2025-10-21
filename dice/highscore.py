"""Simple JSON-backed high-score store keyed by player id (pid)."""
from __future__ import annotations
import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, Any, List


@dataclass
class HighScore:
    path: str = "public/highscores.json"
    _data: Dict[str, Dict[str, Any]] = field(default_factory=dict, init=False)

    def __post_init__(self) -> None:
        p = Path(self.path)
        if p.exists():
            try:
                self._data = json.loads(p.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                self._data = {}
        else:
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text("{}", encoding="utf-8")

    # ---- persistence helpers ----
    def _save(self) -> None:
        Path(self.path).write_text(json.dumps(self._data, indent=2), encoding="utf-8")

    # ---- public API ----
    def ensure(self, pid: str, name: str) -> None:
        rec = self._data.setdefault(pid, {"name": name, "games": 0, "wins": 0, "turns": 0, "points": 0})
        # Keep latest name but never lose stats
        rec["name"] = name
        self._save()

    def record_game(self, pid: str, name: str, won: bool, turns: int, total_points: int) -> None:
        self.ensure(pid, name)
        rec = self._data[pid]
        rec["games"] += 1
        rec["wins"] += 1 if won else 0
        rec["turns"] += max(0, int(turns))
        rec["points"] += max(0, int(total_points))
        self._save()

    def rename(self, pid: str, new_name: str) -> None:
        if pid in self._data:
            self._data[pid]["name"] = new_name
            self._save()

    def stats_for(self, pid: str) -> Dict[str, Any]:
        return dict(self._data.get(pid, {}))

    def top(self, n: int = 10) -> List[Dict[str, Any]]:
        rows = [
            {
                "pid": pid,
                **rec,
                "win_rate": (rec["wins"] / rec["games"]) if rec["games"] else 0.0,
            }
            for pid, rec in self._data.items()
        ]
        rows.sort(key=lambda r: (-r["wins"], -r["win_rate"], -r["points"]))
        return rows[:n]