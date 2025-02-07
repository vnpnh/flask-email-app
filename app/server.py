from datetime import timedelta
from http import HTTPStatus

from celery import Celery, Task
from flask import Flask
from flask_migrate import Migrate

from app.config import Config
from app.database import db
from app.errors import handle_404_error, handle_500_error
from app.models.email import Email
from app.models.event import Event
from app.models.recipient import Recipient
from app.models.user import User
from app.routes import api_v1


def create_app(config_app=Config) -> Flask:
    app = Flask(__name__)

    app.config.from_object(config_app)

    db.init_app(app)
    Migrate(app, db)

    app.register_blueprint(api_v1)

    app.register_error_handler(HTTPStatus.NOT_FOUND, handle_404_error)
    app.register_error_handler(HTTPStatus.INTERNAL_SERVER_ERROR, handle_500_error)

    return app

def make_celery(app):
    celery = Celery(
        app.import_name,
        backend=app.config['CELERY_RESULT_BACKEND'],
        broker=app.config['CELERY_BROKER_URL']
    )

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask

    celery.conf.beat_schedule = {
        'send-scheduled-emails-every-second': {
            'task': 'app.tasks.send_scheduled_emails',
            'schedule': timedelta(seconds=5),
        },
    }

    return celery
