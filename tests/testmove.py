from pathlib import Path
import sys

import torch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from model import load_model


game = None 
file = "stage1[3].pth"
PROJECT_ROOT = Path(__file__).resolve().parent
MODEL_PATH = PROJECT_ROOT / "models" / file

model = load_model(MODEL_PATH)
model.eval()

game = [
    0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 
    0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0,
    0, 1, 0, 0, 0, 0, 0,
    1, 1, 0, 0, 2, 2, 2,
    2
] if game is None else game

game = torch.tensor(game, dtype=torch.float32).unsqueeze(0)

with torch.no_grad():
    output = model(game)
    predicted_move = torch.argmax(output, dim=1).item()
    print(f"Predicted move: {predicted_move}")

