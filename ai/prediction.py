import joblib
import pandas as pd
import numpy as np

morphology_mapping_male = {'H': 0, 'V': 1, 'O': 2}
morphology_mapping_female = {'A': 0, 'X': 1, '8': 2, 'V': 3, 'H': 4, 'O': 5}

def predict(data):

    new_data = {
        'gender': [data['gender']],
        'height_cm': [data['height_cm']],
        'weight_kg': [data['weight_kg']],
        'morphology': [data["morphology"]]
    }

    new_df = pd.DataFrame(new_data)

    new_df['morphology'] = new_df.apply(lambda row: morphology_mapping_male[row['morphology']] if row['gender'] == 1 else morphology_mapping_female.get(row['morphology'], np.nan), axis=1)

    # print("Prepared Input Data:")
    # print(new_df)

    model = joblib.load('random_forest_model.pkl')
    predicted_values = model.predict(new_df)


    original_columns = [
        'ankle', 'arm-length', 'bicep', 'calf', 'chest', 'forearm', 
        'hip', 'leg-length', 'shoulder-breadth', 'shoulder-to-crotch', 
        'thigh', 'waist', 'wrist'
    ]

    predicted_df = pd.DataFrame(predicted_values, columns=original_columns)
    initial_features = predicted_df.to_dict()
    initial_features = {k: list(v.values())[0] for k, v in initial_features.items()}


    mapped_columns = {
        'bicep': 'Biceps',
        'chest': 'Chest_Circumference',
        'waist': 'Waist_Circumference',
        'thigh': 'thigh',
        'shoulder-breadth': 'Shoulder_Width',
        'shoulder-to-crotch': 'Trunk_Length',
        'calf': 'calf',
        'leg-length': 'Leg_Length',
        'forearm': 'forearm',
        'hip': 'hip',
        'wrist': 'wrist',
        'arm-length': 'Arm_Length'
    }

    predicted_df.rename(columns=mapped_columns, inplace=True)

    predicted_df['Leg_Length'] = predicted_df['Leg_Length']*1.16
    predicted_df['Chest_Base'] = predicted_df.apply(lambda row: row['Chest_Circumference'] * 0.86 if new_df.loc[row.name, 'gender'] == 0 else row['Chest_Circumference'] * 0.92, axis=1)
    predicted_df['High_Hip'] = predicted_df['hip'] * 0.95
    predicted_df['Low_Hip'] = predicted_df['hip'] * 1.05
    predicted_df['Right_Elbow'] = predicted_df['forearm'] + 2
    predicted_df['Right_Thigh_Widest'] = predicted_df['thigh'] * 1.25
    predicted_df['Arm_Length'] = predicted_df['Arm_Length']*1.16
    predicted_df['Shoulder_Width'] = predicted_df['Shoulder_Width']*1.2

    output_columns = [
        'Biceps', 'Chest_Circumference', 'Waist_Circumference',
        'Shoulder_Width', 'Trunk_Length', 'calf', 'Leg_Length', 
        'Chest_Base', 'High_Hip', 'Low_Hip', 'Right_Elbow', 
        'Right_Thigh_Widest', 'Arm_Length'
    ]
    
    predicted_measures = predicted_df[output_columns].to_dict()
    predicted_measures = {k: list(v.values())[0] for k, v in predicted_measures.items()}

    return initial_features, predicted_measures
