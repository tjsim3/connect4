from connectfour import getRandomBoard, getRandomWinningBoard
from tqdm import tqdm

def generateStageOne(samples, d=False):
    print("I made it to the data generation function")
    data = []
    labels = []
    players = []
    with tqdm(total=samples) as pbar:
        while len(data) < samples:
            board, answer, player = getRandomWinningBoard(d)

            if board is False or player is None:
                continue

            data.append(board)
            labels.append(answer)
            players.append(player)

            pbar.update(1)

    print("I finished making data")
    return data, labels, players