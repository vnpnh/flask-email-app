from http import HTTPStatus

from flask import request

from app.controllers.controller import Controller
from app.interfaces.user_interface import UserInterface
from app.schemas.user import UserSchema
from app.services.user_service import create_user
from app.utils.decorators import safe_load


class UserController(Controller):
    def __init__(self):
        self.user_schema = UserSchema()

    @safe_load
    def create_user(self):
        """
        Method to handle creating a user.
        """
        data = self.user_schema.load(request.json)

        event = UserInterface(**data)

        response = create_user(event)

        return self.response("Create user successfully",  status_code=HTTPStatus.CREATED)
