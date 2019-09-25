from flask_restful import abort
from functools import wraps
from urus_api.utility.response_formmater import ResponseFormatter


def validate_contentType(action, request, content_types):

    def outer_validate(func):

        @wraps(func)
        def validate(*args, **kargs):
            contentType = request.headers['Content-Type']
            if contentType not in content_types:
                result_msg = {"msg": "Invalid Content-Type"}
                rep = ResponseFormatter(action, result_msg).error()
                abort(400, **rep)
            return func(*args, **kargs)

        return validate

    return outer_validate