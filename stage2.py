import os
from pathlib import Path

from model import NeuralNetwork, load_model, save_model
from neurovolution import mutate, copyAndMutate, tournament, roundRobin

import tqdm

def stage2(num_models=4, generations=4, model=None, model_name="stage2", model_dir="models"):
    if model is None or not os.path.exists(model):
        #print("Generation 1")
        models = [NeuralNetwork() for _ in range(num_models)]
        for model in models:
            mutate(model, 0.1)
        model = tournament(models)
        for i in range(generations-1):
            #print(f"Generation {i+2}")
            models = copyAndMutate(model, num_models)
            model = tournament(models)
    else:
        model = load_model(model)
        for i in tqdm.tqdm(range(generations)):
            #print(f"Generation {i+2}")
            models = copyAndMutate(model, num_models)
            model = tournament(models)

    PROJECT_ROOT = Path(__file__).resolve().parent
    MODEL_DIR = PROJECT_ROOT / model_dir
    MODEL_DIR.mkdir(parents=True, exist_ok=True)

    i = 0

    #change model name to stage1.2 if you want to train defense or 1 if you want to train full model
    while (MODEL_DIR / f"{model_name}[{i}].pth").exists():
        i += 1

    filename = MODEL_DIR / f"{model_name}[{i}].pth"
    save_model(model, filename)

    print(f"Saved model to {filename}")

stage2(64, 10000, "models/stage1[4].pth")