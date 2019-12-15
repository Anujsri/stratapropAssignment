from flask_restful import Resource

from strataprop_server import app, sentry
from strataprop_server.v1.celery_monitoring.functions import get_celery_worker_status
from strataprop_server.v1.status_codes import *


class CeleryWorkerStatus(Resource):
    def get(self):
        try:
            result = get_celery_worker_status()
            return {"status": OK, "msg": "", "data": result}, OK
        except:
            import traceback
            app.logger.error('Unknown Error in celery worker status api')
            app.logger.error(traceback.print_exc())
            sentry.captureException()
            return {"status": INTERNAL_SERVER_ERROR, "msg": "some error occured"}, INTERNAL_SERVER_ERROR
