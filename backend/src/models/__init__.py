# src/models/__init__.py

from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

# initialize our db
db = SQLAlchemy()
bcrypt = Bcrypt()

from .UserModel import UserModel, UserSchema
from .FitboxModel import FitboxModel, FitboxSchema
from .ExerciseTypeModel import ExerciseTypeModel, ExerciseTypeSchema
from .MedicalCheckModel import MedicalCheckModel, MedicalCheckSchema
from .PatientInfoModel import PatientInfoModel, PatientInfoSchema
from .ResultModel import ResultModel, ResultSchema
from .TrainingModel import TrainingModel, TrainingSchema
from .ResultTypeModel import ResultTypeModel, ResultTypeSchema
from .DailyScheduleModel import  DailyScheduleModel, DailyScheduleSchema
from .ExerciseModel import  ExerciseModel, ExerciseSchema
