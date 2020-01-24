# src/models/FitboxModel.py
from marshmallow import fields, Schema
import datetime
from . import db


class FitboxModel(db.Model):
    """
    Fitbox Model
    """

    __tablename__ = 'fitboxes'

    serial_number = db.Column(db.String(128), primary_key=True)
    qr_code = db.Column(db.String(128), unique=True, nullable=False)
    model = db.Column(db.String(128), nullable=True)
    latitude = db.Column(db.Numeric, nullable=True)
    longitude = db.Column(db.Numeric, nullable=True)
    leftarmplate_level = db.Column(db.Integer)
    rightarmplate_level = db.Column(db.Integer)
    middleplate_level = db.Column(db.Integer)
    current_user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=True)
    created_at = db.Column(db.DateTime)
    modified_at = db.Column(db.DateTime)

    # class constructor
    def __init__(self, data):
        """
        Class constructor
        """
        self.serial_number = data.get('serial_number')
        self.qr_code = data.get('qr_code')
        self.model = data.get('model')
        self.latitude = data.get('latitude')
        self.longitude = data.get('longitude')
        self.leftarmplate_level = data.get('leftarmplate_level')
        self.rightarmplate_level = data.get('rightarmplate_level')
        self.middleplate_level = data.get('middleplate_level')
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
    def get_all_fitboxes():
        return FitboxModel.query.all()

    @staticmethod
    def get_one_fitbox(serial_number):
        return FitboxModel.query.get(serial_number)

    @staticmethod
    def get_fitbox_by_user(user_id):
        return FitboxModel.query.filter_by(current_user_id=user_id).first()

    def __repr(self):
        return '<serial_number {}>'.format(self.serial_number)


class FitboxSchema(Schema):
    """
    Fitbox Schema
    """
    serial_number = fields.Str(required=True)
    qr_code = fields.Str(required=True)
    model = fields.Str()
    latitude = fields.Decimal()
    longitude = fields.Decimal()
    leftarmplate_level = fields.Int()
    rightarmplate_level = fields.Int()
    middleplate_level = fields.Int()
    current_user_id = fields.Int()
    created_at = fields.DateTime(dump_only=True)
    modified_at = fields.DateTime(dump_only=True)
