# dice/main.py
"""Text-based UI using cmd.Cmd. Keeps commands tiny & friendly."""
from __future__ import annotations
import cmd
import shlex
from typing import List, Tuple
from .game import Game
from .highscore import HighScore




BANNER = (
   "\n"
   "╔══════════════════════════════════════════════════════════════╗\n"
   "║                    Welcome to Pig Dice Game!                 ║\n"
   "╚══════════════════════════════════════════════════════════════╝\n"
   "\n"
   "Hello there, lucky roller!\n"
   "\n"
   "Your goal is to be the first to reach 100 points.\n"
   "\n"
   "Here’s how it works:\n"
   "  • Roll two dice each turn.\n"
   "  • Double ones (1 + 1): you lose ALL saved points — ouch!\n"
   "  • If one die shows 1, your turn ends and you keep the points you earned.\n"
   "  • Otherwise: add both dice and decide whether to roll again or hold.\n"
   "\n"
   "Type 'help' to see all available commands.\n"
   "Type 'start' to begin your game.\n"
   "\n"
   "Good luck and may the dice be ever in your favor!\n"
)


def render(game: Game) -> str:
   """Return a short text summary of the current game state."""
   p = game.players
   cur = game.current_player()
   lines = [
       "",
       f"Turn: {cur.name}",
       f"Scores → {p[0].name}: {p[0].score} | {p[1].name}: {p[1].score}",
       f"Turn total: {game.turn_total}"
       "\n",
   ]
   return "\n".join(lines)




