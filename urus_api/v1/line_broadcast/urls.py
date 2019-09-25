from flask_restful import Resource, Api
from urus_api.v1.line_broadcast.views import Order, Cancel, Update, UserStatus
from flask import Blueprint
from urus_api.config import Config

line_broadcast_bp = Blueprint(
    'line_broadcast', __name__, url_prefix=f'/Urus/{Config.API_VERSION}/line_broadcast')
api = Api(line_broadcast_bp)

# add resource
api.add_resource(Order, '/order')
api.add_resource(Cancel, '/cancel')
api.add_resource(UserStatus, '/user_status')
api.add_resource(Update, '/update')
