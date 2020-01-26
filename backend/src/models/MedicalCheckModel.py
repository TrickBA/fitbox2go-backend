# src/models/MedicalCheckModel.py
from marshmallow import fields, Schema
import datetime
from . import db


class MedicalCheckModel(db.Model):
    """
    Medical Check Model
    """

    __tablename__ = 'medical_checks'

    check_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    body_weight_kg = db.Column(db.Float, nullable=True)
    ibm = db.Column(db.Float, nullable=True)
    valid_until_date_time = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime)
    modified_at = db.Column(db.DateTime)

    # class constructor
    def __init__(self, data):
        """
        Class constructor
        """
        self.user_id = data.get('user_id')
        self.body_weight_kg = data.get('body_weight_kg')
        self.ibm = data.get('ibm')
        self.created_at = datetime.datetime.utcnow()
        self.modified_at = datetime.datetime.utcnow()

    def save(self):
        db.session.add(self)
        current_check = MedicalCheckModel.get_active_check_by_user(self.user_id)
        if current_check is not None:
            current_check.valid_until_date_time = self.created_at
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
    def get_all_medical_checks():
        return MedicalCheckModel.query.all()

    @staticmethod
    def get_one_medical_check(check_id):
        return MedicalCheckModel.query.get(check_id)

    @staticmethod
    def get_checks_by_user(user_id):
        return MedicalCheckModel.query.filter_by(user_id=user_id).all()

    @staticmethod
    def get_active_check_by_user(user_id):
        return MedicalCheckModel.query.filter_by(user_id=user_id, valid_until_date_time=None).first()

    def __repr(self):
        return '<check_id {}>'.format(self.check_id)


class MedicalCheckSchema(Schema):
    """
    Medical Check Schema
    """
    check_id = fields.Int(dump_only=True)
    user_id = fields.Int(required=True)
    body_weight_kg = fields.Float()
    ibm = fields.Float()
    valid_until_date_time = fields.DateTime(allow_none=True)
    created_at = fields.DateTime(dump_only=True)
    modified_at = fields.DateTime(dump_only=True)
