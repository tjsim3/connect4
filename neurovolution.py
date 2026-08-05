import os
from pathlib import Path

from connectfour import makeMove, checkWin, checkDraw, togglePlayer
from user import printBoard
from model import NeuralNetwork

import torch
import numpy as np
from random import randint, choice
import tqdm

def mutate(model, mutation_rate=0.02, mutation_strength=0.001):
    with torch.no_grad():
        for param in model.parameters():
            mask = torch.rand_like(param) < mutation_rate
            noise = torch.randn_like(param) * mutation_strength
            param.add_(mask * noise)

def copyAndMutate(model, copies=1, mutation_rate=0.02, mutation_strength=0.1):
    models = [NeuralNetwork() for _ in range(copies)]
    for m in models:
        m.load_state_dict(model.state_dict()) 
        mutate(m, mutation_rate, mutation_strength)
    return models

def matchup(model1, model2):
    model1.eval()
    model2.eval()

    board = [
        [0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0],
    ]
    player = randint(0, 1) + 1

    while True:
        flat = torch.tensor(board, dtype=torch.float32).view(-1)
        flat = torch.cat((flat, torch.tensor([player], dtype=torch.float32)))
        with torch.no_grad():
            scores = model1(flat.unsqueeze(0))
            order = torch.argsort(scores.squeeze(), descending=True)
            for col in order:
                if makeMove(player, col.item(), board):
                    break
            
        if checkWin(player, board):
            return player, board
        elif checkDraw(board):
            return 0, board
            
        player = togglePlayer(player)

        flat2 = torch.tensor(board, dtype=torch.float32).view(-1)
        flat2 = torch.cat((flat2, torch.tensor([player], dtype=torch.float32)))
        with torch.no_grad():
            scores = model2(flat2.unsqueeze(0))
            order = torch.argsort(scores.squeeze(), descending=True)
            for col in order:
                if makeMove(player, col.item(), board):
                    break

        if checkWin(player, board):
            return player, board
        elif checkDraw(board):
            return 0, board
            
        player = togglePlayer(player)

def roundRobin(models):
    print("Made it to the round robin function")
    fitness = [0.0 for _ in range(len(models))]
    for i in range(len(models)):
        for j in range(i+1, len(models)):
            result, board = matchup(models[i], models[j])
            if result == 0:
                fitness[i] -= 0.1
                fitness[j] -= 0.1
            elif result == 1:
                fitness[i] += 1
                fitness[j] -= 1
            else:
                fitness[i] -= 1
                fitness[j] += 1
            print(f"Round ended with result {result}")
            for i in range(len(board)):
                print(board[i])

    return fitness

def tournament(models):
    if not np.log2(len(models)).is_integer():
        raise ValueError("Number of models must be a power of 2")

    contenders = list(models)
    round_num = 1

    while len(contenders) > 1:
        #print(f"Round {round_num}: {len(contenders)} contenders")

        next_round = []

        for i in range(0, len(contenders), 2):
            model_a = contenders[i]
            model_b = contenders[i + 1]

            result, board = matchup(model_a, model_b)
            #printBoard(board)

            if result == 1:
                winner = model_a
            elif result == 2:
                winner = model_b
            else:
                winner = choice([model_a, model_b])

            next_round.append(winner)

        contenders = next_round
        round_num += 1

    return contenders[0]
