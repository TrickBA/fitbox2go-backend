# /src/views/MedicalCheckView.py
from flask import request, Blueprint, json, Response
from marshmallow import ValidationError

from ..shared.Authentication import Auth
from ..models.MedicalCheckModel import MedicalCheckModel, MedicalCheckSchema

check_api = Blueprint('check_api', __name__)
check_schema = MedicalCheckSchema()


@check_api.route('/', methods=['POST'])
@Auth.auth_required
def create():
    """
    Create MedicalCheck Function
    """
    req_data = request.get_json()
    try:
        data = check_schema.load(req_data)
    except ValidationError:
        return custom_response({'error': 'Trying to load object with invalid data'}, 400)
    check = MedicalCheckModel(data)
    check.save()
    data = check_schema.dump(check)
    return custom_response(data, 201)


@check_api.route('/', methods=['GET'])
def get_all():
    """
    Get All MedicalChecks
    """
    checks = MedicalCheckModel.get_all_medical_checks()
    data = check_schema.dump(checks, many=True)
    return custom_response(data, 200)


@check_api.route('/<check_id>', methods=['GET'])
def get_one(check_id):
    """
    Get A MedicalCheck
    """
    check = MedicalCheckModel.get_one_medical_check(check_id)
    if not check:
        return custom_response({'error': 'check not found'}, 404)
    data = check_schema.dump(check)
    return custom_response(data, 200)


@check_api.route('/user/<user_id>', methods=['GET'])
def get_user_checks(user_id):
    """
    Get A MedicalCheck
    """
    check = MedicalCheckModel.get_checks_by_user(user_id)
    if not check:
        return custom_response({'error': 'user not found'}, 404)
    data = check_schema.dump(check, many=True)
    return custom_response(data, 200)


@check_api.route('/active/<user_id>', methods=['GET'])
def get_user_active_check(user_id):
    """
    Get A MedicalCheck
    """
    check = MedicalCheckModel.get_active_check_by_user(user_id)
    if not check:
        return custom_response({'error': 'user not found'}, 404)
    data = check_schema.dump(check, many=False)
    return custom_response(data, 200)


@check_api.route('/<check_id>', methods=['PUT'])
@Auth.auth_required
def update(check_id):
    """
    Update A MedicalCheck
    """
    req_data = request.get_json()
    check = MedicalCheckModel.get_one_medical_check(check_id)
    if not check:
        return custom_response({'error': 'check not found'}, 404)

    try:
        data = check_schema.load(req_data, partial=True)
    except ValidationError as err:
        return custom_response({'error': 'Trying to load object with invalid data'}, 400)
    check.update(data)

    data = check_schema.dump(check)
    return custom_response(data, 200)


@check_api.route('/<check_id>', methods=['DELETE'])
@Auth.auth_required
def delete(check_id):
    """
    Delete A MedicalCheck
    """
    check = MedicalCheckModel.get_one_medical_check(check_id)
    if not check:
        return custom_response({'error': 'check not found'}, 404)

    check.delete()
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
