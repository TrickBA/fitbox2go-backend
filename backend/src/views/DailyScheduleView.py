# /src/views/DailyScheduleView.py
from flask import request, g, Blueprint, json, Response
from marshmallow import ValidationError

from ..shared.Authentication import Auth
from ..models.DailyScheduleModel import DailyScheduleModel, DailyScheduleSchema

daily_schedule_api = Blueprint('daily_schedule_api', __name__)
daily_schedule_schema = DailyScheduleSchema()


@daily_schedule_api.route('/', methods=['POST'])
@Auth.auth_required
def create():
    """
    Create daily_schedule Function
    """
    req_data = request.get_json()
    req_data['user_id'] = g.user.get('id')
    try:
        data = daily_schedule_schema.load(req_data)
    except ValidationError as err:
        return custom_response({'error': 'Trying to load object with invalid data'}, 400)
    post = DailyScheduleModel(data)
    post.save()
    data = daily_schedule_schema.dump(post)
    return custom_response(data, 201)


@daily_schedule_api.route('/', methods=['GET'])
def get_all():
    """
    Get All daily_schedules
    """
    posts = DailyScheduleModel.get_all_daily_schedules()
    data = daily_schedule_schema.dump(posts, many=True)
    return custom_response(data, 200)


@daily_schedule_api.route('/<daily_schedule_id>', methods=['GET'])
def get_one(daily_schedule_id):
    """
    Get A daily_schedule
    """
    post = DailyScheduleModel.get_one_daily_schedule(daily_schedule_id)
    if not post:
        return custom_response({'error': 'daily_schedule not found'}, 404)
    data = daily_schedule_schema.dump(post)
    return custom_response(data, 200)


@daily_schedule_api.route('/<daily_schedule_id>', methods=['PUT'])
@Auth.auth_required
def update(daily_schedule_id):
    """
    Update A daily_schedule
    """
    req_data = request.get_json()
    post = DailyScheduleModel.get_one_daily_schedule(daily_schedule_id)
    if not post:
        return custom_response({'error': 'daily_schedule not found'}, 404)
    data = daily_schedule_schema.dump(post)
    if data.get('user_id') != g.user.get('id'):
        return custom_response({'error': 'permission denied'}, 400)

    try:
        data = daily_schedule_schema.load(req_data, partial=True)
    except ValidationError:
        return custom_response({'error': 'Trying to load object with invalid data'}, 400)
    post.update(data)

    data = daily_schedule_schema.dump(post)
    return custom_response(data, 200)


@daily_schedule_api.route('/<daily_schedule_id>', methods=['DELETE'])
@Auth.auth_required
def delete(daily_schedule_id):
    """
    Delete A daily_schedule
    """
    post = DailyScheduleModel.get_one_daily_schedule(daily_schedule_id)
    if not post:
        return custom_response({'error': 'daily_schedule not found'}, 404)
    data = daily_schedule_schema.dump(post)
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
