"""Body-measurement prediction from gender, height, weight and morphology.

A multi-output random forest predicts 13 base measurements; three dedicated
regressors (knee, head circumference, thigh) refine specific ones. Models are
loaded once with `load_models` (called at API startup).
"""
from pathlib import Path

import joblib
import numpy as np
import pandas as pd

MORPHOLOGY_MALE = {"H": 0, "V": 1, "O": 2}
MORPHOLOGY_FEMALE = {"A": 0, "X": 1, "8": 2, "V": 3, "H": 4, "O": 5}

HEAD_CIRC_OFFSET_CM = 1.4

MODEL_FILES = {
    "body": "body_measurements_rf.pkl",
    "head": "head_circumference.pkl",
    "knee": "knee_rf.pkl",
    "thigh": "thigh.pkl",
}

BASE_COLUMNS = [
    "ankle", "arm-length", "bicep", "calf", "chest", "forearm", "hip",
    "leg-length", "shoulder-breadth", "shoulder-to-crotch", "thigh", "waist", "wrist",
]

_models: dict = {}


class ModelsNotLoadedError(RuntimeError):
    pass


def load_models(models_dir: Path) -> None:
    """Load every model once; raises FileNotFoundError naming the missing file."""
    for key, name in MODEL_FILES.items():
        path = Path(models_dir) / name
        if not path.is_file():
            raise FileNotFoundError(f"Model file not found: {path}")
        _models[key] = joblib.load(path)


def models_loaded() -> bool:
    return set(_models) == set(MODEL_FILES)


def _model(key: str):
    if key not in _models:
        raise ModelsNotLoadedError("Models are not loaded; call load_models() first")
    return _models[key]


def predict(data: dict):
    """Return (base features, derived measurements) for one client."""
    gender = data["gender"]
    mapping = MORPHOLOGY_MALE if gender == 1 else MORPHOLOGY_FEMALE
    new_df = pd.DataFrame({
        "gender": [gender],
        "height_cm": [data["height_cm"]],
        "weight_kg": [data["weight_kg"]],
        "morphology": [mapping.get(data["morphology"], np.nan)],
    })

    values = _model("body").predict(new_df)
    predicted_df = pd.DataFrame(values, columns=BASE_COLUMNS)
    initial_features = {k: v[0] for k, v in predicted_df.to_dict("list").items()}

    predicted_df = predicted_df.rename(columns={
        "bicep": "Biceps", "chest": "Chest_Circumference", "waist": "Waist_Circumference",
        "shoulder-breadth": "Shoulder_Width", "shoulder-to-crotch": "Trunk_Length",
        "leg-length": "Leg_Length", "arm-length": "Arm_Length",
    })
    df = predicted_df
    df["Leg_Length"] = df["Leg_Length"] * 1.16
    df["Chest_Base"] = df["Chest_Circumference"] * (0.86 if gender == 0 else 0.92)
    df["High_Hip"] = df["hip"] * 0.95
    df["Low_Hip"] = df["hip"] * 1.05
    df["Right_Elbow"] = df["forearm"] + 2
    df["Right_Thigh_Widest"] = df["thigh"] * 1.25
    df["Arm_Length"] = df["Arm_Length"] * 1.16
    df["Shoulder_Width"] = df["Shoulder_Width"] * 1.2

    output_columns = [
        "Biceps", "Chest_Circumference", "Waist_Circumference", "Shoulder_Width",
        "Trunk_Length", "calf", "Leg_Length", "Chest_Base", "High_Hip", "Low_Hip",
        "Right_Elbow", "Right_Thigh_Widest", "Arm_Length",
    ]
    measures = {k: v[0] for k, v in df[output_columns].to_dict("list").items()}
    return initial_features, measures


def predict_knee(client: dict, f: dict) -> float:
    row = {k: float(f[k]) for k in ("ankle", "bicep", "calf", "chest", "forearm", "hip")}
    row["shoulder_breadth"] = float(f["shoulder-breadth"])
    row.update({k: float(f[k]) for k in ("thigh", "waist", "wrist")})
    row["weight_kg"] = float(client["weight_kg"])
    row["height_cm"] = float(client["height_cm"])
    row["gender"] = int(client["gender"])
    return float(_model("knee").predict(pd.DataFrame([row]))[0])


def predict_head(client: dict, f: dict) -> float:
    df = pd.DataFrame({
        "height_cm": [float(client["height_cm"])],
        "weight_kg": [float(client["weight_kg"])],
        "wrist": [float(f["wrist"])],
    })
    return float(_model("head").predict(df)[0]) + HEAD_CIRC_OFFSET_CM


def predict_thigh(client: dict, f: dict) -> float:
    df = pd.DataFrame([{
        "weight_kg": client["weight_kg"],
        "ankle": f["ankle"],
        "hip": f["hip"],
        "thigh_widest": f["thigh"] * 1.25,
    }])
    return float(_model("thigh").predict(df)[0])


def predict_all(client: dict) -> dict:
    """Full measurement set for one client (the API's prediction pipeline)."""
    features, measures = predict(client)
    measures = {k: float(v) for k, v in measures.items()}
    measures["knee"] = predict_knee(client, features)
    measures["Head_Circumference"] = predict_head(client, features)
    measures["thigh"] = predict_thigh(client, features)
    return measures
