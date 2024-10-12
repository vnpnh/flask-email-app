from app.interfaces.recipient_interface import RecipientInterface
from app.models.recipient import Recipient


def create_recipient(data: RecipientInterface) -> None:
    """
    Create a new recipient.
    :param data: the recipient data
    :return: the saved recipient object
    """

    for user_id in data['user_id']:
        new_recipient = Recipient(user_id=user_id, event_id=data['event_id'])
        new_recipient.save()
