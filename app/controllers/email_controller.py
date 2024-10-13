from http import HTTPStatus

from flask import request

from app.controllers.controller import Controller
from app.interfaces.email_interface import EmailInterface
from app.schemas.email import EmailSchema
from app.services.email_service import schedule_email
from app.utils.decorators import safe_load


class EmailController(Controller):
    def __init__(self):
        self.email_schema = EmailSchema()

    @safe_load
    def save_email(self):
        """
        Method to handle scheduling an email.
        """

        data = self.email_schema.load(request.json)

        email = EmailInterface(**data)

        response = schedule_email(email)

        return self.response("Create email successfully",  status_code=HTTPStatus.CREATED)
