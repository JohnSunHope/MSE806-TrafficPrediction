"""Shared feature engineering and evaluation utilities."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

FEATURE_COLUMNS = [
    "hour",
    "day_of_week",
    "weather_temp",
    "weather_precip",
    "volume",
    "incident",
    "speed_lag_1",
    "speed_lag_2",
    "speed_lag_3",
    "rolling_mean_3",
]


@dataclass(frozen=True)
class RegressionMetrics:
    mae: float
    rmse: float
    r2: float

    def as_dict(self) -> dict[str, float]:
        return {
            "mae_kmh": round(self.mae, 4),
            "rmse_kmh": round(self.rmse, 4),
            "r2": round(self.r2, 4),
        }


def create_features(data: pd.DataFrame) -> pd.DataFrame:
    """Create lag and rolling features without using future observations."""
    prepared = data.sort_values("timestamp").copy()
    for lag in range(1, 4):
        prepared[f"speed_lag_{lag}"] = prepared["speed"].shift(lag)
    prepared["rolling_mean_3"] = prepared[
        ["speed_lag_1", "speed_lag_2", "speed_lag_3"]
    ].mean(axis=1)
    return prepared.dropna().reset_index(drop=True)


def chronological_split(
    data: pd.DataFrame,
    train_ratio: float = 0.8,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    if not 0.5 <= train_ratio < 1:
        raise ValueError("train_ratio must be between 0.5 and 1.0")
    split_index = int(len(data) * train_ratio)
    return data.iloc[:split_index].copy(), data.iloc[split_index:].copy()


def regression_metrics(actual: np.ndarray, predicted: np.ndarray) -> RegressionMetrics:
    return RegressionMetrics(
        mae=float(mean_absolute_error(actual, predicted)),
        rmse=float(np.sqrt(mean_squared_error(actual, predicted))),
        r2=float(r2_score(actual, predicted)),
    )
