# src/models/ResultModel.py
from marshmallow import fields, Schema
import datetime
from . import db


class ResultModel(db.Model):
    """
    Result Model
    """

    __tablename__ = 'results'

    result_id = db.Column(db.Integer, primary_key=True)
    result_type_id = db.Column(db.Integer, db.ForeignKey("result_types.result_type_id"), nullable=False)
    training_id = db.Column(db.Integer, db.ForeignKey("trainings.training_id"), nullable=False)
    actual_value = db.Column(db.Numeric, nullable=False)
    expected_value = db.Column(db.Numeric, nullable=True)
    upper_control_limit = db.Column(db.Numeric, nullable=True)
    lower_control_limit = db.Column(db.Numeric, nullable=True)
    created_at = db.Column(db.DateTime)
    modified_at = db.Column(db.DateTime)

    # class constructor
    def __init__(self, data):
        """
        Class constructor
        """
        self.result_type_id = data.get('result_type_id')
        self.training_id = data.get('training_id')
        self.unit_of_measure = data.get('unit_of_measure')
        self.actual_value = data.get('actual_value')
        self.upper_control_limit = data.get('upper_control_limit')
        self.lower_control_limit = data.get('lower_control_limit')
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
    def get_all_results():
        return ResultModel.query.all()

    @staticmethod
    def get_one_result(result_id):
        return ResultModel.query.get(result_id)

    def __repr(self):
        return '<result_id {}>'.format(self.result_id)


class ResultSchema(Schema):
    """
    ResultSchema
    """
    result_id = fields.Int(dump_only=True)
    result_type_id = fields.Int(required=True)
    training_id = fields.Int(required=True)
    actual_value = fields.Decimal(required=True)
    expected_value = fields.Decimal()
    upper_control_limit = fields.Decimal()
    lower_control_limit = fields.Decimal()
    created_at = fields.DateTime(dump_only=True)
    modified_at = fields.DateTime(dump_only=True)
