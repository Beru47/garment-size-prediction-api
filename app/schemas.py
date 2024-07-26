from pydantic import BaseModel
from typing import Union

class ClientModel(BaseModel):

    user_id: int = None
    height_cm: float
    weight_kg: float
    gender: int
    morphology: str

    class Config:
        from_attributes = True 

class MeasuresModel(BaseModel):

    user_id: int = None
    Head_Circumference: Union[float, str] = None
    Biceps: Union[float, str] = None
    Chest_Circumference: Union[float, str] = None
    Waist_Circumference: Union[float, str] = None
    Right_Knee: Union[float, str] = None
    Left_Knee: Union[float, str] = None
    Right_Thigh: Union[float, str] = None
    Left_Thigh: Union[float, str] = None
    Shoulder_Width: Union[float, str] = None
    Trunk_Length: Union[float, str] = None
    Right_Calf: Union[float, str] = None
    Left_Calf: Union[float, str] = None
    Leg_Length: Union[float, str] = None
    Chest_Base: Union[float, str] = None
    High_Hip: Union[float, str] = None
    Low_Hip: Union[float, str] = None
    Right_Elbow: Union[float, str] = None
    Right_Thigh_Widest: Union[float, str] = None
    Left_Thigh_Widest: Union[float, str] = None
    Arm_Length: Union[float, str] = None

    class Config:
        from_attributes = True

class MeasuresAccuracyModel(BaseModel):

    user_id: int = None
    Head_Circumference_accuracy: float = None
    Biceps_accuracy: float = None
    Chest_Circumference_accuracy: float = None
    Waist_Circumference_accuracy: float = None
    Right_Knee_accuracy: float = None
    Left_Knee_accuracy: float = None
    Right_Thigh_accuracy: float = None
    Left_Thigh_accuracy: float = None
    Shoulder_Width_accuracy: float = None
    Trunk_Length_accuracy: float = None
    Right_Calf_accuracy: float = None
    Left_Calf_accuracy: float = None
    Leg_Length_accuracy: float = None
    Chest_Base_accuracy: float = None
    High_Hip_accuracy: float = None
    Low_Hip_accuracy: float = None
    Right_Elbow_accuracy: float = None
    Right_Thigh_Widest_accuracy: float = None
    Left_Thigh_Widest_accuracy: float = None
    Arm_Length_accuracy: float = None

    class Config:
        from_attributes = True

class MeasurePredictionModel(BaseModel):

    user_id: int = None
    Biceps: float = None
    Chest_Circumference: float = None
    Waist_Circumference: float = None
    thigh: float = None
    Shoulder_Width: float = None
    Trunk_Length: float = None
    calf: float = None
    Leg_Length: float = None
    Chest_Base: float = None
    High_Hip: float = None
    Low_Hip: float = None
    Right_Elbow: float = None
    Right_Thigh_Widest: float = None
    knee: float = None
    Arm_Length: float = None
    Head_Circumference: float = None

    class Config:
        from_attributes = True