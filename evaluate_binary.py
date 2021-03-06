import os

from src.evaluation.model_evaluator import ModelEvaluator

from pathlib import Path

from wasabi import msg

if __name__ == "__main__":

    NUM_CLASSES = 2
    MODEL_TYPE = "embedding_baseline"

    BASE_SPLIT_PATH = (
        Path("/work")
        / "wav2vec_finetune"
        / "data"
        / "audio_file_splits"
        / "binary_splits"
    )
    BASE_MODEL_PATH = Path("/work") / "wav2vec_finetune" / "baseline_models_v3"

    for diagnosis in ["ASD", "DEPR", "SCHZ"]:
        msg.info(f"Evaluating {diagnosis}..")
        id2label = {0: "TD", 1: diagnosis}

        for split in ["train", "val", "test"]:
            msg.info(f"Split: {split}")
            data_path = BASE_SPLIT_PATH / f"{diagnosis}_{split}_split.csv"
            for model in BASE_MODEL_PATH.glob(f"*{diagnosis}*"):
                msg.info(f"Model: {model.name}")
                # Choosing the first sorted checkpoint, i.e. the checkpoint with highest val score
                ckpts = sorted(list(model.iterdir()))
                ckpt = ckpts[0]
                feature_set = model.name.split("_")[2:]
                feature_set = "_".join(feature_set)
                save_name = f"{model.name}_{split}.jsonl"

                if (Path("results") / save_name).exists():
                    msg.info(f"{save_name} already exists. Skipping...")
                    continue
                evaluator = ModelEvaluator(
                    model_type=MODEL_TYPE,
                    model_path=ckpt,
                    feature_set=feature_set,
                    data_path=data_path,
                    num_classes=NUM_CLASSES,
                    id2label=id2label,
                )
                evaluator.evaluate_model()
                evaluator.save_to_json(save_name)
