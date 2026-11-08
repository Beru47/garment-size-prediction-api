import logging
from contextlib import asynccontextmanager
from io import StringIO

import pandas as pd
from fastapi import Depends, FastAPI, File, HTTPException, UploadFile, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy import inspect
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import Session

from ai import prediction

from . import models, schemas
from .client_ops import ClientOPS
from .config import CORS_ORIGINS, MODELS_DIR
from .database import engine, get_db
from .utils import get_table_info

logger = logging.getLogger("wefizz")


def try_convert_to_float(value):
    try:
        return float(value)
    except ValueError:
        return value


@asynccontextmanager
async def lifespan(app: FastAPI):
    prediction.load_models(MODELS_DIR)  # fail fast if a model file is missing
    try:
        models.Base.metadata.create_all(bind=engine)
    except OperationalError:
        logger.warning("Database unreachable at startup; DB endpoints will return 503")
    yield


app = FastAPI(
    title="Garment Size Prediction API",
    description="Predicts body measurements (used for garment sizing) from gender, height, weight and morphology.",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["POST", "GET"],
    allow_headers=["*"],
)


@app.exception_handler(OperationalError)
async def db_unavailable(_, exc: OperationalError):
    return JSONResponse(status_code=503, content={"detail": "Database unavailable"})


@app.get("/")
async def root():
    return {"Data": "API started correctly!"}


@app.get("/health", tags=["Health"])
async def health():
    ok = prediction.models_loaded()
    return JSONResponse(
        status_code=200 if ok else 503,
        content={"status": "ok" if ok else "unavailable", "models_loaded": ok},
    )


@app.post("/predict", response_model=schemas.PredictResponse, tags=["Predict"])
def predict(req: schemas.PredictRequest):
    """Predict the full measurement set for one person (no database needed)."""
    measurements = prediction.predict_all(req.model_dump())
    return {"measurements": measurements}


@app.get("/check_client_table", tags=["Table Checks"])
async def check_client_table(db: Session = Depends(get_db)):
    info = get_table_info(db, "client")
    if info["exists"]:
        return {"table_name": "client", "columns": info["columns"]}
    raise HTTPException(status_code=404, detail="Table 'client' does not exist.")


@app.get("/check_db")
async def check_db(db: Session = Depends(get_db)):
    return {"tables": inspect(db.bind).get_table_names()}


@app.post("/add_client", status_code=status.HTTP_201_CREATED, tags=["Add Client"])
async def add_clients(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if file.content_type != "text/csv":
        raise HTTPException(status_code=400, detail="Invalid file format. Please upload a CSV file.")

    csv_data = StringIO(file.file.read().decode("utf-8"))

    try:
        df = pd.read_csv(csv_data, header=None).transpose()
        df.columns = df.iloc[0]
        df = df[1:].reset_index(drop=True)
        df = df.map(try_convert_to_float)
        df.loc[df["morphology"] == 8.0, "morphology"] = "8"
        df["morphology"] = df["morphology"].astype(str)

        clientOPS = ClientOPS(df)

        client_orms = [models.ClientORM(**m.model_dump()) for m in clientOPS.new_clients]
        other_orms = (
            [models.MeasureORM(**m.model_dump()) for m in clientOPS.new_clients_measures]
            + [models.MeasureAccuracyORM(**m.model_dump()) for m in clientOPS.new_clients_measures_accuracy]
            + [models.MeasurePredictionORM(**m.model_dump()) for m in clientOPS.new_clients_measures_prediction]
        )
        db.add_all(client_orms + other_orms)
        db.commit()

        for orm in client_orms + other_orms:
            db.refresh(orm)

        response_data = [dict(c.__dict__) for c in client_orms]
        for data in response_data:
            data.pop("_sa_instance_state", None)
        return {"data": response_data}

    except OperationalError:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"An error occurred while processing the data: {e}")


def _row_or_404(db: Session, orm, client_id: int) -> dict:
    row = db.query(orm).filter(orm.user_id == client_id).first()
    if row is None:
        raise HTTPException(status_code=404, detail="Client not found")
    return {k: v for k, v in row.__dict__.items() if k != "_sa_instance_state"}


@app.get("/get_measures_predictions/{client_id}", tags=["Get Measures Predictions"])
async def get_measures_predictions(client_id: int, db: Session = Depends(get_db)):
    return {"Measures Prediction": _row_or_404(db, models.MeasurePredictionORM, client_id)}


@app.get("/get_measures/{client_id}", tags=["Get Measures Corrected"])
async def get_measures(client_id: int, db: Session = Depends(get_db)):
    return {"Measures": _row_or_404(db, models.MeasureORM, client_id)}


@app.get("/get_measures_accuracy/{client_id}", tags=["Get Measures Accuracy"])
async def get_measures_accuracy(client_id: int, db: Session = Depends(get_db)):
    return {"Measures Accuracy": _row_or_404(db, models.MeasureAccuracyORM, client_id)}
