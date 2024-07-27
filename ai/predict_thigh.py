import pandas as pd
import joblib

model_filename = 'thigh_predictor.pkl'
loaded_model = joblib.load(model_filename)

def predict(input_dict):
    
    input_df = pd.DataFrame([input_dict])
    prediction = loaded_model.predict(input_df)
    return prediction[0]
