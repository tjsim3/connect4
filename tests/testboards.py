from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from user import printBoard
from generatedata import generateStageOne

boards, cols, players = generateStageOne(25, d="False", save=False)
for i in range(len(boards)):
    print(f"Column: {cols[i]}, Player: {players[i]}")
    printBoard(boards[i])