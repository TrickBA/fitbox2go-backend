# /src/views/ExerciseTypeView.py
from flask import request, g, Blueprint, json, Response
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
    req_data['user_id'] = g.user.get('id')
    try:
        data = exercise_type_schema.load(req_data)
    except ValidationError:
        return custom_response({'error': 'Trying to load object with invalid data'}, 400)
    post = ExerciseTypeModel(data)
    post.save()
    data = exercise_type_schema.dump(post)
    return custom_response(data, 201)


@exercise_type_api.route('/', methods=['GET'])
def get_all():
    """
    Get All ExerciseTypes
    """
    posts = ExerciseTypeModel.get_all_ExerciseTypes()
    data = exercise_type_schema.dump(posts, many=True)
    return custom_response(data, 200)


@exercise_type_api.route('/<exercise_type_id>', methods=['GET'])
def get_one(exercise_type_id):
    """
    Get A ExerciseType
    """
    post = ExerciseTypeModel.get_one_exercise_type(exercise_type_id)
    if not post:
        return custom_response({'error': 'exercise_type not found'}, 404)
    data = exercise_type_schema.dump(post)
    return custom_response(data, 200)


@exercise_type_api.route('/<exercise_type_id>', methods=['PUT'])
@Auth.auth_required
def update(exercise_type_id):
    """
    Update A ExerciseType
    """
    req_data = request.get_json()
    post = ExerciseTypeModel.get_one_exercise_type(exercise_type_id)
    if not post:
        return custom_response({'error': 'exercise_type not found'}, 404)
    data = exercise_type_schema.dump(post)
    if data.get('user_id') != g.user.get('id'):
        return custom_response({'error': 'permission denied'}, 400)

    try:
        data = exercise_type_schema.load(req_data, partial=True)
    except ValidationError:
        return custom_response({'error': 'Trying to load object with invalid data'}, 400)
    post.update(data)

    data = exercise_type_schema.dump(post)
    return custom_response(data, 200)


@exercise_type_api.route('/<exercise_type_id>', methods=['DELETE'])
@Auth.auth_required
def delete(exercise_type_id):
    """
    Delete A ExerciseType
    """
    post = ExerciseTypeModel.get_one_ExerciseType(exercise_type_id)
    if not post:
        return custom_response({'error': 'exercise_type not found'}, 404)
    data = exercise_type_schema.dump(post)
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

