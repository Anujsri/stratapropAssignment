from flask import Blueprint
from flask_restful import Api

from strataprop_server.v1.device.controllers.list_users import DeviceAPI

device_blueprint = Blueprint('device_blueprint_v1', __name__)
api = Api(device_blueprint, prefix='/api/v1/device')

api.add_resource(DeviceAPI, '/create-device', strict_slashes=False)
