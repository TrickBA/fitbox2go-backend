# /src/views/PatientInfoView.py
from flask import request, Blueprint, json, Response
from marshmallow import ValidationError

from ..shared.Authentication import Auth
from ..models.PatientInfoModel import PatientInfoModel, PatientInfoSchema

patient_info_api = Blueprint('patient_info_api', __name__)
patient_info_schema = PatientInfoSchema()


@patient_info_api.route('/', methods=['POST'])
@Auth.auth_required
def create():
    """
    Create PatientInfo Function
    """
    req_data = request.get_json()
    try:
        data = patient_info_schema.load(req_data)
    except ValidationError:
        return custom_response({'error': 'Trying to load object with invalid data'}, 400)
    patient_info = PatientInfoModel(data)
    patient_info.save()
    data = patient_info_schema.dump(patient_info)
    return custom_response(data, 201)


@patient_info_api.route('/', methods=['GET'])
def get_all():
    """
    Get All PatientInfos
    """
    patient_infos = PatientInfoModel.get_all_patient_infos()
    data = patient_info_schema.dump(patient_infos, many=True)
    return custom_response(data, 200)


@patient_info_api.route('/<patient_info_id>', methods=['GET'])
def get_one(patient_info_id):
    """
    Get A PatientInfo
    """
    patient_info = PatientInfoModel.get_one_patient_info(patient_info_id)
    if not patient_info:
        return custom_response({'error': 'patient_info not found'}, 404)
    data = patient_info_schema.dump(patient_info)
    return custom_response(data, 200)


@patient_info_api.route('/user/<user_id>', methods=['GET'])
def get_info_user(user_id):
    """
    Get PatientInfo For User
    """
    patient_info = PatientInfoModel.get_user_patient_info(user_id)
    if not patient_info:
        return custom_response({'error': 'patient_info not found'}, 404)
    data = patient_info_schema.dump(patient_info)
    return custom_response(data, 200)


@patient_info_api.route('/<patient_info_id>', methods=['PUT'])
@Auth.auth_required
def update(patient_info_id):
    """
    Update A PatientInfo
    """
    req_data = request.get_json()
    patient_info = PatientInfoModel.get_one_patient_info(patient_info_id)
    if not patient_info:
        return custom_response({'error': 'patient_info not found'}, 404)

    try:
        data = patient_info_schema.load(req_data, partial=True)
    except ValidationError:
        return custom_response({'error': 'Trying to load object with invalid data'}, 400)
    patient_info.update(data)

    data = patient_info_schema.dump(patient_info)
    return custom_response(data, 200)


@patient_info_api.route('/<patient_info_id>', methods=['DELETE'])
@Auth.auth_required
def delete(patient_info_id):
    """
    Delete A PatientInfo
    """
    patient_info = PatientInfoModel.get_one_patient_info(patient_info_id)
    if not patient_info:
        return custom_response({'error': 'patient_info not found'}, 404)

    patient_info.delete()
    return custom_response({'message': 'deleted'}, 204)


def custom_response(res, status_code):
    """
    Custom Response Function
    """
    return Response(
        mimetype="application/json",
        response=json.dumps(res),
        status=status_code
    )
