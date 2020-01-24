# src/models/ExerciseTypeModel.py
from marshmallow import fields, Schema
import datetime
from . import db


class ExerciseTypeModel(db.Model):
    """
    ExerciseType Model
    """

    __tablename__ = 'exercise_types'

    exercise_type_id = db.Column(db.Integer, primary_key=True)
    action = db.Column(db.String(32), nullable=False)
    description = db.Column(db.String(128), nullable=True)
    default_reps = db.Column(db.Integer, nullable=True)
    default_series = db.Column(db.Integer, nullable=True)
    default_weight = db.Column(db.Float, nullable=True)
    default_rest = db.Column(db.Integer, nullable=True)
    default_speed = db.Column(db.Integer, nullable=True)
    default_range_of_motion = db.Column(db.Integer, nullable=True)
    level = db.Column(db.Integer, nullable=False)
    video_link = db.Column(db.String(128), nullable=True)
    default_leftarmplate_level = db.Column(db.Integer, nullable=True)
    default_rightarmplate_level = db.Column(db.Integer, nullable=True)
    default_middleplate_level = db.Column(db.Integer, nullable=True)
    created_at = db.Column(db.DateTime)
    modified_at = db.Column(db.DateTime)

    # class constructor
    def __init__(self, data):
        """
        Class constructor
        """
        self.action = data.get('action')
        self.description = data.get('description')
        self.default_reps = data.get('default_reps')
        self.default_series = data.get('default_series')
        self.default_weight = data.get('default_weight')
        self.default_rest = data.get('default_rest')
        self.default_speed = data.get('default_speed')
        self.default_range_of_motion = data.get('default_range_of_motion')
        self.level = data.get('level')
        self.video_link = data.get('video_link')
        self.default_leftarmplate_level = data.get('default_leftarmplate_level')
        self.default_rightarmplate_level = data.get('default_rightarmplate_level')
        self.default_middleplate_level = data.get('default_middleplate_level')
        self.created_at = datetime.datetime.utcnow()
        self.modified_at = datetime.datetime.utcnow()

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
    def get_all_exercise_types():
        return ExerciseTypeModel.query.all()

    @staticmethod
    def get_one_exercise_type(exercise_type_id):
        return ExerciseTypeModel.query.get(exercise_type_id)

    def __repr(self):
        return '<exercise_type_id {}>'.format(self.exercise_type_id)


class ExerciseTypeSchema(Schema):
    """
    ExerciseType Schema
    """
    exercise_type_id = fields.Int(dump_only=True)
    action = fields.Str(required=True)
    description = fields.Str()
    default_reps = fields.Int()
    default_series = fields.Int()
    default_weight = fields.Float()
    default_rest = fields.Int()
    default_speed = fields.Int()
    default_range_of_motion = fields.Int()
    level = fields.Int(required=True)
    video_link = fields.Str()
    default_leftarmplate_level = fields.Int()
    default_rightarmplate_level = fields.Int()
    default_middleplate_level = fields.Int()
    created_at = fields.DateTime(dump_only=True)
    modified_at = fields.DateTime(dump_only=True)
