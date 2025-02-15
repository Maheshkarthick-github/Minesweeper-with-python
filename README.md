# Minesweeper-with-python
**Minesweeper Game (Pygame Implementation)

Overview

This is a simple Minesweeper game implemented using Pygame. The game follows standard Minesweeper mechanics, where the player must reveal cells without triggering mines.

Features

✅ 10x10 grid size (customizable)
✅ 15 randomly placed mines
✅ Click to reveal cells
✅ Numbers indicate adjacent mines
✅ Red cells indicate mines
✅ Immediate zero-neighbor reveal (prevents large auto-clearing)

Installation

Install Python (Ensure Python 3.x is installed)

Install Pygame:

pip install pygame

Clone the Repository:

git clone <repository_url>
cd minesweeper

How to Run

Run the following command:

python minesweeper.py

Controls

🖱 Left Click → Reveal a cell🚩 Right Click (Optional Enhancement) → Flag a potential mine

Game Rules

If a mine is clicked, the game ends.

If a numbered cell is clicked, it shows the number of adjacent mines.

If a zero is clicked, only its immediate neighbors are revealed.

The objective is to reveal all non-mine cells.

Customization

You can change the following constants in minesweeper.py:

GRID_SIZE = 10  # Change board size
CELL_SIZE = 40  # Adjust cell dimensions
MINE_COUNT = 15  # Modify the number of mines

Dependencies

Python 3.x

Pygame
