from http import HTTPStatus

from flask import request

from app.controllers.controller import Controller
from app.interfaces.recipient_interface import RecipientInterface
from app.schemas.recipient import RecipientSchema
from app.services.recipient_service import create_recipient
from app.utils.decorators import safe_load


class RecipientController(Controller):
    def __init__(self):
        self.recipient_schema = RecipientSchema()

    @safe_load
    def create_recipient(self):
        """
        Method to handle creating a recipient.
        """
        data = self.recipient_schema.load(request.json)

        recipient = RecipientInterface(**data)

        create_recipient(recipient)

        return self.response("Create recipient successfully",  status_code=HTTPStatus.CREATED)
