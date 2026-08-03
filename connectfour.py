import random
import copy

def togglePlayer(player):
    return 1 if player == 2 else 2

def getRandomBoard():
    board = [
    [0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0]
    ]
    moveCache = []

    turns = random.randint(2, 6)
    for i in range(turns):
        moveCache.append((1, random.randint(0, 6)))
        moveCache.append((2, random.randint(0, 6)))
    for player, col in moveCache:
        makeMove(player, col, board)
        if checkWin(player, board):
            for i in range(6):
                if board[i][col] == player:
                    board[i][col] = 0
                    break
            return board
    return board

def getRandomWinningBoard(defense="False"):
    while True:
        board = [
        [0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0]
        ]
        moveCache = []

        for i in range(21):
            moveCache.append((1, random.randint(0, 6)))
            moveCache.append((2, random.randint(0, 6)))

        #print("Move cache:", moveCache)
        for player, col in moveCache:
            makeMove(player, col, board)
            win = checkPossibleWin(player, board)
            if win is not False:
                if defense == "True":
                    throwMove(player, col, board)
                    player = togglePlayer(player)
                if defense == "both":
                    if random.randint(0, 1) == 0:
                        throwMove(player, col, board)
                        player = togglePlayer(player)
                return board, win, player


def makeMove(player, col, board):
    for i in range(6):
        if board[5-i][col] == 0:
            board[5-i][col] = player
            return True
    return False

def throwMove(player, col, board):
    throwMove = random.randint(0, 6)
    while throwMove == col:
        throwMove = random.randint(0, 6)
    player = togglePlayer(player)
    makeMove(player, throwMove, board)

def checkWin(player, board):
    # Check horizontal
    for row in range(6):
        for col in range(4):
            if all(board[row][col+i] == player for i in range(4)):
                return True

    # Check vertical
    for col in range(7):
        for row in range(3):
            if all(board[row+i][col] == player for i in range(4)):
                return True

    # Check diagonal (bottom-left to top-right)
    for row in range(3, 6):
        for col in range(4):
            if all(board[row-i][col+i] == player for i in range(4)):
                return True

    # Check diagonal (top-left to bottom-right)
    for row in range(3):
        for col in range(4):
            if all(board[row+i][col+i] == player for i in range(4)):
                return True

    return False

def checkPossibleWin(player, board):
    wins = []
    for i in range(7):
        board_copy = copy.deepcopy(board)
        makeMove(player, i, board_copy)
        if checkWin(player, board_copy):
            wins.append(i)
    return wins[0] if wins else False

def checkDraw(board):
    for row in range(6):
        for col in range(7):
            if board[row][col] == 0:
                return False
    return True


for i in range(100):
    board = getRandomBoard()

