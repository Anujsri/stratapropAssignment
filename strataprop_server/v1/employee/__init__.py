from flask import Blueprint
from flask_restful import Api

from strataprop_server.v1.employee.controllers.list_users import CreateUserAPI

employee_blueprint = Blueprint('employee_blueprint_v1', __name__)
api = Api(employee_blueprint, prefix='/api/v1/employee')

api.add_resource(CreateUserAPI, '/list-users', strict_slashes=False)
