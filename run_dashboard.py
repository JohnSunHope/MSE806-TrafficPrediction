"""Secure FastAPI service for traffic speed prediction."""

from __future__ import annotations

import hmac
import logging
import os
import time
import uuid
from collections import defaultdict, deque
from contextlib import asynccontextmanager
from pathlib import Path
from threading import Lock

import joblib
import pandas as pd
from fastapi import Depends, FastAPI, Header, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, ConfigDict, Field

from modeling import FEATURE_COLUMNS

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
LOGGER = logging.getLogger("traffic-api")
MODEL_PATH = Path("models/traffic_model.joblib")
DEFAULT_DEMO_KEY = "mse806-demo-key"
RATE_LIMIT = int(os.getenv("TRAFFIC_RATE_LIMIT", "30"))
RATE_WINDOW_SECONDS = 60


class PredictionFeatures(BaseModel):
    model_config = ConfigDict(extra="forbid")
    hour: float = Field(ge=0, lt=24)
    day_of_week: int = Field(ge=0, le=6)
    weather_temp: float = Field(ge=-30, le=60)
    weather_precip: float = Field(ge=0, le=100)
    volume: float = Field(ge=0, le=500)
    incident: int = Field(ge=0, le=1)
    speed_lag_1: float = Field(ge=0, le=160)
    speed_lag_2: float = Field(ge=0, le=160)
    speed_lag_3: float = Field(ge=0, le=160)
    rolling_mean_3: float = Field(ge=0, le=160)


class PredictionRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    features: PredictionFeatures


class SlidingWindowLimiter:
    def __init__(self, limit: int, window_seconds: int) -> None:
        self.limit = limit
        self.window_seconds = window_seconds
        self._requests: defaultdict[str, deque[float]] = defaultdict(deque)
        self._lock = Lock()

    def allow(self, client: str) -> bool:
        now = time.monotonic()
        with self._lock:
            requests = self._requests[client]
            while requests and now - requests[0] >= self.window_seconds:
                requests.popleft()
            if len(requests) >= self.limit:
                return False
            requests.append(now)
            return True


def require_api_key(x_api_key: str = Header(default="")) -> None:
    expected = os.getenv("TRAFFIC_API_KEY", DEFAULT_DEMO_KEY)
    if not hmac.compare_digest(x_api_key, expected):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="A valid X-API-Key header is required",
        )


def load_model():
    if not MODEL_PATH.exists():
        raise RuntimeError("Model missing. Run train_model.py first.")
    return joblib.load(MODEL_PATH)


def create_app(model=None) -> FastAPI:
    @asynccontextmanager
    async def lifespan(application: FastAPI):
        if application.state.model is None:
            application.state.model = load_model()
        yield

    application = FastAPI(
        title="Secure Traffic Prediction API",
        version="2.0.0",
        description="Five minute traffic speed forecasting for one synthetic road segment.",
        lifespan=lifespan,
    )
    application.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:8001", "http://127.0.0.1:8001"],
        allow_credentials=False,
        allow_methods=["GET", "POST"],
        allow_headers=["Content-Type", "X-API-Key"],
    )
    application.state.model = model
    application.state.limiter = SlidingWindowLimiter(RATE_LIMIT, RATE_WINDOW_SECONDS)

    @application.middleware("http")
    async def request_logging(request: Request, call_next):
        request_id = str(uuid.uuid4())
        started = time.perf_counter()
        response = await call_next(request)
        response.headers["X-Request-ID"] = request_id
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["Cache-Control"] = "no-store"
        LOGGER.info(
            "request_id=%s method=%s path=%s status=%s duration_ms=%.2f",
            request_id,
            request.method,
            request.url.path,
            response.status_code,
            (time.perf_counter() - started) * 1000,
        )
        return response

    @application.get("/health")
    def health() -> dict[str, str]:
        return {"status": "healthy", "model": "gradient_boosting", "data": "synthetic"}

    @application.post("/predict", dependencies=[Depends(require_api_key)])
    def predict(payload: PredictionRequest, request: Request) -> dict[str, object]:
        client = request.client.host if request.client else "unknown"
        if not application.state.limiter.allow(client):
            raise HTTPException(status_code=429, detail="Rate limit exceeded")
        values = payload.features.model_dump()
        frame = pd.DataFrame([[values[name] for name in FEATURE_COLUMNS]], columns=FEATURE_COLUMNS)
        prediction = float(application.state.model.predict(frame)[0])
        return {
            "predicted_speed_kmh": round(prediction, 2),
            "forecast_horizon_minutes": 5,
            "segment_id": "CITY_CENTRE_01",
        }

    return application


app = create_app()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
