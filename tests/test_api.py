from __future__ import annotations

import numpy as np
from fastapi.testclient import TestClient

from run_dashboard import DEFAULT_DEMO_KEY, SlidingWindowLimiter, create_app


class FixedModel:
    def predict(self, _frame):
        return np.array([42.5])


def valid_payload() -> dict[str, object]:
    return {
        "features": {
            "hour": 17,
            "day_of_week": 2,
            "weather_temp": 18,
            "weather_precip": 0.4,
            "volume": 150,
            "incident": 0,
            "speed_lag_1": 45,
            "speed_lag_2": 46,
            "speed_lag_3": 44,
            "rolling_mean_3": 45,
        }
    }


def test_health_endpoint_is_public():
    with TestClient(create_app(FixedModel())) as client:
        response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_prediction_rejects_missing_api_key():
    with TestClient(create_app(FixedModel())) as client:
        response = client.post("/predict", json=valid_payload())
    assert response.status_code == 401


def test_prediction_rejects_invalid_range():
    payload = valid_payload()
    payload["features"]["hour"] = 30
    with TestClient(create_app(FixedModel())) as client:
        response = client.post(
            "/predict", json=payload, headers={"X-API-Key": DEFAULT_DEMO_KEY}
        )
    assert response.status_code == 422


def test_prediction_returns_forecast_and_security_headers():
    with TestClient(create_app(FixedModel())) as client:
        response = client.post(
            "/predict", json=valid_payload(), headers={"X-API-Key": DEFAULT_DEMO_KEY}
        )
    assert response.status_code == 200
    assert response.json()["predicted_speed_kmh"] == 42.5
    assert response.headers["cache-control"] == "no-store"
    assert response.headers["x-content-type-options"] == "nosniff"
    assert response.headers["x-request-id"]


def test_rate_limiter_blocks_after_limit():
    limiter = SlidingWindowLimiter(limit=2, window_seconds=60)
    assert limiter.allow("client") is True
    assert limiter.allow("client") is True
    assert limiter.allow("client") is False
