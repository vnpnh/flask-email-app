from app.interfaces.event_interface import EventInterface
from app.models.event import Event


def create_event(data: EventInterface) -> Event:
    """
    Create a new event.
    :param data: the event data
    :return: the saved Event object
    """
    event = Event(**data)
    event.save()
    return event
