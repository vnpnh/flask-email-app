from app.interfaces.email_interface import EmailInterface
from app.models import Email


def schedule_email(data: EmailInterface) -> Email:
    """
    Schedule a new email to be sent at a specific time.

    :param data: The email data to be scheduled.
    :return: The saved Email object
    """

    new_email = Email(**data)

    new_email.save()

    return new_email
