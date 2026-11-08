import pandas as pd

from ai import prediction

from . import schemas


class ClientOPS:

    PAIRED = {
        "calf": ("Right_Calf", "Left_Calf"),
        "Right_Thigh_Widest": ("Right_Thigh_Widest", "Left_Thigh_Widest"),
        "thigh": ("Right_Thigh", "Left_Thigh"),
        "knee": ("Right_Knee", "Left_Knee"),
    }

    @staticmethod
    def _ratio(a, b):
        return min(a, b) / max(a, b) * 100

    @staticmethod
    def get_measures_accuracy(predicted_measures, client_measures_model, client_data):
        """Accuracy (%) of each prediction vs the measured value; fills missing measures with the prediction."""
        measures_accuracy = {}
        for measure, predicted in predicted_measures.items():
            for field in ClientOPS.PAIRED.get(measure, (measure,)):
                actual = getattr(client_measures_model, field) if measure in ClientOPS.PAIRED else client_data[measure]
                if isinstance(actual, str):
                    setattr(client_measures_model, field, predicted)
                else:
                    measures_accuracy[field + "_accuracy"] = ClientOPS._ratio(actual, predicted)

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

            predicted_measures = prediction.predict_all(client)

            client_measures_prediction = predicted_measures.copy()
            client_measures_prediction["user_id"] = client_data["user_id"]
            client_measures_prediction_model = schemas.MeasurePredictionModel(**client_measures_prediction)

            measures_accuracy = ClientOPS.get_measures_accuracy(predicted_measures, client_measures_model, client_data)
            client_measures_accuracy_model = schemas.MeasuresAccuracyModel(**measures_accuracy)

            self.new_clients.append(client_model)
            self.new_clients_measures.append(client_measures_model)
            self.new_clients_measures_accuracy.append(client_measures_accuracy_model)
            self.new_clients_measures_prediction.append(client_measures_prediction_model)
