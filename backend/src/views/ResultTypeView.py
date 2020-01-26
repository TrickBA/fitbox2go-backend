# /src/views/ResultTypeView.py
from flask import request, Blueprint, json, Response
from marshmallow import ValidationError

from ..shared.Authentication import Auth
from ..models.ResultTypeModel import ResultTypeModel, ResultTypeSchema

result_type_api = Blueprint('result_type_api', __name__)
result_type_schema = ResultTypeSchema()


@result_type_api.route('/', methods=['POST'])
@Auth.auth_required
def create():
    """
    Create ResultType Function
    """
    req_data = request.get_json()
    try:
        data = result_type_schema.load(req_data)
    except ValidationError:
        return custom_response({'error': 'Trying to load object with invalid data'}, 400)
    result_type = ResultTypeModel(data)
    result_type.save()
    data = result_type_schema.dump(result_type)
    return custom_response(data, 201)


@result_type_api.route('/', methods=['GET'])
def get_all():
    """
    Get All ResultTypes
    """
    result_types = ResultTypeModel.get_all_result_types()
    data = result_type_schema.dump(result_types, many=True)
    return custom_response(data, 200)


@result_type_api.route('/<result_type_id>', methods=['GET'])
def get_one(result_type_id):
    """
    Get A ResultType
    """
    result_type = ResultTypeModel.get_one_result_type(result_type_id)
    if not result_type:
        return custom_response({'error': 'result_type not found'}, 404)
    data = result_type_schema.dump(result_type)
    return custom_response(data, 200)


@result_type_api.route('/<result_type_id>', methods=['PUT'])
@Auth.auth_required
def update(result_type_id):
    """
    Update A ResultType
    """
    req_data = request.get_json()
    result_type = ResultTypeModel.get_one_result_type(result_type_id)
    if not result_type:
        return custom_response({'error': 'result_type not found'}, 404)

    try:
        data = result_type_schema.load(req_data, partial=True)
    except ValidationError:
        return custom_response({'error': 'Trying to load object with invalid data'}, 400)
    result_type.update(data)

    data = result_type_schema.dump(result_type)
    return custom_response(data, 200)


@result_type_api.route('/<result_type_id>', methods=['DELETE'])
@Auth.auth_required
def delete(result_type_id):
    """
    Delete A ResultType
    """
    result_type = ResultTypeModel.get_one_result_type(result_type_id)
    if not result_type:
        return custom_response({'error': 'result_type not found'}, 404)

    result_type.delete()
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
