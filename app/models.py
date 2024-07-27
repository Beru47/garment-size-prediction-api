from .database import Base
from sqlalchemy import Column, Integer, Boolean, Float, CHAR, SmallInteger
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text

class ClientORM(Base):

    __tablename__ = "client"

    user_id = Column(Integer, primary_key = True, nullable= False, autoincrement=True)
    gender = Column(SmallInteger, nullable=False)
    adult = Column(Boolean, server_default="TRUE", nullable=False)
    height_cm = Column(Float, nullable=False)
    weight_kg = Column(Float, nullable=False)
    morphology = Column(CHAR, nullable = False)
    created_at = Column(TIMESTAMP(timezone=True), nullable= False, server_default=text("now()"))

class MeasureORM(Base):

    __tablename__ = "measures"

    user_id = Column(Integer, primary_key = True, nullable= False)
    Head_Circumference = Column(Float, nullable=True)
    Biceps = Column(Float, nullable=True)
    Chest_Circumference = Column(Float, nullable=True)
    Waist_Circumference = Column(Float, nullable=True)
    Right_Knee = Column(Float, nullable=True)
    Left_Knee = Column(Float, nullable=True)
    Right_Thigh = Column(Float, nullable=True)
    Left_Thigh = Column(Float, nullable=True)
    Shoulder_Width = Column(Float, nullable=True)
    Trunk_Length = Column(Float, nullable=True)
    Right_Calf = Column(Float, nullable=True)
    Left_Calf = Column(Float, nullable=True)
    Leg_Length = Column(Float, nullable=True)
    Chest_Base = Column(Float, nullable=True)
    High_Hip = Column(Float, nullable=True)
    Low_Hip = Column(Float, nullable=True)
    Right_Elbow = Column(Float, nullable=True)
    Right_Thigh_Widest = Column(Float, nullable=True)
    Left_Thigh_Widest = Column(Float, nullable=True)
    Arm_Length = Column(Float, nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable= False, server_default=text("now()"))

class MeasureAccuracyORM(Base):

    __tablename__ = "measures_accuracy"

    user_id = Column(Integer, primary_key = True, nullable= False)
    Head_Circumference_accuracy = Column(Float, nullable=True)
    Biceps_accuracy = Column(Float, nullable=True)
    Chest_Circumference_accuracy = Column(Float, nullable=True)
    Waist_Circumference_accuracy = Column(Float, nullable=True)
    Right_Knee_accuracy = Column(Float, nullable=True)
    Left_Knee_accuracy = Column(Float, nullable=True)
    Right_Thigh_accuracy = Column(Float, nullable=True)
    Left_Thigh_accuracy = Column(Float, nullable=True)
    Shoulder_Width_accuracy = Column(Float, nullable=True)
    Trunk_Length_accuracy = Column(Float, nullable=True)
    Right_Calf_accuracy = Column(Float, nullable=True)
    Left_Calf_accuracy = Column(Float, nullable=True)
    Leg_Length_accuracy = Column(Float, nullable=True)
    Chest_Base_accuracy = Column(Float, nullable=True)
    High_Hip_accuracy = Column(Float, nullable=True)
    Low_Hip_accuracy = Column(Float, nullable=True)
    Right_Elbow_accuracy = Column(Float, nullable=True)
    Right_Thigh_Widest_accuracy = Column(Float, nullable=True)
    Left_Thigh_Widest_accuracy = Column(Float, nullable=True)
    Arm_Length_accuracy = Column(Float, nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable= False, server_default=text("now()"))

class MeasurePredictionORM(Base):

    __tablename__ = "measures_prediction"

    user_id = Column(Integer, primary_key = True, nullable= False)
    Biceps = Column(Float, nullable=True)
    Chest_Circumference = Column(Float, nullable=True)
    Waist_Circumference = Column(Float, nullable=True)
    thigh = Column(Float, nullable=True)
    Shoulder_Width = Column(Float, nullable=True)
    Trunk_Length = Column(Float, nullable=True)
    calf = Column(Float, nullable=True)
    Leg_Length = Column(Float, nullable=True)
    Chest_Base = Column(Float, nullable=True)
    High_Hip = Column(Float, nullable=True)
    Low_Hip = Column(Float, nullable=True)
    Right_Elbow = Column(Float, nullable=True)
    Right_Thigh_Widest = Column(Float, nullable=True)
    knee = Column(Float, nullable=True)
    Arm_Length = Column(Float, nullable=True)
    Head_Circumference = Column(Float, nullable=True)
