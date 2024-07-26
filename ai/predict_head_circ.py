import pandas as pd
from joblib import load

error = 1.4

def predict_head_circ(data):

    rf_loaded = load('head_circumference_predictor.pkl')

    new_data = pd.DataFrame({
        'height_cm': [data['height_cm']],
        'weight_kg': [data['weight_kg']],
        'wrist': [data['wrist']]
    })

    predicted_head_circumference = rf_loaded.predict(new_data)
    return predicted_head_circumference[0] + error
