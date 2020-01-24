# src/models/DailyScheduleModel.py
from marshmallow import fields, Schema
import datetime
from . import db
from .ExerciseModel import ExerciseSchema


class DailyScheduleModel(db.Model):
    """
    DailySchedule Model
    """

    __tablename__ = 'daily_schedules'

    schedule_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    is_completed = db.Column(db.Boolean, nullable=False)
    schedule_date = db.Column(db.Date, nullable=False)
    created_at = db.Column(db.DateTime)
    modified_at = db.Column(db.DateTime)
    exercises = db.relationship('ExerciseModel', backref='exercises', lazy=True)

    # class constructor
    def __init__(self, data):
        """
        Class constructor
        """
        self.user_id = data.get('user_id')
        self.is_completed = False
        self.schedule_date = datetime.datetime.strptime(data.get('schedule_date'), "%d-%m-%Y")
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
    def get_all_daily_schedules():
        return DailyScheduleModel.query.all()

    @staticmethod
    def get_one_daily_schedule(schedule_id):
        return DailyScheduleModel.query.get(schedule_id)

    @staticmethod
    def get_daily_schedules_by_user(user_id):
        return DailyScheduleModel.query.filter_by(user_id=user_id).all()

    def __repr(self):
        return '<schedule_id {}>'.format(self.schedule_id)


class DailyScheduleSchema(Schema):
    """
    DailySchedule Schema
    """
    schedule_id = fields.Int(dump_only=True)
    user_id = fields.Int()
    is_completed = fields.Bool()
    schedule_date = fields.Str(required=True)
    created_at = fields.DateTime(dump_only=True)
    modified_at = fields.DateTime(dump_only=True)
    exercises = fields.Nested(ExerciseSchema, many=True)
