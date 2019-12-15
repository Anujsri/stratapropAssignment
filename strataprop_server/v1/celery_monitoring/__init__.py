from flask import Blueprint
from flask_restful import Api

from strataprop_server.v1.celery_monitoring.controllers.celery_worker_status_api import CeleryWorkerStatus

celery_monitoring_blueprint = Blueprint('celery_monitoring_blueprint_v1', __name__)
api = Api(celery_monitoring_blueprint, prefix='/api/v1/celery-monitoring')

api.add_resource(CeleryWorkerStatus, '/status', strict_slashes=False)
# api.add_resource(MemberVerticalMapping, '/', strict_slashes=False)
