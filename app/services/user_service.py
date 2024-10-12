from app.interfaces.user_interface import UserInterface
from app.models.user import User


def create_user(data: UserInterface) -> User:
    """
    Create a new user.
    :param data: the user data
    :return: the saved User object
    """
    user = User(**data)
    user.save()
    return user
