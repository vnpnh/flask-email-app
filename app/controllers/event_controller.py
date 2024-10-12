from http import HTTPStatus

from flask import request

from app.controllers.controller import Controller
from app.interfaces.event_interface import EventInterface
from app.schemas.event import EventSchema
from app.services.event_service import create_event
from app.utils.decorators import safe_load


class EventController(Controller):
    def __init__(self):
        self.event_schema = EventSchema()

    @safe_load
    def create_event(self):
        """
        Method to handle creating an event.
        """
        data = self.event_schema.load(request.json)

        event = EventInterface(**data)

        response = create_event(event)

        return self.response("Create event successfully",  status_code=HTTPStatus.CREATED)
