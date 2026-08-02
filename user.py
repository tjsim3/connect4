import os

from connectfour import makeMove, checkWin, checkDraw

board = [
    [0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0]
]

def printBoard(board):
    for row in board:
        print(row)

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
        player = 2 if player == 1 else 1
        os.system('cls')
        printBoard(board)