from typing import TypedDict


class UserInterface(TypedDict, total=False):
    first_name: str
    last_name: str
    email: str
