# /src/views/ExerciseTypeView.py
from flask import request, Blueprint, json, Response
from marshmallow import ValidationError

from ..shared.Authentication import Auth
from ..models.ExerciseTypeModel import ExerciseTypeModel, ExerciseTypeSchema

exercise_type_api = Blueprint('exercise_type_api', __name__)
exercise_type_schema = ExerciseTypeSchema()


@exercise_type_api.route('/', methods=['POST'])
@Auth.auth_required
def create():
    """
    Create ExerciseType Function
    """
    req_data = request.get_json()
    try:
        data = exercise_type_schema.load(req_data)
    except ValidationError:
        return custom_response({'error': 'Trying to load object with invalid data'}, 400)
    exercise_type = ExerciseTypeModel(data)
    exercise_type.save()
    data = exercise_type_schema.dump(exercise_type)
    return custom_response(data, 201)


@exercise_type_api.route('/', methods=['GET'])
def get_all():
    """
    Get All ExerciseTypes
    """
    exercise_types = ExerciseTypeModel.get_all_exercise_types()
    data = exercise_type_schema.dump(exercise_types, many=True)
    return custom_response(data, 200)


@exercise_type_api.route('/<exercise_type_id>', methods=['GET'])
def get_one(exercise_type_id):
    """
    Get A ExerciseType
    """
    exercise_type = ExerciseTypeModel.get_one_exercise_type(exercise_type_id)
    if not exercise_type:
        return custom_response({'error': 'exercise_type not found'}, 404)
    data = exercise_type_schema.dump(exercise_type)
    return custom_response(data, 200)


@exercise_type_api.route('/<exercise_type_id>', methods=['PUT'])
@Auth.auth_required
def update(exercise_type_id):
    """
    Update A ExerciseType
    """
    req_data = request.get_json()
    exercise_type = ExerciseTypeModel.get_one_exercise_type(exercise_type_id)
    if not exercise_type:
        return custom_response({'error': 'exercise_type not found'}, 404)

    try:
        data = exercise_type_schema.load(req_data, partial=True)
    except ValidationError:
        return custom_response({'error': 'Trying to load object with invalid data'}, 400)
    exercise_type.update(data)

    data = exercise_type_schema.dump(exercise_type)
    return custom_response(data, 200)


@exercise_type_api.route('/<exercise_type_id>', methods=['DELETE'])
@Auth.auth_required
def delete(exercise_type_id):
    """
    Delete A ExerciseType
    """
    exercise_type = ExerciseTypeModel.get_one_exercise_type(exercise_type_id)
    if not exercise_type:
        return custom_response({'error': 'exercise_type not found'}, 404)

    exercise_type.delete()
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

