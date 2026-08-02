import random

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
                if board[5-i][col] == player:
                    board[5-i][col] = 0
                    break
            return board
    return board

def getRandomWinningBoard(defense):
    board = [
    [0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0]
    ]
    moveCache = []

    w = False
    for i in range(21):
        moveCache.append((1, random.randint(0, 6)))
        moveCache.append((2, random.randint(0, 6)))
    for player, col in moveCache:
        makeMove(player, col, board)
        if checkWin(player, board):
            for i in range(6):
                if board[5-i][col] == player:
                    board[5-i][col] = 0
                    if defense == "True":
                        throwMove = random.randint(0, 6)
                        while throwMove == col:
                            throwMove = random.randint(0, 6)
                        player = 1 if player == 2 else 2
                        makeMove(player, throwMove, board)

                    if defense == "both":
                        if random.randint(0, 1) == 0:
                            throwMove = random.randint(0, 6)
                            while throwMove == col:
                                throwMove = random.randint(0, 6)
                            player = 1 if player == 2 else 2
                            makeMove(player, throwMove, board)
                    
                    w = True
                    player = 1 if player == 2 else 2
                    return board, col, player
                    break
    return False, False, None

def makeMove(player, col, board):
    for i in range(6):
        if board[5-i][col] == 0:
            board[5-i][col] = player
            return True
    return False

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

def checkDraw(board):
    for row in range(6):
        for col in range(7):
            if board[row][col] == 0:
                return False
    return True


for i in range(100):
    board = getRandomBoard()

