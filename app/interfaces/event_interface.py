from typing import TypedDict


class EventInterface(TypedDict, total=False):
    event_id: int
    event_name: str
    event_description: str
    event_date: str
