# src/app.py

from flask import Flask

from .config import app_config
from .models import db, bcrypt

# import user_api blueprint
from .views.UserView import user_api as user_blueprint
from .views.TrainingView import training_api as training_blueprint
from .views.DailyScheduleView import daily_schedule_api as daily_schedule_blueprint
from .views.ExerciseTypeView import exercise_type_api as exercise_type_blueprint
from .views.ExerciseView import exercise_api as exercise_blueprint
from .views.FitboxView import fitbox_api as fitbox_blueprint
from .views.ResultTypeView import result_type_api as result_type_blueprint
from .views.ResultView import result_api as result_blueprint
from .views.MedicalCheckView import check_api as check_blueprint
from .views.PatientInfoView import patient_info_api as patient_info_blueprint


def create_app(env_name):
    app = Flask(__name__)

    app.config.from_object(app_config[env_name])

    bcrypt.init_app(app)
    db.init_app(app)

    app.register_blueprint(user_blueprint, url_prefix='/api/v1/users')
    app.register_blueprint(training_blueprint, url_prefix='/api/v1/trainings')
    app.register_blueprint(daily_schedule_blueprint, url_prefix='/api/v1/daily_schedules')
    app.register_blueprint(exercise_type_blueprint, url_prefix='/api/v1/exercise_types')
    app.register_blueprint(exercise_blueprint, url_prefix='/api/v1/exercises')
    app.register_blueprint(fitbox_blueprint, url_prefix='/api/v1/fitboxes')
    app.register_blueprint(result_type_blueprint, url_prefix='/api/v1/result_types')
    app.register_blueprint(result_blueprint, url_prefix='/api/v1/results')
    app.register_blueprint(check_blueprint, url_prefix='/api/v1/checks')
    app.register_blueprint(patient_info_blueprint, url_prefix='/api/v1/patient_infos')

    @app.route('/', methods=['GET'])
    def index():
        """
        example endpoint
        """
        return 'Welcome to Fitbox2Go API!'

    return app
