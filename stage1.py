from pathlib import Path

from model import trainStageOne, save_model

def stage1():
    print("Initializing")
    model = trainStageOne(
        samples=10000,
        epochs=100,

        #string "True" for defense, "False" for offense, "both" for both
        d = "both"
    )

    PROJECT_ROOT = Path(__file__).resolve().parent
    MODEL_DIR = PROJECT_ROOT / "models"
    MODEL_DIR.mkdir(parents=True, exist_ok=True)

    i = 0

    #change model name to stage1.2 if you want to train defense or 1 if you want to train full model
    while (MODEL_DIR / f"stage1[{i}].pth").exists():
        i += 1

    filename = MODEL_DIR / f"stage1[{i}].pth"
    save_model(model, filename)

    print(f"Saved model to {filename}")

stage1()