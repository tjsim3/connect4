from connectfour import getRandomBoard, getRandomWinningBoard

from tqdm import tqdm
import torch
from random import random

def generateStageOne(samples, d="False", save=False):
    print("I made it to the data generation function")
    data = []
    labels = []
    players = []
    with tqdm(total=samples) as pbar:
        pbar.set_description("Generating data")
        while len(data) < samples:
            board, answer, player = getRandomWinningBoard(d)

            if board is False or player is None:
                continue

            data.append(board)
            labels.append(answer)
            players.append(player)

            pbar.update(1)

    print("I finished making data")
    if save:
        torch.save(
            {
                "data": torch.tensor(data, dtype=torch.float32),
                "labels": torch.tensor(labels, dtype=torch.long),
                "players": torch.tensor(players, dtype=torch.long)
            },
            "stage1_data_10k.pt"
        )
    return data, labels, players

def generateStageTwo(samples, save=False):
    data = []
    labels = []
    players = []
    with tqdm(total=samples) as pbar:
        pbar.set_description("Generating data")
        while len(data) < samples:
            board = None
            col = None
            player = None
            random_val = random()
            if random_val < 0.3:
                board, col, player = getRandomWinningBoard(defense="False")
            elif random_val < 0.5:
                board, col, player = getRandomWinningBoard(defense="True")
            else:
                board, col, player = getRandomWinningBoard(defense="both")

            if all([board, col, player]) is not False:
                data.append(board)
                labels.append(col)
                players.append(player)

            pbar.update(1)