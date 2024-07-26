from ai import prediction, predict_knee, predict_head_circ, predict_thigh
from . import schemas
import pandas as pd

class ClientOPS:

    @staticmethod
    def get_predicted_measures(predicted_measures):

        for key, value in predicted_measures.items():
            try:
                predicted_measures[key] = float(value)
            except ValueError:
                predicted_measures[key] = value

        return predicted_measures
    
    @staticmethod
    def get_predicted_knee_circumference(client, initial_features):
            
        input_data = {}

        input_data['ankle'] = float(initial_features['ankle'])
        input_data['bicep'] = float(initial_features['bicep'])
        input_data['calf'] = float(initial_features['calf'])
        input_data['chest'] = float(initial_features['chest'])
        input_data['forearm'] = float(initial_features['forearm'])
        input_data['hip'] = float(initial_features['hip'])
        input_data['shoulder_breadth'] = float(initial_features['shoulder-breadth'])
        input_data['thigh'] = float(initial_features['thigh'])
        input_data['waist'] = float(initial_features['waist'])
        input_data['wrist'] = float(initial_features['wrist'])
        input_data['weight_kg'] = float(client['weight_kg'])
        input_data['height_cm'] = float(client['height_cm'])
        input_data['gender'] = int(client['gender'])  

        predicted_knee_girth = predict_knee.predict_knee_diameter(input_data)

        return predicted_knee_girth
    

    @staticmethod
    def get_predicted_head_circumference(client, initial_features):
            
        input_data = {}

        input_data['wrist'] = float(initial_features['wrist'])
        input_data['weight_kg'] = float(client['weight_kg'])
        input_data['height_cm'] = float(client['height_cm'])

        predicted_head_circ = predict_head_circ.predict_head_circ(input_data)

        return predicted_head_circ
    
    @staticmethod
    def get_predicted_thigh(client, initial_features):
        
        data = {
            'weight_kg': client['weight_kg'],
            'ankle': initial_features['ankle'],
            'hip': initial_features['hip'],
            'thigh_widest': initial_features['thigh']*1.25
        }

        predicted_thigh = predict_thigh.predict(data)
        return predicted_thigh

    @staticmethod
    def get_measures_accuracy(predicted_measures, client_measures_model, client_data):

        measures_accuracy = dict()
        for measure in predicted_measures.keys():
            if measure == "calf":
                if isinstance(client_measures_model.Right_Calf, str):
                    client_measures_model.Right_Calf = predicted_measures["calf"]
                else:
                    measures_accuracy["Right_Calf_accuracy"] = (min(client_measures_model.Right_Calf, predicted_measures["calf"]) / max(client_measures_model.Right_Calf, predicted_measures["calf"])) * 100

                if isinstance(client_measures_model.Left_Calf, str):
                    client_measures_model.Left_Calf = predicted_measures["calf"]
                else:
                    measures_accuracy["Left_Calf_accuracy"] = (min(client_measures_model.Left_Calf, predicted_measures["calf"]) / max(client_measures_model.Left_Calf, predicted_measures["calf"])) * 100

            elif measure == "Right_Thigh_Widest":
                if isinstance(client_measures_model.Right_Thigh_Widest, str):
                    client_measures_model.Right_Thigh_Widest = predicted_measures["Right_Thigh_Widest"]
                else:
                    measures_accuracy["Right_Thigh_Widest_accuracy"] = (min(client_measures_model.Right_Thigh_Widest, predicted_measures["Right_Thigh_Widest"]) / max(client_measures_model.Right_Thigh_Widest, predicted_measures["Right_Thigh_Widest"])) * 100

                if isinstance(client_measures_model.Left_Thigh_Widest, str):
                    client_measures_model.Left_Thigh_Widest = predicted_measures["Right_Thigh_Widest"]
                else:
                    measures_accuracy["Left_Thigh_Widest_accuracy"] = (min(client_measures_model.Left_Thigh_Widest, predicted_measures["Right_Thigh_Widest"]) / max(client_measures_model.Left_Thigh_Widest, predicted_measures["Right_Thigh_Widest"])) * 100

            elif measure == "thigh":
                if isinstance(client_measures_model.Right_Thigh, str):
                    client_measures_model.Right_Thigh = predicted_measures["thigh"]
                else:
                    measures_accuracy["Right_Thigh_accuracy"] = (min(client_measures_model.Right_Thigh, predicted_measures["thigh"]) / max(client_measures_model.Right_Thigh, predicted_measures["thigh"])) * 100

                if isinstance(client_measures_model.Left_Thigh, str):
                    client_measures_model.Left_Thigh = predicted_measures["thigh"]
                else:
                    measures_accuracy["Left_Thigh_accuracy"] = (min(client_measures_model.Left_Thigh, predicted_measures["thigh"]) / max(client_measures_model.Left_Thigh, predicted_measures["thigh"])) * 100

            elif measure == "knee":
                if isinstance(client_measures_model.Right_Knee, str):
                    client_measures_model.Right_Knee = predicted_measures["knee"]
                else:
                    measures_accuracy["Right_Knee_accuracy"] = (min(client_measures_model.Right_Knee, predicted_measures["knee"]) / max(client_measures_model.Right_Knee, predicted_measures["knee"])) * 100

                if isinstance(client_measures_model.Left_Knee, str):
                    client_measures_model.Left_Knee = predicted_measures["knee"]
                else:
                    measures_accuracy["Left_Knee_accuracy"] = (min(client_measures_model.Left_Knee, predicted_measures["knee"]) / max(client_measures_model.Left_Knee, predicted_measures["knee"])) * 100

            else:
                if isinstance(client_data[measure], str):
                    setattr(client_measures_model, measure, predicted_measures[measure])
                else:
                    measures_accuracy[measure + "_accuracy"] = (min(client_data[measure], predicted_measures[measure]) / max(client_data[measure], predicted_measures[measure])) * 100

        measures_accuracy["user_id"] = client_data["user_id"]

        return measures_accuracy
    

    def __init__(self, df):

        assert isinstance(df, pd.DataFrame)

        self.new_clients = []
        self.new_clients_measures = []
        self.new_clients_measures_accuracy = []
        self.new_clients_measures_prediction = []

        for _, row in df.iterrows():
            client_data = row.to_dict()
            client_model = schemas.ClientModel(**client_data)
            client_measures_model = schemas.MeasuresModel(**client_data)

            client = client_model.model_dump()
            del client["user_id"]

            initial_features, initial_predicted_measures = prediction.predict(client)

            predicted_measures = ClientOPS.get_predicted_measures(initial_predicted_measures)
            predicted_measures["knee"] = ClientOPS.get_predicted_knee_circumference(client, initial_features)
            predicted_measures["Head_Circumference"] = ClientOPS.get_predicted_head_circumference(client, initial_features)
            predicted_measures["thigh"] = ClientOPS.get_predicted_thigh(client, initial_features)

            client_measures_prediction = predicted_measures.copy()
            client_measures_prediction["user_id"] = client_data["user_id"]
            client_measures_prediction_model = schemas.MeasurePredictionModel(**client_measures_prediction)

            measures_accuracy = ClientOPS.get_measures_accuracy(predicted_measures, client_measures_model, client_data)
            client_measures_accuracy_model = schemas.MeasuresAccuracyModel(**measures_accuracy)
            
            self.new_clients.append(client_model)
            self.new_clients_measures.append(client_measures_model)
            self.new_clients_measures_accuracy.append(client_measures_accuracy_model)
            self.new_clients_measures_prediction.append(client_measures_prediction_model)
            