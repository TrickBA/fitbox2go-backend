# /src/views/DailyScheduleView.py
from flask import request, g, Blueprint, json, Response
from marshmallow import ValidationError

from ..shared.Authentication import Auth
from ..models.DailyScheduleModel import DailyScheduleModel, DailyScheduleSchema
from ..models.UserModel import UserModel, UserSchema

daily_schedule_api = Blueprint('daily_schedule_api', __name__)
daily_schedule_schema = DailyScheduleSchema()
user_schema = UserSchema()


@daily_schedule_api.route('/', methods=['POST'])
@Auth.auth_required
def create():
    """
    Create daily_schedule Function
    """
    req_data = request.get_json()
    opt_param = request.args.get("user_id")

    """
    #Additional check for creating schedule only if the user is a supervisor of the specified user_id
    #or is adding schedule for himself.
    if opt_param is not None:
        user = UserModel.get_one_user(opt_param)
        if not user:
            return custom_response({'error': 'Patient not found'}, 404)
        else:
            u = user_schema.dump(user, many=False)
            if u.get('supervisor_id') != g.user.get('id'):
                return custom_response({'error': 'permission denied'}, 400)
    else:
        req_data['user_id'] = g.user.get('id')
    """
    if not opt_param:
        req_data['user_id'] = g.user.get('id')
    try:
        data = daily_schedule_schema.load(req_data)
    except ValidationError as err:
        return custom_response({'error': 'Trying to load object with invalid data'}, 400)
    schedule = DailyScheduleModel(data)
    schedule.save()
    data = daily_schedule_schema.dump(schedule)
    return custom_response(data, 201)


@daily_schedule_api.route('/', methods=['GET'])
def get_all():
    """
    Get All daily_schedules
    """
    schedules = DailyScheduleModel.get_all_daily_schedules()
    data = daily_schedule_schema.dump(schedules, many=True)
    return custom_response(data, 200)


@daily_schedule_api.route('/<daily_schedule_id>', methods=['GET'])
def get_one(daily_schedule_id):
    """
    Get A daily_schedule
    """
    schedule = DailyScheduleModel.get_one_daily_schedule(daily_schedule_id)
    if not schedule:
        return custom_response({'error': 'daily_schedule not found'}, 404)
    data = daily_schedule_schema.dump(schedule)
    return custom_response(data, 200)


@daily_schedule_api.route('/<daily_schedule_id>', methods=['PUT'])
@Auth.auth_required
def update(daily_schedule_id):
    """
    Update A daily_schedule
    """
    req_data = request.get_json()
    schedule = DailyScheduleModel.get_one_daily_schedule(daily_schedule_id)
    if not schedule:
        return custom_response({'error': 'daily_schedule not found'}, 404)
    data = daily_schedule_schema.dump(schedule)
    if data.get('user_id') != g.user.get('id'):
        return custom_response({'error': 'permission denied'}, 400)

    try:
        data = daily_schedule_schema.load(req_data, partial=True)
    except ValidationError:
        return custom_response({'error': 'Trying to load object with invalid data'}, 400)
    schedule.update(data)

    data = daily_schedule_schema.dump(schedule)
    return custom_response(data, 200)


@daily_schedule_api.route('/<daily_schedule_id>', methods=['DELETE'])
@Auth.auth_required
def delete(daily_schedule_id):
    """
    Delete A daily_schedule
    """
    schedule = DailyScheduleModel.get_one_daily_schedule(daily_schedule_id)
    if not schedule:
        return custom_response({'error': 'daily_schedule not found'}, 404)
    data = daily_schedule_schema.dump(schedule)
    if data.get('user_id') != g.user.get('id'):
        return custom_response({'error': 'permission denied'}, 400)

    schedule.delete()
    return custom_response({'message': 'deleted'}, 204)


@daily_schedule_api.route('/my', methods=['GET'])
@Auth.auth_required
def get_my_schedules():
    """
    Get all my daily_schedule
    """
    schedules = DailyScheduleModel.get_daily_schedules_by_user(g.user.get('id'))
    user_schedules = daily_schedule_schema.dump(schedules, many=True)
    return custom_response(user_schedules, 200)


def custom_response(res, status_code):
    """
    Custom Response Function
    """
    return Response(
        mimetype="application/json",
        response=json.dumps(res),
        status=status_code
    )
