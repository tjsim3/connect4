from connectfour import getRandomBoard, getRandomWinningBoard

from tqdm import tqdm
import torch

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