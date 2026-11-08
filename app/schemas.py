from typing import Literal, Optional, Union

from pydantic import BaseModel, Field, field_validator, model_validator


class ClientModel(BaseModel):

    user_id: Optional[int] = None
    height_cm: float
    weight_kg: float
    gender: int
    morphology: str

    class Config:
        from_attributes = True

class MeasuresModel(BaseModel):

    user_id: Optional[int] = None
    Head_Circumference: Optional[Union[float, str]] = None
    Biceps: Optional[Union[float, str]] = None
    Chest_Circumference: Optional[Union[float, str]] = None
    Waist_Circumference: Optional[Union[float, str]] = None
    Right_Knee: Optional[Union[float, str]] = None
    Left_Knee: Optional[Union[float, str]] = None
    Right_Thigh: Optional[Union[float, str]] = None
    Left_Thigh: Optional[Union[float, str]] = None
    Shoulder_Width: Optional[Union[float, str]] = None
    Trunk_Length: Optional[Union[float, str]] = None
    Right_Calf: Optional[Union[float, str]] = None
    Left_Calf: Optional[Union[float, str]] = None
    Leg_Length: Optional[Union[float, str]] = None
    Chest_Base: Optional[Union[float, str]] = None
    High_Hip: Optional[Union[float, str]] = None
    Low_Hip: Optional[Union[float, str]] = None
    Right_Elbow: Optional[Union[float, str]] = None
    Right_Thigh_Widest: Optional[Union[float, str]] = None
    Left_Thigh_Widest: Optional[Union[float, str]] = None
    Arm_Length: Optional[Union[float, str]] = None

    class Config:
        from_attributes = True

class MeasuresAccuracyModel(BaseModel):

    user_id: Optional[int] = None
    Head_Circumference_accuracy: Optional[float] = None
    Biceps_accuracy: Optional[float] = None
    Chest_Circumference_accuracy: Optional[float] = None
    Waist_Circumference_accuracy: Optional[float] = None
    Right_Knee_accuracy: Optional[float] = None
    Left_Knee_accuracy: Optional[float] = None
    Right_Thigh_accuracy: Optional[float] = None
    Left_Thigh_accuracy: Optional[float] = None
    Shoulder_Width_accuracy: Optional[float] = None
    Trunk_Length_accuracy: Optional[float] = None
    Right_Calf_accuracy: Optional[float] = None
    Left_Calf_accuracy: Optional[float] = None
    Leg_Length_accuracy: Optional[float] = None
    Chest_Base_accuracy: Optional[float] = None
    High_Hip_accuracy: Optional[float] = None
    Low_Hip_accuracy: Optional[float] = None
    Right_Elbow_accuracy: Optional[float] = None
    Right_Thigh_Widest_accuracy: Optional[float] = None
    Left_Thigh_Widest_accuracy: Optional[float] = None
    Arm_Length_accuracy: Optional[float] = None

    class Config:
        from_attributes = True

class PredictedMeasures(BaseModel):
    """Predicted body measurements, in cm."""

    Biceps: Optional[float] = None
    Chest_Circumference: Optional[float] = None
    Waist_Circumference: Optional[float] = None
    thigh: Optional[float] = None
    Shoulder_Width: Optional[float] = None
    Trunk_Length: Optional[float] = None
    calf: Optional[float] = None
    Leg_Length: Optional[float] = None
    Chest_Base: Optional[float] = None
    High_Hip: Optional[float] = None
    Low_Hip: Optional[float] = None
    Right_Elbow: Optional[float] = None
    Right_Thigh_Widest: Optional[float] = None
    knee: Optional[float] = None
    Arm_Length: Optional[float] = None
    Head_Circumference: Optional[float] = None


class MeasurePredictionModel(PredictedMeasures):
    user_id: Optional[int] = None

    class Config:
        from_attributes = True


class PredictRequest(BaseModel):
    gender: Literal[0, 1] = Field(description="0 = female, 1 = male")
    height_cm: float = Field(gt=100, lt=250)
    weight_kg: float = Field(gt=25, lt=300)
    morphology: Literal["A", "X", "8", "V", "H", "O"] = Field(
        description="Body shape. Female: A, X, 8, V, H, O. Male: H, V, O."
    )

    @field_validator("morphology", mode="before")
    @classmethod
    def _upper(cls, v):
        return v.upper() if isinstance(v, str) else v

    @model_validator(mode="after")
    def _morphology_matches_gender(self):
        if self.gender == 1 and self.morphology not in ("H", "V", "O"):
            raise ValueError("morphology for male (gender=1) must be one of H, V, O")
        return self


class PredictResponse(BaseModel):
    measurements: PredictedMeasures
