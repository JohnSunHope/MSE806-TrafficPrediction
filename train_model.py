"""Train and persist the traffic speed model."""

from __future__ import annotations

import json
from pathlib import Path

import joblib
import pandas as pd
from sklearn.ensemble import HistGradientBoostingRegressor

from modeling import FEATURE_COLUMNS, chronological_split, create_features, regression_metrics

MODEL_PATH = Path("models/traffic_model.joblib")
METRICS_PATH = Path("results/training_metrics.json")


def train_model(data_path: Path = Path("traffic_data.csv")) -> dict[str, float]:
    data = pd.read_csv(data_path, parse_dates=["timestamp"])
    prepared = create_features(data)
    training, validation = chronological_split(prepared)
    model = HistGradientBoostingRegressor(
        learning_rate=0.08,
        max_iter=180,
        max_leaf_nodes=31,
        l2_regularization=0.1,
        random_state=42,
    )
    model.fit(training[FEATURE_COLUMNS], training["speed"])
    predictions = model.predict(validation[FEATURE_COLUMNS])
    metrics = regression_metrics(validation["speed"].to_numpy(), predictions).as_dict()
    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    METRICS_PATH.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, MODEL_PATH)
    METRICS_PATH.write_text(json.dumps(metrics, indent=2), encoding="utf-8")
    return metrics


def main() -> None:
    metrics = train_model()
    print(json.dumps(metrics, indent=2))
    print(f"Model saved to {MODEL_PATH}")


if __name__ == "__main__":
    main()
