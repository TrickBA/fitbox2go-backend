
# src/models/TrainingModel.py
from marshmallow import fields, Schema
import datetime
from . import db
from .ResultModel import ResultSchema


class TrainingModel(db.Model):
    """
    Training Model
    """

    __tablename__ = 'trainings'

    training_id = db.Column(db.Integer, primary_key=True)
    exercise_id = db.Column(db.Integer, db.ForeignKey("exercises.exercise_id"), nullable=False)
    performed_reps = db.Column(db.Integer, nullable=False)
    performed_series = db.Column(db.Integer, nullable=False)
    valid_until_date_time = db.Column(db.DateTime, nullable=True)
    end_date_time = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime)
    modified_at = db.Column(db.DateTime)
    results = db.relationship('ResultModel', backref='results', lazy=True)

    # class constructor
    def __init__(self, data):
        """
        Class constructor
        """
        self.exercise_id = data.get('exercise_id')
        self.performed_reps = data.get('performed_reps')
        self.performed_series = data.get('performed_series')
        self.created_at = datetime.datetime.utcnow()
        self.modified_at = datetime.datetime.utcnow()

    def save(self):
        db.session.add(self)
        current_training = TrainingModel.get_active_training_by_exercise(self.exercise_id)
        if current_training is not None:
            current_training.valid_until_date_time = self.created_at
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
    def get_all_trainings():
        return TrainingModel.query.all()

    @staticmethod
    def get_one_training(training_id):
        return TrainingModel.query.get(training_id)

    @staticmethod
    def get_trainings_by_exercise(exercise_id):
        return TrainingModel.query.filter_by(exercise_id=exercise_id).all()

    @staticmethod
    def get_active_training_by_exercise(exercise_id):
        return TrainingModel.query.filter_by(exercise_id=exercise_id, valid_until_date_time=None).first()

    def __repr(self):
        return '<training_id {}>'.format(self.training_id)


class TrainingSchema(Schema):
    """
    TrainingSchema
    """
    training_id = fields.Int(dump_only=True)
    exercise_id = fields.Int(required=True)
    performed_reps = fields.Int(required=True)
    performed_series = fields.Int(required=True)
    valid_until_date_time = fields.DateTime()
    end_date_time = fields.DateTime()
    created_at = fields.DateTime()
    modified_at = fields.DateTime(dump_only=True)
    results = fields.Nested(ResultSchema, many=True)
