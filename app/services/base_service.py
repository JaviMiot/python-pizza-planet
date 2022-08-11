from functools import wraps
from flask import jsonify


def base_service(status_code=200, name=None):
    def decorator(service):
        @wraps(service)
        def wrapped(*args, **kwargs):
            data, error = service(*args, **kwargs)
            response = data if not error else {'error': error}
            status = status_code if data else 404 if not error else 400
            return jsonify(response), status
        return wrapped
    return decorator
