# src/app.py

from flask import Flask

from .config import app_config
from .models import db, bcrypt

# import user_api blueprint
from .views.UserView import user_api as user_blueprint
from .views.TrainingView import training_api as training_blueprint
from .views.DailyScheduleView import daily_schedule_api as daily_schedule_blueprint


def create_app(env_name):
    app = Flask(__name__)

    app.config.from_object(app_config[env_name])

    bcrypt.init_app(app)
    db.init_app(app)

    app.register_blueprint(user_blueprint, url_prefix='/api/v1/users')
    app.register_blueprint(training_blueprint, url_prefix='/api/v1/trainings')
    app.register_blueprint(daily_schedule_blueprint, url_prefix='/api/v1/daily_schedules')

    @app.route('/', methods=['GET'])
    def index():
        """
        example endpoint
        """
        return 'Welcome to Fitbox2Go API!'

    return app
