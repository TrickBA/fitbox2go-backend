# src/app.py

from flask import Flask, render_template
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

    app.config['SECRET'] = 'my secret key'
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.config['MQTT_BROKER_URL'] = 'localhost'
    app.config['MQTT_BROKER_PORT'] = 1883
    app.config['MQTT_CLIENT_ID'] = 'flask_mqtt'
    app.config['MQTT_USERNAME'] = ''
    app.config['MQTT_PASSWORD'] = ''
    app.config['MQTT_KEEPALIVE'] = 5
    app.config['MQTT_TLS_ENABLED'] = False
    app.config['MQTT_LAST_WILL_TOPIC'] = 'home/lastwill'
    app.config['MQTT_LAST_WILL_MESSAGE'] = 'bye'
    app.config['MQTT_LAST_WILL_QOS'] = 2

    # Parameters for SSL enabled
    # app.config['MQTT_BROKER_PORT'] = 8883
    # app.config['MQTT_TLS_ENABLED'] = True
    # app.config['MQTT_TLS_INSECURE'] = True
    # app.config['MQTT_TLS_CA_CERTS'] = 'ca.crt'

    @app.route('/', methods=['GET'])
    def index():
        return render_template('index.html')

    return app
