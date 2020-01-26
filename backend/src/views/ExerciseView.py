# /src/views/ExerciseView.py
from flask import request, Blueprint, json, Response
from marshmallow import ValidationError

from ..shared.Authentication import Auth
from ..models.ExerciseModel import ExerciseModel, ExerciseSchema
from ..models.ExerciseTypeModel import ExerciseTypeModel

exercise_api = Blueprint('exercise_api', __name__)
exercise_schema = ExerciseSchema()


@exercise_api.route('/', methods=['POST'])
@Auth.auth_required
def create():
    """
    Create Exercise Function
    """
    req_data = request.get_json()
    try:
        data = exercise_schema.load(req_data)
        ex_type_id = req_data.get('exercise_type_id')
        ex_type = ExerciseTypeModel.get_one_exercise_type(ex_type_id)
    except ValidationError:
        return custom_response({'error': 'Trying to load object with invalid data'}, 400)
    exercise = ExerciseModel(data, ex_type)
    exercise.save()
    data = exercise_schema.dump(exercise)
    return custom_response(data, 201)


@exercise_api.route('/', methods=['GET'])
def get_all():
    """
    Get All Exercises
    """
    exercises = ExerciseModel.get_all_exercises()
    data = exercise_schema.dump(exercises, many=True)
    return custom_response(data, 200)


@exercise_api.route('/<exercise_id>', methods=['GET'])
def get_one(exercise_id):
    """
    Get A Exercise
    """
    exercise = ExerciseModel.get_one_exercise(exercise_id)
    if not exercise:
        return custom_response({'error': 'exercise not found'}, 404)
    data = exercise_schema.dump(exercise)
    return custom_response(data, 200)


@exercise_api.route('/<exercise_id>', methods=['PUT'])
@Auth.auth_required
def update(exercise_id):
    """
    Update A Exercise
    """
    req_data = request.get_json()
    exercise = ExerciseModel.get_one_exercise(exercise_id)
    if not exercise:
        return custom_response({'error': 'exercise not found'}, 404)

    try:
        data = exercise_schema.load(req_data, partial=True)
    except ValidationError:
        return custom_response({'error': 'Trying to load object with invalid data'}, 400)
    exercise.update(data)

    data = exercise_schema.dump(exercise)
    return custom_response(data, 200)


@exercise_api.route('/<exercise_id>', methods=['DELETE'])
@Auth.auth_required
def delete(exercise_id):
    """
    Delete A Exercise
    """
    exercise = ExerciseModel.get_one_exercise(exercise_id)
    if not exercise:
        return custom_response({'error': 'exercise not found'}, 404)

    exercise.delete()
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

