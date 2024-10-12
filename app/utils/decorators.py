from functools import wraps
from flask import jsonify, request
from marshmallow import ValidationError

def safe_load(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except ValidationError as err:
            return jsonify(error="Validation Error", message=err.messages), 400
        except Exception as e:
            return jsonify(error="Internal Server Error", message=str(e)), 500
    return decorated_function
