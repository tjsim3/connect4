from pathlib import Path

from model import trainStageOne, save_model


print("Initializing")
model = trainStageOne(
    samples=10000,
    epochs=100
)

PROJECT_ROOT = Path(__file__).resolve().parent
MODEL_DIR = PROJECT_ROOT / "models"
MODEL_DIR.mkdir(parents=True, exist_ok=True)

i = 0
while (MODEL_DIR / f"stage1.1[{i}].pth").exists():
    i += 1

filename = MODEL_DIR / f"stage1.1[{i}].pth"
save_model(model, filename)

print(f"Saved model to {filename}")