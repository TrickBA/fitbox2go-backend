# src/models/ExerciseModel.py
from marshmallow import fields, Schema
import datetime
from . import db
from .ExerciseTypeModel import ExerciseTypeModel
from .TrainingModel import TrainingSchema


class ExerciseModel(db.Model):
    """
    Exercise Model
    """

    __tablename__ = 'exercises'

    exercise_id = db.Column(db.Integer, primary_key=True)
    exercise_type_id = db.Column(db.Integer, db.ForeignKey("exercise_types.exercise_type_id"), nullable=False)
    schedule_id = db.Column(db.Integer, db.ForeignKey("daily_schedules.schedule_id"), nullable=False)
    order = db.Column(db.Integer, nullable=False)
    is_completed = db.Column(db.Boolean, nullable=False)
    reps = db.Column(db.Integer, nullable=False)
    series = db.Column(db.Integer, nullable=False)
    weight = db.Column(db.Float, nullable=False)
    rest = db.Column(db.Integer, nullable=False)
    speed = db.Column(db.Integer, nullable=False)
    range_of_motion = db.Column(db.Integer, nullable=False)
    leftarmplate_level = db.Column(db.Integer, nullable=False)
    rightarmplate_level = db.Column(db.Integer, nullable=False)
    middleplate_level = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime)
    modified_at = db.Column(db.DateTime)
    trainings = db.relationship('TrainingModel', backref='trainings', lazy=True)

    # class constructor
    def __init__(self, data, ex_type: ExerciseTypeModel):
        """
        Class constructor
        """
        self.exercise_type_id = data.get('exercise_type_id')
        self.schedule_id = data.get('schedule_id')
        self.is_completed = False
        self.reps = data.get('reps') | ex_type.default_reps
        self.series = data.get('series') | ex_type.default_series
        self.weight = data.get('weight') | ex_type.default_weight
        self.rest = data.get('rest') | ex_type.default_rest
        self.speed = data.get('speed') | ex_type.default_speed
        self.range_of_motion = data.get('range_of_motion') | ex_type.default_range_of_motion
        self.leftarmplate_level = data.get('leftarmplate_level') | ex_type.default_leftarmplate_level
        self.rightarmplate_level = data.get('rightarmplate_level') | ex_type.default_rightarmplate_level
        self.middleplate_level = data.get('middleplate_level') | ex_type.default_middleplate_level
        self.created_at = datetime.datetime.utcnow()
        self.modified_at = datetime.datetime.utcnow()
        self.order = data.get('order')

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self, data):
        for key, item in data.items():
            setattr(self, key, item)
        self.modified_at = datetime.datetime.utcnow()
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def get_all_exercises():
        return ExerciseModel.query.all()

    @staticmethod
    def get_one_exercise(exercise_id):
        return ExerciseModel.query.get(exercise_id)

    def __repr(self):
        return '<exercise_id {}>'.format(self.exercise_id)


class ExerciseSchema(Schema):
    """
    Exercise Schema
    """
    exercise_id = fields.Int(dump_only=True)
    exercise_type_id = fields.Int(required=True)
    schedule_id = fields.Int(required=True)
    order = fields.Int(required=True)
    is_completed = fields.Bool()
    reps = fields.Int()
    series = fields.Int()
    weight = fields.Float()
    rest = fields.Int()
    speed = fields.Int()
    range_of_motion = fields.Int()
    leftarmplate_level = fields.Int()
    rightarmplate_level = fields.Int()
    middleplate_level = fields.Int()
    created_at = fields.DateTime(dump_only=True)
    modified_at = fields.DateTime(dump_only=True)
    trainings = fields.Nested(TrainingSchema, many=True)
