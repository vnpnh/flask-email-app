from typing import Optional, Union

from flask import jsonify


class Controller:

    @staticmethod
    def response(
            message: str,
            data: Optional[Union[dict, list]] = None,
            status_code: int = 200,
    ) -> tuple:
        """
        Return a JSON response.

        :param message: The message to return with the response.
        :param data: The data to return (optional, can be a dictionary or list).
        :param status_code: The HTTP status code (default is 200).
        :return: A tuple containing the JSON response and status code.
        """
        status = "success" if status_code < 400 else "error"
        response = {
            "status": status,
            "message": message,
            "data": data,
            "error": None if status_code < 400 else message
        }

        return jsonify(response), status_code
