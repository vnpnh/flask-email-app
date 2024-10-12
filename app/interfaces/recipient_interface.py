from typing import TypedDict


class RecipientInterface(TypedDict, total=False):
    user_id: list[int]
    event_id: int
