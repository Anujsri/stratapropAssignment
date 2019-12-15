from flask import request, g
from flask_restful import Resource

from strataprop_server import app, sentry
# from strataprop_server.v1.auth.login_decorators import login_required, roles_required
from strataprop_server.v1.device.user_functions import create_device,update_device,get_device
from strataprop_server.v1.status_codes import *
from strataprop_server.v1.common.exceptions import  *


class DeviceAPI(Resource):
    # method_decorators = [login_required, roles_required(["mis", "manager","tele","tele-manager","tele-source-management"])]

    def get(self):
        try:
            # member = g.user
            device_id = request.args.get('id')
            result, msg, status = get_device(device_id)
            return {"status": OK, "msg": msg, "data": result}, OK
        except BadRequest:
            return {"status": BAD_REQUEST, "msg": "Form details not shared"}, BAD_REQUEST
        except DeviceNotFound:
            msg = "Device does not exist"
            return {"status": BAD_REQUEST, "msg": msg}, BAD_REQUEST
        except:
            import traceback
            app.logger.error('Unknown Error in Device  api'.format(str(traceback.print_exc())))
            sentry.captureException()
            return {"status": INTERNAL_SERVER_ERROR, "msg": "some error occured"}, INTERNAL_SERVER_ERROR 


    def post(self):
        # member = g.user
        
        try:
            json_data = None
            json_data = request.json
            result, msg, status = create_device(json_data)
            return {"status": OK, "msg": msg, "data": result}, OK

        except BadRequest:
            return {"status": BAD_REQUEST, "msg": "Form details not shared"}, BAD_REQUEST
        except DuplicateEntry:
            msg = "Device already present in the system"
            return {"status": BAD_REQUEST, "msg": msg}, BAD_REQUEST
        except DeviceNotFound:
            msg = "Device name can not be empaty"
            return {"status": BAD_REQUEST, "msg": msg}, BAD_REQUEST
        except InvalidDeviceNameException:
            msg = "Device Name is not valid only character is allowed"
            return {"status": BAD_REQUEST, "msg": msg}, BAD_REQUEST
        except:
            import traceback
            app.logger.error('Unknown Error in Device api'.format(str(traceback.print_exc())))
            sentry.captureException()
            return {"status": INTERNAL_SERVER_ERROR, "msg": "some error occured"}, INTERNAL_SERVER_ERROR

    def put(self):
        try:
            # member = g.user
            json_data = None
            json_data = request.json
            device_id = request.args.get('id')
            result, msg, status = update_device(json_data,device_id)
            return {"status": OK, "msg": msg, "data": result}, OK
        except BadRequest:
            return {"status": BAD_REQUEST, "msg": "Form details not shared"}, BAD_REQUEST
        except DuplicateEntry:
            msg = "Device already present in the system"
            return {"status": BAD_REQUEST, "msg": msg}, BAD_REQUEST
        except InvalidDeviceNameException:
            msg = "Device Name is not valid only character is allowed"
            return {"status": BAD_REQUEST, "msg": msg}, BAD_REQUEST
        except DeviceNotFound:
            msg = "Device does not exist"
            return {"status": BAD_REQUEST, "msg": msg}, BAD_REQUEST
        except:
            import traceback
            app.logger.error('Unknown Error in Device api'.format(str(traceback.print_exc())))
            sentry.captureException()
            return {"status": INTERNAL_SERVER_ERROR, "msg": "some error occured"}, INTERNAL_SERVER_ERROR
