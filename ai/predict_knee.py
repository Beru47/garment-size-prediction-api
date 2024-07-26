import pandas as pd
import joblib

model_filename = 'rf_regressor_knee_diameter.pkl'
loaded_model = joblib.load(model_filename)

def predict_knee_diameter(input_dict):
    
    input_df = pd.DataFrame([input_dict])
    prediction = loaded_model.predict(input_df)
    return prediction[0]
