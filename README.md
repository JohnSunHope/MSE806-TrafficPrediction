# Secure Intelligent Traffic Congestion Prediction and Monitoring System

This MSE806 Assessment 2 project predicts road speed five minutes ahead for a
synthetic city-centre sensor. It combines a gradient-boosted regression model, a
FastAPI service, a browser dashboard and security controls that protect the
prediction endpoint.

## Group members start here

All assignment documents, the presentation, the recording instructions and the
downloaded Turnitin similarity report are in
[`assessment_materials/`](assessment_materials/README.md).

Before recording, each member should:

1. Read the official brief and the project report.
2. Open the PowerPoint and find the four slides assigned to their role.
3. Read the matching section in the presentation transcript.
4. Rehearse for 3 to 5 minutes and explain the work in their own words.
5. Record in 16:9 landscape format with the assigned slides visible.

| Presenter | Student ID | Role | Slides |
| --- | --- | --- | --- |
| Xiaotong Sun | 270876224 | Data and Model Engineer | 1 to 4 |
| Jingbiao Geng | 270686148 | API and Security Engineer | 5 to 8 |
| Han Jia | 270902385 | Evaluation and Communication Lead | 9 to 12 |

The combined recording must remain below 15 minutes. The three recordings can
be recorded separately and combined in slide order, or the group can record one
continuous presentation. Keep the handovers at the end of slides 4 and 8.

## Academic origin and original contribution

The project adapts the public MIT-licensed
[TrafficPrediction repository](https://github.com/LuthandoCandlovu/TrafficPrediction)
by Luthando Candlovu at commit `cfd0058c8376b88b3abcbc638fd4098c95bd1625`.
The original repository supplied the topic, an initial data generator, training
scripts, a FastAPI example and a dashboard. The assessment version adds:

- a revised deterministic traffic and incident simulator;
- chronological evaluation against a persistence baseline;
- reproducible metrics and an editable evaluation chart in the presentation;
- strict request schemas and range validation;
- API-key authentication, rate limiting and restricted CORS;
- request IDs, audit logging and security response headers;
- automated tests and a three-person contribution structure.

The synthetic data do not describe a real road or city. Do not use the model
for operational traffic management without validation on authorised local data.

## Three-person roles

| Role | Main ownership | Presentation part |
| --- | --- | --- |
| Xiaotong Sun 270876224, Data and Model Engineer | Data generator, feature engineering, gradient-boosted model training, reproducibility | Part 1, problem, proposal, data and model |
| Jingbiao Geng 270686148, API and Security Engineer | FastAPI service, authentication, validation, rate limiting, logging, tests | Part 2, system design, implementation and security |
| Han Jia 270902385, Evaluation and Communication Lead | Baseline comparison, metrics, chart, dashboard, report and integration checks | Part 3, results, limitations and conclusion |

Each member should verify and explain their own contribution during the recorded presentation.

## Reproduce the project

Use Python 3.9 or later.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python generate_data.py
python train_model.py
python evaluate_models.py
pytest -q
```

Start the API and dashboard in separate terminals:

```bash
TRAFFIC_API_KEY=mse806-demo-key uvicorn run_dashboard:app --host 127.0.0.1 --port 8000
python -m http.server 8001
```

Open `http://127.0.0.1:8001/dashboard.html`. The included demonstration key
is suitable only for a local presentation. Use a randomly generated secret in
any shared environment.

## API example

```bash
curl -X POST http://127.0.0.1:8000/predict \
  -H 'Content-Type: application/json' \
  -H 'X-API-Key: mse806-demo-key' \
  -d '{"features":{"hour":17,"day_of_week":2,"weather_temp":18,"weather_precip":0.4,"volume":150,"incident":0,"speed_lag_1":45,"speed_lag_2":46,"speed_lag_3":44,"rolling_mean_3":45}}'
```

## Files

- `generate_data.py` creates 17,280 five-minute synthetic records.
- `modeling.py` contains feature, split and metric functions.
- `train_model.py` trains and saves the model.
- `evaluate_models.py` compares the model with the previous-speed baseline and saves JSON evidence.
- `run_dashboard.py` serves the secured API.
- `dashboard.html` provides the demonstration interface.
- `tests/test_api.py` checks authentication, validation, headers and rate limits.
- `results/` contains generated evaluation evidence.

## Security boundaries

The in-memory rate limiter works for one API process and resets when that
process restarts. A production deployment should use a shared rate-limit store,
TLS, managed secrets, user-level authorisation, central monitoring and a formal
incident response process. The model also needs drift monitoring and periodic
retraining on authorised traffic data.

## Licence

The adapted code remains available under the MIT License. See `LICENSE`.
