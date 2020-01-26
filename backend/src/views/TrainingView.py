# /src/views/TrainingView.py
from flask import request, Blueprint, json, Response
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
    try:
        data = training_schema.load(req_data)
    except ValidationError:
        return custom_response({'error': 'Trying to load object with invalid data'}, 400)
    training = TrainingModel(data)
    training.save()
    data = training_schema.dump(training)
    return custom_response(data, 201)


@training_api.route('/', methods=['GET'])
def get_all():
    """
    Get All Trainings
    """
    trainings = TrainingModel.get_all_trainings()
    data = training_schema.dump(trainings, many=True)
    return custom_response(data, 200)


@training_api.route('/<training_id>', methods=['GET'])
def get_one(training_id):
    """
    Get A Training
    """
    training = TrainingModel.get_one_training(training_id)
    if not training:
        return custom_response({'error': 'training not found'}, 404)
    data = training_schema.dump(training)
    return custom_response(data, 200)


@training_api.route('/exercise/<exercise_id>', methods=['GET'])
def get_all_by_exercise(exercise_id):
    """
    Get All Trainings By Exercise
    """
    trainings = TrainingModel.get_trainings_by_exercise(exercise_id)
    if not trainings:
        return custom_response({'error': 'trainings not found'}, 404)
    data = training_schema.dump(trainings, many=True)
    return custom_response(data, 200)


@training_api.route('/<training_id>', methods=['PUT'])
@Auth.auth_required
def update(training_id):
    """
    Update A Training
    """
    req_data = request.get_json()
    training = TrainingModel.get_one_training(training_id)
    if not training:
        return custom_response({'error': 'training not found'}, 404)

    try:
        data = training_schema.load(req_data, partial=True)
    except ValidationError:
        return custom_response({'error': 'Trying to load object with invalid data'}, 400)
    training.update(data)

    data = training_schema.dump(training)
    return custom_response(data, 200)


@training_api.route('/<training_id>', methods=['DELETE'])
@Auth.auth_required
def delete(training_id):
    """
    Delete A Training
    """
    training = TrainingModel.get_one_training(training_id)
    if not training:
        return custom_response({'error': 'training not found'}, 404)

    training.delete()
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

