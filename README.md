# Pig Dice Game

We have created a **text-based Pig Dice Game** implemented in **Python** using **object-oriented programming (OOP)** principles.  
The game runs directly in the terminal using Python’s built-in `cmd` module and follows a modified version of the traditional Pig dice rules.  

This project demonstrates:
- Clean OOP design  
- Command-line interface programming  
- Persistent data storage  
- Test-driven development  
- Automated documentation practices  

---

## Table of Contents

1. [Overview](#overview)  
2. [Game Rules](#game-rules)  
3. [Installation and Setup](#installation-and-setup)  
   - [Clone or download the repository](#clone-or-download-the-repository)  
   - [How to create a virtual environment](#how-to-create-a-virtual-environment)  
   - [How to install dependencies](#how-to-install-dependencies)  
4. [How to Run the Game](#how-to-run-the-game)  
5. [How to Run All Tests](#how-to-run-all-tests)  
6. [Author and License](#author-and-license)

---

## Overview

The **Pig Dice Game** was developed as part of the *Methods for Sustainable Programming* course assignment.  

It’s designed to demonstrate:
- The use of **object-oriented programming** in Python.  
- Clean and maintainable **software architecture**.  
- Implementation of **unit tests** using the built-in `unittest` framework.  
- A clear **command-line user interface**.  
- Documentation and structure that enable easy extension by other developers.  

The game allows **one human player** to play against a **computer opponent** with configurable difficulty.

---

## Game Rules

- **Goal:** Reach **100 points** or more before the computer does.  
- **Double ones (1 + 1):** You lose all saved points and your turn ends.  
- **Single one (1 + 2–6):** Your turn ends automatically, but you keep the points you’ve earned.  
- **Otherwise:** Add both dice to your *turn total* and choose to roll again or hold.  
- The computer automatically plays its turn based on an AI “risk threshold”.

---

## Installation and Setup

### Clone or download the repository
```bash
git clone https://github.com/DanielAbbasi21/Pig-dice-game-
cd Pig-dice-game-
````
---
## How to create a virtual environment

````bash
python -m venv .venv
source .venv/bin/activate     # macOS/Linux
.venv\Scripts\activate        # Windows
````
---
## How to install dependencies

````bash
pip install -r requirements.txt
````
---
## How to run the Game

Once everything is set up, start the game by running:

````bash
python -m dice.main
````
but because we already have a makefile ready you just need to write:
````bash
make run
````
---
## How to run all tests
````bash
python -m unittest discover -s test -p "test_*.py" -v
````
---

## How to play the game
When you start the game, you’ll be greeted with a introduction message.

Your goal is to reach 100 points before the computer.

**Each turn you roll two dice:**

Double ones (1 + 1): You lose all saved points and your turn ends.

Single one (1 + 2–6): Your turn ends, but you keep the points earned.

Otherwise: Add both dice to your current turn total and choose to roll again or hold.

Type 'help' in the terminal to see all available commands.

Type 'start' to begin a new game.

**Example commands:**

roll → roll the dice

hold → save your points

highscore → show leaderboard

quit → exit the game
## Author and License

**Author**: Mohammed Kawaf, Daniel Owliazadehabbasi, Mahmoud Nour 
**Course**: Methods for Sustainable Programming
**Language**: Python 3.12
**License**: MIT (Educational Use)



https://github.com/DanielAbbasi21/Pig-dice-game-