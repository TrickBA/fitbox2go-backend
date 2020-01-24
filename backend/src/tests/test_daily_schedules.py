import unittest
import json

from datetime import datetime

from src.models import UserModel, UserSchema
from ..app import create_app, db


class DailyScheduleTest(unittest.TestCase):
    """
    DailySchedules Test Case
    """

    def setUp(self):
        """
        Test Setup
        """
        self.app = create_app("testing")
        self.client = self.app.test_client
        user_schema = UserSchema()
        user_data = {
            'last_name': 'olawale',
            'first_name': 'shindeiru',
            'email': 'olawale@mail.com',
            'password': 'passw0rd!',
            'address': 'Missing data for required field.',
            'city': 'Eindhoven',
            'zip_code': '3123ND',
            'age': '21',
            'phone_number': '0631566246',
        }
        user1 = {
            'password': 'passw0rd!',
            'email': 'olawale@mail.com',
        }
        data = user_schema.load(user_data)
        user = UserModel(data)
        self.daily_schedule = {'schedule_date': '22-01-2020'}

        with self.app.app_context():
            # create all tables
            db.create_all()
            user.save()
            res = self.client().post('/api/v1/users/login', headers={'Content-Type': 'application/json'},
                                     data=json.dumps(user1))
            json_data = json.loads(res.data)
            self.token = json_data.get('jwt_token')

    def test_daily_schedule_creation(self):
        """ test daily_schedule creation with valid credentials """
        res = self.client().post('/api/v1/daily_schedules/',
                                 headers={'Content-Type': 'application/json', 'api-token': self.token},
                                 data=json.dumps(self.daily_schedule))
        self.assertEqual(res.status_code, 201)

    def test_daily_schedule_creation_with_empty_request(self):
        """ test daily_schedule creation with empty request """
        daily_schedule1 = {}
        res = self.client().post('/api/v1/daily_schedules/',
                                 headers={'Content-Type': 'application/json', 'api-token': self.token},
                                 data=json.dumps(daily_schedule1))
        json_data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertTrue(json_data.get('error'))

    def test_daily_schedule_get_me(self):
        """ Test DailySchedules Get Me """
        res = self.client().post('/api/v1/daily_schedules/',
                                 headers={'Content-Type': 'application/json', 'api-token': self.token},
                                 data=json.dumps(self.daily_schedule))
        self.assertEqual(res.status_code, 201)

        res = self.client().get('/api/v1/daily_schedules/me',
                                headers={'Content-Type': 'application/json', 'api-token': self.token})
        json_data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(json_data.get('schedule_date'), '22-01-2020')
        self.assertEqual(json_data.get('user_id'), '1')

    """
    def test_daily_schedule_update_me(self):
        Test DailySchedules Update Me
        daily_schedule1 = {
            'last_name': 'new name'
        }
        res = self.client().post('/api/v1/daily_schedules/', headers={'Content-Type': 'application/json'},
                                 data=json.dumps(self.daily_schedule))
        self.assertEqual(res.status_code, 201)
        api_token = json.loads(res.data).get('jwt_token')
        res = self.client().put('/api/v1/daily_schedules/me',
                                headers={'Content-Type': 'application/json', 'api-token': api_token},
                                data=json.dumps(daily_schedule1))
        json_data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(json_data.get('last_name'), 'new name')

    def test_delete_daily_schedule(self):
        Test DailySchedules Delete
        res = self.client().post('/api/v1/daily_schedules/', headers={'Content-Type': 'application/json'},
                                 data=json.dumps(self.daily_schedule))
        self.assertEqual(res.status_code, 201)
        api_token = json.loads(res.data).get('jwt_token')
        res = self.client().delete('/api/v1/daily_schedules/me',
                                   headers={'Content-Type': 'application/json', 'api-token': api_token})
        self.assertEqual(res.status_code, 204)
    """

    def tearDown(self):
        """
        Tear Down
        """
        with self.app.app_context():
            db.session.remove()
            db.drop_all()


if __name__ == "__main__":
    unittest.main()
