from flask import request, g
from flask_restful import Resource
from strataprop_server import app, sentry
from strataprop_server.v1.device.services import unassign_device
from strataprop_server.v1.status_codes import *
from strataprop_server.v1.common.exceptions import  *


class UnAssignDeviceAPI(Resource):
    def put(self):
        try:
            json_data = None
            json_data = request.json
            result, msg, status = unassign_device(json_data)
            return {"status": OK, "msg": msg, "data": result}, OK
        except BadRequest:
            return {"status": BAD_REQUEST, "msg": "Form details not shared"}, BAD_REQUEST
        except DeviceNotFree:
            msg = "This Device already assigned to other employee"
            return {"status": BAD_REQUEST, "msg": msg}, BAD_REQUEST
        except EmployeeNotFound:
            msg = "Employee does not exist"
            return {"status": BAD_REQUEST, "msg": msg}, BAD_REQUEST
        except DeviceNotFound:
            msg = "Device does not exist"
            return {"status": BAD_REQUEST, "msg": msg}, BAD_REQUEST
        except:
            import traceback
            app.logger.error('Unknown Error in Device api'.format(str(traceback.print_exc())))
            sentry.captureException()
            return {"status": INTERNAL_SERVER_ERROR, "msg": "some error occured"}, INTERNAL_SERVER_ERROR
