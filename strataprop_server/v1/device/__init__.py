from flask import Blueprint
from flask_restful import Api

from strataprop_server.v1.device.controllers.list_users import DeviceAPI
from strataprop_server.v1.device.controllers.assign_device import AssignDeviceAPI
from strataprop_server.v1.device.controllers.unassign_device import UnAssignDeviceAPI
from strataprop_server.v1.device.controllers.available_device import AvailableDeviceAPI

device_blueprint = Blueprint('device_blueprint_v1', __name__)
api = Api(device_blueprint, prefix='/api/v1/device')

api.add_resource(DeviceAPI, '/create-device', strict_slashes=False)
api.add_resource(AssignDeviceAPI, '/assign', strict_slashes=False)
api.add_resource(UnAssignDeviceAPI, '/unassign', strict_slashes=False)
api.add_resource(AvailableDeviceAPI, '/abailable-device', strict_slashes=False)