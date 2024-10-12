from app.server import create_app, make_celery
from app.tasks import send_scheduled_emails

app = create_app()

celery = make_celery(app)

if __name__ == "__main__":
    celery.start()
