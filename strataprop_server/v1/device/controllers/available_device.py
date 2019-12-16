from flask_restful import Resource
from strataprop_server import app, sentry
from strataprop_server.v1.device.services import get_device
from strataprop_server.v1.status_codes import *
from strataprop_server.v1.common.exceptions import  *


class AvailableDeviceAPI(Resource):

    def get(self):
        try:
            result, msg, status = get_device(available_devices=True)
            return {"status": OK, "msg": msg, "data": result}, OK
        except BadRequest:
            return {"status": BAD_REQUEST, "msg": "Some error occured"}, BAD_REQUEST
        except:
            import traceback
            app.logger.error('Unknown Error in Device  api'.format(str(traceback.print_exc())))
            sentry.captureException()
            return {"status": INTERNAL_SERVER_ERROR, "msg": "some error occured"}, INTERNAL_SERVER_ERROR