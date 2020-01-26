# src/models/PatientInfoModel.py
from marshmallow import fields, Schema
import datetime
from . import db


class PatientInfoModel(db.Model):
    """
    Patient Info Model
    """

    __tablename__ = 'patient_infos'

    patient_info_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), unique=True, nullable=False)
    limitations = db.Column(db.String(128), nullable=True)
    body_length_cm = db.Column(db.Float, nullable=True)
    upper_leg_length_cm = db.Column(db.Float, nullable=True)
    lower_leg_length_cm = db.Column(db.Float, nullable=True)
    shoe_size = db.Column(db.Float, nullable=True)
    created_at = db.Column(db.DateTime)
    modified_at = db.Column(db.DateTime)

    # class constructor
    def __init__(self, data):
        """
        Class constructor
        """
        self.user_id = data.get('user_id')
        self.limitations = data.get('limitations')
        self.body_length_cm = data.get('body_length_cm')
        self.upper_leg_length_cm = data.get('upper_leg_length_cm')
        self.lower_leg_length_cm = data.get('lower_leg_length_cm')
        self.shoe_size = data.get('shoe_size')
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
    def get_all_patient_infos():
        return PatientInfoModel.query.all()

    @staticmethod
    def get_one_patient_info(patient_info_id):
        return PatientInfoModel.query.get(patient_info_id)

    @staticmethod
    def get_user_patient_info(user_id):
        return PatientInfoModel.query.filter_by(user_id=user_id).first()

    def __repr(self):
        return '<patient_info_id {}>'.format(self.patient_info_id)


class PatientInfoSchema(Schema):
    """
    Patient Info Schema
    """
    patient_info_id = fields.Int(dump_only=True)
    user_id = fields.Int(required=True)
    limitations = fields.Str()
    body_length_cm = fields.Float()
    upper_leg_length_cm = fields.Float()
    lower_leg_length_cm = fields.Float()
    shoe_size = fields.Float()
    created_at = fields.DateTime(dump_only=True)
    modified_at = fields.DateTime(dump_only=True)
