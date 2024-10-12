from flask import Blueprint
from app.constants.methods import HTTPMethod
from app.controllers.event_controller import EventController
from app.controllers.email_controller import EmailController
from app.controllers.recipient_controller import RecipientController
from app.controllers.user_controller import UserController

api_v1 = Blueprint('api_v1', __name__, url_prefix='/api/v1')
email_controller = EmailController()
event_controller = EventController()
user_controller = UserController()
recipient_controller = RecipientController()


@api_v1.route('/save_emails/', methods=[HTTPMethod.POST.value])
def save_email_route():
    return email_controller.save_email()


@api_v1.route('/event/', methods=[HTTPMethod.POST.value])
def create_event_route():
    return event_controller.create_event()


@api_v1.route('/user/', methods=[HTTPMethod.POST.value])
def create_user_route():
    return user_controller.create_user()


@api_v1.route('/recipient/', methods=[HTTPMethod.POST.value])
def create_recipient_route():
    return recipient_controller.create_recipient()
