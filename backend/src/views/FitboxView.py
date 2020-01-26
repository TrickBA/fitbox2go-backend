# /src/views/FitboxView.py
from flask import request, Blueprint, json, Response
from marshmallow import ValidationError

from ..shared.Authentication import Auth
from ..models.FitboxModel import FitboxModel, FitboxSchema

fitbox_api = Blueprint('fitbox_api', __name__)
fitbox_schema = FitboxSchema()


@fitbox_api.route('/', methods=['POST'])
@Auth.auth_required
def create():
    """
    Create Fitbox Function
    """
    req_data = request.get_json()
    try:
        data = fitbox_schema.load(req_data)
    except ValidationError:
        return custom_response({'error': 'Trying to load object with invalid data'}, 400)
    fitbox = FitboxModel(data)
    fitbox.save()
    data = fitbox_schema.dump(fitbox)
    return custom_response(data, 201)


@fitbox_api.route('/', methods=['GET'])
def get_all():
    """
    Get All Fitboxs
    """
    fitboxs = FitboxModel.get_all_fitboxs()
    data = fitbox_schema.dump(fitboxs, many=True)
    return custom_response(data, 200)


@fitbox_api.route('/<fitbox_id>', methods=['GET'])
def get_one(fitbox_id):
    """
    Get A Fitbox
    """
    fitbox = FitboxModel.get_one_fitbox(fitbox_id)
    if not fitbox:
        return custom_response({'error': 'fitbox not found'}, 404)
    data = fitbox_schema.dump(fitbox)
    return custom_response(data, 200)


@fitbox_api.route('/<fitbox_id>', methods=['PUT'])
@Auth.auth_required
def update(fitbox_id):
    """
    Update A Fitbox
    """
    req_data = request.get_json()
    fitbox = FitboxModel.get_one_fitbox(fitbox_id)
    if not fitbox:
        return custom_response({'error': 'fitbox not found'}, 404)

    try:
        data = fitbox_schema.load(req_data, partial=True)
    except ValidationError:
        return custom_response({'error': 'Trying to load object with invalid data'}, 400)
    fitbox.update(data)

    data = fitbox_schema.dump(fitbox)
    return custom_response(data, 200)


@fitbox_api.route('/<fitbox_id>', methods=['DELETE'])
@Auth.auth_required
def delete(fitbox_id):
    """
    Delete A Fitbox
    """
    fitbox = FitboxModel.get_one_fitbox(fitbox_id)
    if not fitbox:
        return custom_response({'error': 'fitbox not found'}, 404)

    fitbox.delete()
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

