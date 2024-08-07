from fastapi import Depends, FastAPI, status, HTTPException, UploadFile, File
from . import models
from .database import engine, get_db
from .utils import  get_table_info
from sqlalchemy.orm import Session
from sqlalchemy import inspect
import pandas as pd
from io import StringIO
from .ClientOPS import ClientOPS
from fastapi.middleware.cors import CORSMiddleware

def try_convert_to_float(value):
    try:
        return float(value)
    except ValueError:
        return value

models.Base.metadata.create_all(bind = engine)

app = FastAPI()

origins = [
    "http://127.0.0.1:5500",  
    "http://localhost:5500", 
    "http://localhost"
]



app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["POST", "GET"],
    allow_headers=["*"],
)

@app.get("/check_client_table", tags=["Table Checks"])
async def check_client_table(db: Session = Depends(get_db)):
    info = get_table_info(db, "client")
    if info["exists"]:
        return {"table_name": "client", "columns": info["columns"]}
    else:
        raise HTTPException(status_code=404, detail="Table 'client' does not exist.")

@app.get("/check_db")
async def check_db(db: Session = Depends(get_db)):
    inspector = inspect(db.bind)
    tables = inspector.get_table_names()
    return {"tables": tables}


@app.get("/")
async def root():
    return {"Data": "API started correctly!"}

@app.post("/add_client", status_code=status.HTTP_201_CREATED, tags=["Add Client"])
async def add_clients(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if file.content_type != 'text/csv':
        raise HTTPException(status_code=400, detail="Invalid file format. Please upload a CSV file.")

    content = file.file.read().decode("utf-8")
    csv_data = StringIO(content)
    
    try:
        df = pd.read_csv(csv_data, header=None)
        df = df.transpose()
        df.columns = df.iloc[0]
        df = df[1:]
        df.reset_index(drop=True, inplace=True)
    
        df = df.map(try_convert_to_float)
        df.loc[df['morphology'] == 8.0, 'morphology'] = '8'
        df['morphology'] = df['morphology'].astype(str)
        
        clientOPS = ClientOPS(df)

        new_client_orms = []
        new_clients_measures_orms = []
        new_clients_measures_accuracy_orms = []
        new_clients_measures_prediction_orms = []

        for client_model in clientOPS.new_clients:
            client_orm = models.ClientORM(**client_model.dict())
            new_client_orms.append(client_orm)
            db.add(client_orm)
        
        for measures_model in clientOPS.new_clients_measures:
            measures_orm = models.MeasureORM(**measures_model.dict())
            new_clients_measures_orms.append(measures_orm)
            db.add(measures_orm)
        
        for measures_accuracy_model in clientOPS.new_clients_measures_accuracy:
            measures_accuracy_orm = models.MeasureAccuracyORM(**measures_accuracy_model.dict())
            new_clients_measures_accuracy_orms.append(measures_accuracy_orm)
            db.add(measures_accuracy_orm)
        
        for measures_prediction_model in clientOPS.new_clients_measures_prediction:
            measures_prediction_orm = models.MeasurePredictionORM(**measures_prediction_model.dict())
            new_clients_measures_prediction_orms.append(measures_prediction_orm)
            db.add(measures_prediction_orm)
        
        db.commit()

        for client_orm in new_client_orms:
            db.refresh(client_orm)
            
        for measures_orm in new_clients_measures_orms:
            db.refresh(measures_orm)

        for measures_accuracy_orm in new_clients_measures_accuracy_orms:
            db.refresh(measures_accuracy_orm)
            
        for measures_prediction_orm in new_clients_measures_prediction_orms:
            db.refresh(measures_prediction_orm)

        response_data = [client.__dict__ for client in new_client_orms]
        for data in response_data:
            data.pop('_sa_instance_state', None)  

        return {"data": response_data}

    except Exception as e:
        print(f"An error occurred: {e}")  # Print the error for debugging
        db.rollback()
        raise HTTPException(status_code=500, detail=f"An error occurred while processing the data: {str(e)}")


@app.get("/get_measures_predictions/{client_id}", tags=["Get Measures Predictions"])
async def get_measures(client_id: int, db: Session = Depends(get_db)):
        client_measures_prediction = db.query(models.MeasurePredictionORM).filter(models.MeasurePredictionORM.user_id == client_id).first()
        if client_measures_prediction is None:
            raise HTTPException(status_code=404, detail="Client not found")
        return {"Measures Prediction": client_measures_prediction.__dict__}

@app.get("/get_measures/{client_id}", tags=["Get Measures Corrected"])
async def get_measures(client_id: int, db: Session = Depends(get_db)):
        client_measures = db.query(models.MeasureORM).filter(models.MeasureORM.user_id == client_id).first()
        if client_measures is None:
            raise HTTPException(status_code=404, detail="Client not found")
        return {"Measures": client_measures.__dict__}

@app.get("/get_measures_accuracy/{client_id}", tags=["Get Measures Accuracy"])
async def get_measures(client_id: int, db: Session = Depends(get_db)):
        client_measures_accuracy = db.query(models.MeasureAccuracyORM).filter(models.MeasureAccuracyORM.user_id == client_id).first()
        if client_measures_accuracy is None:
            raise HTTPException(status_code=404, detail="Client not found")
        return {"Measures Accuracy": client_measures_accuracy.__dict__}
