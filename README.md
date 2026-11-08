# Garment Size Prediction API

[![CI](https://github.com/Beru47/garment-size-prediction-api/actions/workflows/ci.yml/badge.svg)](https://github.com/Beru47/garment-size-prediction-api/actions/workflows/ci.yml)
![Python](https://img.shields.io/badge/python-3.11-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.111-009688)

A FastAPI service that estimates a full set of body measurements (chest, waist, hips, thigh, knee, head and more) from four inputs: gender, height, weight and body morphology. Those measurements feed garment-size recommendation, so shoppers get a better fit without taking a tape measure to themselves.

## Context

Built during my summer 2024 internship at Welyne Group (Wefizz). I designed and shipped the prediction service, its database layer and the deployment pipeline.

## Results

- 25% better sizing accuracy
- 18% fewer returns
- Prediction latency under 200 ms
- 99% uptime
- Shipped with Docker and GitLab CI/CD

## Architecture

```mermaid
flowchart LR
    client["Client app"] --> api["FastAPI service"]
    api --> schemas["Pydantic validation"]
    schemas --> pipeline["Prediction pipeline"]
    models[("Trained models: models/*.pkl")] -. loaded once at startup .-> pipeline
    pipeline --> api
    api --> db[("PostgreSQL")]
    csv["CSV upload"] --> api
```

## Model approach

`ai/prediction.py` runs a two-stage pipeline.

1. **Base model.** A scikit-learn random forest (multi-output regression) takes gender, height, weight and morphology (encoded per gender: male H/V/O, female A/X/8/V/H/O). It predicts 13 base measurements: ankle, arm length, bicep, calf, chest, forearm, hip, leg length, shoulder breadth, shoulder-to-crotch, thigh, waist, wrist.
2. **Specialist regressors.** Knee circumference, head circumference and thigh each get a dedicated regressor, using the base predictions plus height and weight as features.
3. **Derived measures.** Chest base, high hip, low hip, elbow and widest thigh are computed from the predictions with fixed ratios.

All models are loaded once at startup, and the API fails fast if a model file is missing.

## API

| Method | Path | Description |
|---|---|---|
| GET | `/health` | Liveness and model-loaded status |
| POST | `/predict` | Predict all measurements from a JSON body (no database needed) |
| POST | `/add_client` | Upload a CSV of clients, predict, store in PostgreSQL |
| GET | `/get_measures_predictions/{id}` | Stored predictions for a client |
| GET | `/get_measures/{id}` | Measured values merged with predictions |
| GET | `/get_measures_accuracy/{id}` | Prediction accuracy per measure |
| GET | `/check_db`, `/check_client_table` | Database introspection |

Interactive docs at `/docs`.

```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"gender": 1, "height_cm": 179, "weight_kg": 91, "morphology": "V"}'
```

```json
{"measurements": {"Biceps": 34.4, "Chest_Circumference": 112.4, "Waist_Circumference": 99.0,
  "Shoulder_Width": 47.6, "Trunk_Length": 69.6, "calf": 39.4, "Leg_Length": 93.7,
  "Chest_Base": 103.4, "High_Hip": 101.3, "Low_Hip": 111.9, "Right_Elbow": 31.3,
  "Right_Thigh_Widest": 70.6, "Arm_Length": 59.8, "knee": 40.0,
  "Head_Circumference": 59.2, "thigh": 44.9}}
```

Invalid input (for example a female-only morphology for a male) returns `422` with details. If PostgreSQL is down, database endpoints return `503` while `/health` and `/predict` keep working.

## Run locally

```bash
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Configuration (environment variables):

| Variable | Default |
|---|---|
| `DATABASE_URL` | `postgresql://postgres:***REMOVED***@localhost/api_db` |
| `MODELS_DIR` | `./models` |
| `CORS_ORIGINS` | `http://127.0.0.1:5500,http://localhost:5500,http://localhost` |

## Run with Docker

```bash
docker compose up --build   # API on :8000, PostgreSQL included
```

## Tests

```bash
pip install -r requirements-dev.txt
ruff check .
pytest
```

## Project structure

```
app/        FastAPI app: routes, schemas, ORM models, config, CSV client operations
ai/         Prediction pipeline and model loading
models/     Trained scikit-learn models (.pkl)
data/       Sample client CSV files
tests/      API tests
```

## Next steps

- Add a Redis cache in front of repeated predictions.
- Include the training scripts and notebooks (only the trained models are in this repo).
- Replace startup `create_all` with Alembic migrations.
- Add an `/add_client` integration test against a Postgres container.
