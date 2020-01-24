# /src/views/TrainingView.py
from flask import request, g, Blueprint, json, Response
from marshmallow import ValidationError

from ..shared.Authentication import Auth
from ..models.TrainingModel import TrainingModel, TrainingSchema

training_api = Blueprint('training_api', __name__)
training_schema = TrainingSchema()


@training_api.route('/', methods=['POST'])
@Auth.auth_required
def create():
    """
    Create Training Function
    """
    req_data = request.get_json()
    req_data['user_id'] = g.user.get('id')
    try:
        data = training_schema.load(req_data)
    except ValidationError:
        return custom_response({'error': 'Trying to load object with invalid data'}, 400)
    post = TrainingModel(data)
    post.save()
    data = training_schema.dump(post)
    return custom_response(data, 201)


@training_api.route('/', methods=['GET'])
def get_all():
    """
    Get All Trainings
    """
    posts = TrainingModel.get_all_Trainings()
    data = training_schema.dump(posts, many=True)
    return custom_response(data, 200)


@training_api.route('/<training_id>', methods=['GET'])
def get_one(training_id):
    """
    Get A Training
    """
    post = TrainingModel.get_one_training(training_id)
    if not post:
        return custom_response({'error': 'training not found'}, 404)
    data = training_schema.dump(post)
    return custom_response(data, 200)


@training_api.route('/<training_id>', methods=['PUT'])
@Auth.auth_required
def update(training_id):
    """
    Update A Training
    """
    req_data = request.get_json()
    post = TrainingModel.get_one_training(training_id)
    if not post:
        return custom_response({'error': 'training not found'}, 404)
    data = training_schema.dump(post)
    if data.get('user_id') != g.user.get('id'):
        return custom_response({'error': 'permission denied'}, 400)

    try:
        data = training_schema.load(req_data, partial=True)
    except ValidationError:
        return custom_response({'error': 'Trying to load object with invalid data'}, 400)
    post.update(data)

    data = training_schema.dump(post)
    return custom_response(data, 200)


@training_api.route('/<training_id>', methods=['DELETE'])
@Auth.auth_required
def delete(training_id):
    """
    Delete A Training
    """
    post = TrainingModel.get_one_Training(training_id)
    if not post:
        return custom_response({'error': 'training not found'}, 404)
    data = training_schema.dump(post)
    if data.get('user_id') != g.user.get('id'):
        return custom_response({'error': 'permission denied'}, 400)

    post.delete()
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

