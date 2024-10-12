from typing import TypedDict


class EmailInterface(TypedDict, total=False):
    event_id: int
    email_subject: str
    email_content: str
    scheduled_at: str
