"""Generate a reproducible synthetic traffic sensor data set.

The data are synthetic and must not be described as observations from a real
city. They represent a single urban road segment sampled every five minutes.
"""

from __future__ import annotations

from datetime import datetime, timedelta
from pathlib import Path

import numpy as np
import pandas as pd


def generate_traffic_data(
    days: int = 60,
    sample_interval: int = 5,
    seed: int = 42,
) -> pd.DataFrame:
    """Return synthetic speed, demand, weather and incident measurements."""
    rng = np.random.default_rng(seed)
    start_time = datetime(2025, 1, 1)
    intervals = int(days * 24 * 60 / sample_interval)
    timestamps = [
        start_time + timedelta(minutes=index * sample_interval)
        for index in range(intervals)
    ]

    hour = np.array([value.hour + value.minute / 60 for value in timestamps])
    day_of_week = np.array([value.weekday() for value in timestamps])
    weekday = (day_of_week < 5).astype(int)
    morning_peak = np.exp(-0.5 * ((hour - 8.0) / 1.5) ** 2)
    evening_peak = np.exp(-0.5 * ((hour - 17.5) / 1.8) ** 2)
    demand_index = weekday * (morning_peak + evening_peak)

    incident = (rng.random(intervals) < 0.025).astype(int)
    weather_temp = (
        18
        + 6 * np.sin(2 * np.pi * (hour - 10) / 24)
        + rng.normal(0, 1.8, intervals)
    )
    raining = rng.random(intervals) < 0.12
    weather_precip = np.where(raining, rng.gamma(1.5, 0.7, intervals), 0)
    speed = (
        58
        - 19 * demand_index
        - 17 * incident
        - 2.2 * weather_precip
        + rng.normal(0, 3.2, intervals)
    )
    speed = np.clip(speed, 8, 80)
    volume = (
        65
        + 120 * demand_index
        + 18 * weekday
        + rng.normal(0, 12, intervals)
    )
    volume = np.clip(volume, 10, 260)

    return pd.DataFrame(
        {
            "timestamp": timestamps,
            "segment_id": "CITY_CENTRE_01",
            "speed": speed,
            "volume": volume,
            "weather_temp": weather_temp,
            "weather_precip": weather_precip,
            "incident": incident,
            "hour": hour,
            "day_of_week": day_of_week,
        }
    )


def main() -> None:
    output_path = Path("traffic_data.csv")
    data = generate_traffic_data()
    data.to_csv(output_path, index=False)
    print(f"Generated {len(data):,} synthetic records -> {output_path}")


if __name__ == "__main__":
    main()
