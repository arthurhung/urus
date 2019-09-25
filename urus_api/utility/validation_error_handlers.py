from flask_restful import abort

from urus_api.utility.response_formmater import ResponseFormatter


def validation_error_400(err, data, schema):
    action = schema.get('id')
    result_msg = {"msg": err.message}
    rep = ResponseFormatter(action, result_msg).error(error_type='ValidationError')
    abort(400, **rep)