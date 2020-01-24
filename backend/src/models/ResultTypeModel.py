# src/models/ResultTypeModel.py
from marshmallow import fields, Schema
import datetime
from . import db


class ResultTypeModel(db.Model):
    """
    Result Type Model
    """

    __tablename__ = 'result_types'

    result_type_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    unit_of_measure = db.Column(db.String(64), nullable=False)
    description = db.Column(db.String(128), nullable=True)
    created_at = db.Column(db.DateTime)
    modified_at = db.Column(db.DateTime)

    # class constructor
    def __init__(self, data):
        """
        Class constructor
        """
        self.name = data.get('name')
        self.unit_of_measure = data.get('unit_of_measure')
        self.description = data.get('description')
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
    def get_all_result_types():
        return ResultTypeModel.query.all()

    @staticmethod
    def get_one_result_type(result_type_id):
        return ResultTypeModel.query.get(result_type_id)

    def __repr(self):
        return '<result_type_id {}>'.format(self.result_type_id)


class ResultTypeSchema(Schema):
    """
    ResultTypeSchema
    """
    result_type_id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    unit_of_measure = fields.Str(required=True)
    description = fields.Str()
    created_at = fields.DateTime()
    modified_at = fields.DateTime(dump_only=True)
