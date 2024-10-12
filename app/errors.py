from flask import jsonify


def handle_404_error(e):
    """
    Handle the 404 Not Found error by returning a custom JSON response.

    Args:
        e (Exception): The exception that caused the 404 error, passed automatically by Flask.

    Returns:
        response (Response): A Flask Response object with a JSON payload describing the error
        and a status code of 404.
    """
    response = jsonify(
        {
            'error': 'Not Found',
            'message': 'The requested URL was not found on the server.'
        }
    )
    response.status_code = 404
    return response


def handle_500_error(e):
    """
    Handle the 500 Internal Server Error by returning a custom JSON response.

    Args:
       e (Exception): The exception that caused the 500 error, passed automatically by Flask.

    Returns:
       response (Response): A Flask Response object with a JSON payload describing the error
       and a status code of 500.
   """
    response = jsonify(
        {
            'error': 'Internal Server Error',
            'message': 'An unexpected error occurred on the server.'
        }
    )
    response.status_code = 500
    return response