class PigDiceGame(cmd.Cmd):
   """Command-line shell for the Pig Dice game."""
   intro = BANNER
   prompt = "(pig) "


   def __init__(self) -> None:
       super().__init__()
       self.highs = HighScore()
       self.game = Game.vs_computer()
       self.game.start()


   # ---- helpers ----
   def _println(self, *parts: str) -> None:
       for p in parts:
           if p is not None and p != "":
               print(p)


   # ---- commands ----
   def do_rules(self, arg: str) -> None:  # noqa: ARG002
       """Show the rules for this variant."""
       self._println(
           "Rules:",
           "  • Roll two dice each turn.",
           "  • Double ones (1+1): you lose all saved points; turn ends.",
           "  • If one die shows 1, your turn ends and you keep the points you earned.",
           "  • Otherwise: add both dice to your turn total and choose to roll/hold.",
           "  • First to 100 or more wins.",
       )


   def do_start(self, arg: str) -> None:
       """start [target] [ai=easy|medium|hard] — start/restart a game."""
       try:
           target = 100
           ai = "medium"
           for token in shlex.split(arg):
               if token.startswith("ai="):
                   ai = token.split("=", 1)[1]
               else:
                   target = int(token)
           self.game = Game.vs_computer(ai_level=ai, target=target)
           self.game.start()
           self._println("", "New game started!", render(self.game))
       except Exception as exc:  # pragma: no cover - resilience only
           self._println(f"Could not start: {exc}")


   def do_name(self, arg: str) -> None:
       """name <new name> — change your display name (keeps stats)."""
       name = arg.strip()
       if not name:
           self._println("\n""Enter your name: name <new name>""\n")
           return
       self.game.players[0].rename(name)
       self.highs.ensure(self.game.players[0].pid, self.game.players[0].name)
       self._println("\n"f"Hello, {self.game.players[0].name}!", render(self.game))


   def do_roll(self, arg: str) -> None:  # noqa: ARG002
       """Roll the dice for the current player. (Computer auto-plays its turn.)"""
       cur = self.game.current_player()
       if cur is self.game.players[1]:  # computer's turn (safety)
           self._ai_turn()
           return


       # Human roll
       d1, d2, msg = self.game.roll()


       # If your roll ended your turn (single/double 1), let the AI handle rendering
       if self.game.current_player() is self.game.players[1] and not self.game.winner():
           self._println(msg)        # show the roll result
           self._ai_turn()           # AI will render its own turn header/output
       else:
           self._println(msg, render(self.game))


       if self.game.winner():
           self._println("\n"f"🎉 {self.game.winner().name} wins!")


   def do_hold(self, arg: str) -> None:  # noqa: ARG002
       """Hold your current turn total."""
       cur = self.game.current_player()
       if cur is self.game.players[1]:
           self._println("It's not your turn.")
           return
       msg = self.game.hold()
       self._println(msg)
       if self.game.winner():
           self._println("\n"f"🎉 {self.game.winner().name} wins!""\n")
       else:
           self._ai_turn()  # AI will render once it starts


   def _ai_turn(self) -> None:
       """Let the computer play automatically until it holds or the turn ends."""
       acted = False
       while self.game.winner() is None and self.game.current_player() is self.game.players[1]:
           acted = True
           my = self.game.players[1]
           opp = self.game.players[0]


           # Always show the current state before the AI acts
           self._println(render(self.game))


           # decide whether to hold
           if getattr(my, "decide_hold")(self.game.turn_total, my.score, opp.score, self.game.target):
               msg = self.game.hold()
               self._println(f"Computer: {msg}")  # one-line
               break


           # otherwise roll  ← fixed indentation
           d1, d2, msg = self.game.roll()
           self._println(f"Computer: {msg}")      # one-line


           if self.game.winner():
               self._println("\n"f"🎉 {self.game.winner().name} wins!""\n")
               return


       # Show the board once more after the AI finishes (if no winner)
       if acted and not self.game.winner():
           self._println(render(self.game))


   def do_highscore(self, arg: str) -> None:  # noqa: ARG002
       """Show high-score table (top 10)."""
       rows = self.highs.top(10)
       if not rows:
           self._println("No games recorded yet.")
           return
       self._println("Leaderboard (wins, games, win%, points):")
       for i, r in enumerate(rows, 1):
           pct = f"{100*r['win_rate']:.0f}%"
           self._println(f" {i:>2}. {r['name']:<15}  {r['wins']:>3}/{r['games']:<3}  {pct:>4}  {r['points']:>5}")


   def do_cheat(self, arg: str) -> None:
       """cheat <d1> <d2> [; <d1> <d2> ...] — queue up future rolls.


       Example: cheat 6 6; 6 6; 1 1
       """
       try:
           batches: List[Tuple[int, int]] = []
           for chunk in arg.split(";"):
               parts = [p for p in chunk.strip().split() if p]
               if not parts:
                   continue
               if len(parts) != 2:
                   raise ValueError("each chunk must be two ints")
               batches.append((int(parts[0]), int(parts[1])))
           self.game.set_cheat(batches)
           self._println("\n"f"Queued {len(batches)} scripted rolls.")
       except Exception as exc:  # pragma: no cover - resilience only
           self._println("\n"f"Cheat parse error: {exc}")


   def do_show(self, arg: str) -> None:  # noqa: ARG002
       """Show current state."""
       self._println(render(self.game))


   def do_help(self, arg: str) -> None:  # noqa: ARG002
       """Show all commands with short descriptions."""
       if arg:  # built-in detail for help <command>
           super().do_help(arg)
           return
       self._println(
           "",
           "\n"
           "Available Commands:",
           "───────────────────",
           "cheat       → queue specific dice rolls for testing",
           "help        → show this help message",
           "highscore   → display the high-score leaderboard",
           "hold        → hold your current turn total and save points",
           "name        → change your player name (write the word 'name' and the your name)",
           "quit        → exit the game",
           "roll        → roll the dice for your turn",
           "rules       → show the game rules",
           "show        → display the current game state",
           "start       → start or restart a new game",
           "",
           "\n"
           "Tip: type a command and press Enter (example: roll)",
       )


   def do_quit(self, arg: str) -> bool:  # noqa: ARG002
       """Quit the game shell."""
       self._println("", "\n" "Bye!")
       return True


   def default(self, line: str) -> None:  # pragma: no cover - UX only
       """Handle unknown commands gracefully."""
       self._println("\n"f"Unknown command: {line}")




if __name__ == "__main__":
   PigDiceGame().cmdloop()



