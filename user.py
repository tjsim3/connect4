import os

from connectfour import makeMove, checkWin, checkDraw, togglePlayer
from model import load_model

import torch

def uservuser():
    board = [
        [0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0]
    ]
    player = 1
    printBoard(board)

    while not (checkWin(1, board) or checkWin(2, board) or checkDraw(board)):
        col = int(input(f"Player {player}, enter a column (0-6): "))
        if makeMove(player, col, board):
            if checkWin(player, board):
                os.system('cls')
                printBoard(board)
                print(f"Player {player} wins!")
                break
            elif checkDraw(board):
                os.system('cls')
                printBoard(board)
                print("It's a draw!")
                break
            player = togglePlayer(player)
            os.system('cls')
            printBoard(board)

def uservmodel(model):
    board = [
        [0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0]
    ]

    model = load_model(model)

    player = 1
    printBoard(board)

    while not (checkWin(1, board) or checkWin(2, board) or checkDraw(board)):
        col = int(input(f"Player {player}, enter a column (0-6): "))
        if makeMove(player, col, board):
            if checkWin(player, board):
                os.system('cls')
                printBoard(board)
                print(f"Player {player} wins!")
                break
            elif checkDraw(board):
                os.system('cls')
                printBoard(board)
                print("It's a draw!")
                break
            player = togglePlayer(player)
            os.system('cls')
            flat = torch.tensor(board, dtype=torch.float32).view(-1)
            flat = torch.cat((flat, torch.tensor([player], dtype=torch.float32)))
            with torch.no_grad():
                scores = model(flat.unsqueeze(0))
                order = torch.argsort(scores.squeeze(), descending=True)
                for col in order:
                    if makeMove(player, col.item(), board):
                        print(f"AI chooses column {col.item()}")
                        print(scores)
                        break

            player = togglePlayer(player)
            printBoard(board)
    
def printBoard(board):
    for row in board:
        print(row)
    print("---------------------")

