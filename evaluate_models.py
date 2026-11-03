"""Compare the trained model with a persistence baseline and save evidence."""

from __future__ import annotations

import json
import time
from pathlib import Path

import joblib
import pandas as pd

from modeling import FEATURE_COLUMNS, chronological_split, create_features, regression_metrics
from train_model import MODEL_PATH

RESULTS_DIR = Path("results")


def evaluate() -> dict[str, object]:
    data = pd.read_csv("traffic_data.csv", parse_dates=["timestamp"])
    prepared = create_features(data)
    _, validation = chronological_split(prepared)
    actual = validation["speed"].to_numpy()
    baseline = validation["speed_lag_1"].to_numpy()
    model = joblib.load(MODEL_PATH)
    started = time.perf_counter()
    predicted = model.predict(validation[FEATURE_COLUMNS])
    latency_ms = (time.perf_counter() - started) * 1000 / len(validation)

    baseline_metrics = regression_metrics(actual, baseline).as_dict()
    model_metrics = regression_metrics(actual, predicted).as_dict()
    model_metrics["mean_inference_ms_per_record"] = round(latency_ms, 6)
    results: dict[str, object] = {
        "data": {
            "synthetic_records": int(len(data)),
            "validation_records": int(len(validation)),
            "split": "chronological 80/20",
        },
        "persistence_baseline": baseline_metrics,
        "gradient_boosting": model_metrics,
        "mae_improvement_percent": round(
            100 * (baseline_metrics["mae_kmh"] - model_metrics["mae_kmh"])
            / baseline_metrics["mae_kmh"],
            2,
        ),
    }
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    (RESULTS_DIR / "model_evaluation.json").write_text(
        json.dumps(results, indent=2), encoding="utf-8"
    )

    return results


if __name__ == "__main__":
    print(json.dumps(evaluate(), indent=2))
