# src/models/UserModel.py
from marshmallow import fields, Schema
import datetime
from . import db, bcrypt
from .PatientInfoModel import PatientInfoSchema
from .FitboxModel import FitboxSchema
from .DailyScheduleModel import DailyScheduleSchema
from .MedicalCheckModel import MedicalCheckSchema


class UserModel(db.Model):
    """
    User Model
    """

    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True)
    last_name = db.Column(db.String(32), nullable=False)
    first_name = db.Column(db.String(32), nullable=False)
    city = db.Column(db.String(32), nullable=False)
    address = db.Column(db.String(64), nullable=False)
    zip_code = db.Column(db.String(32), nullable=False)
    phone_number = db.Column(db.String(64), nullable=True)
    email = db.Column(db.String(128), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    supervisor_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=True)
    created_at = db.Column(db.DateTime)
    modified_at = db.Column(db.DateTime)
    patient_info = db.relationship('PatientInfoModel', backref='patient_infos', lazy=True)
    current_fitbox = db.relationship('FitboxModel', backref='fitboxes', lazy=True)
    daily_schedules = db.relationship('DailyScheduleModel', backref='daily_schedules', lazy=True)
    checks = db.relationship('MedicalCheckModel', backref='medical_checks', lazy=True)

    # class constructor
    def __init__(self, data):
        """
    Class constructor
    """
        self.last_name = data.get('last_name')
        self.first_name = data.get('first_name')
        self.city = data.get('city')
        self.address = data.get('address')
        self.zip_code = data.get('zip_code')
        self.phone_number = data.get('phone_number')
        self.email = data.get('email')
        self.age = data.get('age')
        self.password = self.__generate_hash(data.get('password'))
        self.supervisor_id = data.get('supervisor_id')
        self.created_at = datetime.datetime.utcnow()
        self.modified_at = datetime.datetime.utcnow()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self, data):
        for key, item in data.items():
            if key == 'password':
                self.password = self.__generate_hash(item)
            setattr(self, key, item)
        self.modified_at = datetime.datetime.utcnow()
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def get_all_users():
        return UserModel.query.all()

    @staticmethod
    def get_one_user(user_id):
        return UserModel.query.get(user_id)

    @staticmethod
    def get_user_by_email(value):
        return UserModel.query.filter_by(email=value).first()

    def __generate_hash(self, password):
        return bcrypt.generate_password_hash(password, rounds=10).decode("utf-8")

    def check_hash(self, password):
        return bcrypt.check_password_hash(self.password, password)

    def __repr(self):
        return '<user_id {}>'.format(self.user_id)


class UserSchema(Schema):
    user_id = fields.Int(dump_only=True)
    last_name = fields.Str(required=True)
    first_name = fields.Str(required=True)
    city = fields.Str(required=True)
    address = fields.Str(required=True)
    zip_code = fields.Str(required=True)
    phone_number = fields.Str()
    email = fields.Email(required=True)
    password = fields.Str(required=True, load_only=True)
    age = fields.Int(required=True)
    supervisor_id = fields.Int()
    created_at = fields.DateTime(dump_only=True)
    modified_at = fields.DateTime(dump_only=True)
    patient_info = fields.Nested(PatientInfoSchema, many=False)
    current_fibox = fields.Nested(FitboxSchema, many=False)
    daily_schedules = fields.Nested(DailyScheduleSchema, many=True)
    checks = fields.Nested(MedicalCheckSchema, many=True)
