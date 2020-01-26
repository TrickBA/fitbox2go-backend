# /src/views/ResultView.py
from flask import request, Blueprint, json, Response
from marshmallow import ValidationError

from ..shared.Authentication import Auth
from ..models.ResultModel import ResultModel, ResultSchema

result_api = Blueprint('result_api', __name__)
result_schema = ResultSchema()


@result_api.route('/', methods=['POST'])
@Auth.auth_required
def create():
    """
    Create Result Function
    """
    req_data = request.get_json()
    try:
        data = result_schema.load(req_data)
    except ValidationError:
        return custom_response({'error': 'Trying to load object with invalid data'}, 400)
    result = ResultModel(data)
    result.save()
    data = result_schema.dump(result)
    return custom_response(data, 201)


@result_api.route('/', methods=['GET'])
def get_all():
    """
    Get All Results
    """
    results = ResultModel.get_all_results()
    data = result_schema.dump(results, many=True)
    return custom_response(data, 200)


@result_api.route('/<result_id>', methods=['GET'])
def get_one(result_id):
    """
    Get A Result
    """
    result = ResultModel.get_one_result(result_id)
    if not result:
        return custom_response({'error': 'result not found'}, 404)
    data = result_schema.dump(result)
    return custom_response(data, 200)


@result_api.route('/<result_id>', methods=['PUT'])
@Auth.auth_required
def update(result_id):
    """
    Update A Result
    """
    req_data = request.get_json()
    result = ResultModel.get_one_result(result_id)
    if not result:
        return custom_response({'error': 'result not found'}, 404)

    try:
        data = result_schema.load(req_data, partial=True)
    except ValidationError:
        return custom_response({'error': 'Trying to load object with invalid data'}, 400)
    result.update(data)

    data = result_schema.dump(result)
    return custom_response(data, 200)


@result_api.route('/<result_id>', methods=['DELETE'])
@Auth.auth_required
def delete(result_id):
    """
    Delete A Result
    """
    result = ResultModel.get_one_result(result_id)
    if not result:
        return custom_response({'error': 'result not found'}, 404)

    result.delete()
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
