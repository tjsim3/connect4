from pathlib import Path

from model import trainStageOne, save_model

def stage1(samples=100000, epochs=100, d="both", model_name="stage1", model_dir="models"):
    print("Initializing")
    model = trainStageOne(
        samples=samples,
        epochs=epochs,

        #string "True" for defense, "False" for offense, "both" for both
        d = d
    )

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

stage1()