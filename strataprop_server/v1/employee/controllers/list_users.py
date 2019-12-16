from flask import request, g
from flask_restful import Resource
from strataprop_server import app, sentry
from strataprop_server.v1.employee.services import create_employee,update_employee,get_employee
from strataprop_server.v1.status_codes import *
from strataprop_server.v1.common.exceptions import  *


class CreateUserAPI(Resource):

    def get(self):
        try:
            employee_id = request.args.get('id')
            result, msg, status = get_employee(employee_id)
            return {"status": OK, "msg": msg, "data": result}, OK
        except BadRequest:
            return {"status": BAD_REQUEST, "msg": "Form details not shared"}, BAD_REQUEST
        except EmployeeNotFound:
            msg = "Empolyee does not exist"
            return {"status": BAD_REQUEST, "msg": msg}, BAD_REQUEST
        except:
            import traceback
            app.logger.error('Unknown Error in Employee api'.format(str(traceback.print_exc())))
            sentry.captureException()
            return {"status": INTERNAL_SERVER_ERROR, "msg": "some error occured"}, INTERNAL_SERVER_ERROR        

    def post(self):
        
        try:
            json_data = None
            json_data = request.json
            result, msg, status = create_employee(json_data)
            return {"status": OK, "msg": msg, "data": result}, OK

        except BadRequest:
            return {"status": BAD_REQUEST, "msg": "Form details not shared"}, BAD_REQUEST
        except DuplicateEntry:
            msg = "Empolyee already present in the system"
            return {"status": BAD_REQUEST, "msg": msg}, BAD_REQUEST
        except EmployeeBasicInfoNotFoundException:
            msg = "Empolyee basic info not found like first name,last name etc.."
            return {"status": BAD_REQUEST, "msg": msg}, BAD_REQUEST
        except InvalidEmployeeNameException:
            msg = "Name is not valid only character is allowed"
            return {"status": BAD_REQUEST, "msg": msg}, BAD_REQUEST
        except InvalidMobileNumber:
            msg = "Mobile is not valid should have length 10/should contais only number"
            return {"status": BAD_REQUEST, "msg": msg}, BAD_REQUEST
        except InvalidEmail:
            msg = "Email is is not valid"
            return {"status": BAD_REQUEST, "msg": msg}, BAD_REQUEST
        except:
            import traceback
            app.logger.error('Unknown Error in Employee api'.format(str(traceback.print_exc())))
            sentry.captureException()
            return {"status": INTERNAL_SERVER_ERROR, "msg": "some error occured"}, INTERNAL_SERVER_ERROR

    def put(self):
        try:
            employee_id = request.args.get('id')
            json_data = None
            json_data = request.json
            result, msg, status = update_employee(json_data,employee_id)
            return {"status": OK, "msg": msg, "data": result}, OK
        except BadRequest:
            return {"status": BAD_REQUEST, "msg": "Form details not shared"}, BAD_REQUEST
        except DuplicateEntry:
            msg = "Empolyee already present in the system"
            return {"status": BAD_REQUEST, "msg": msg}, BAD_REQUEST
        except EmployeeBasicInfoNotFoundException:
            msg = "Empolyee basic info not found like first name,last name etc.."
            return {"status": BAD_REQUEST, "msg": msg}, BAD_REQUEST
        except InvalidEmployeeNameException:
            msg = "Name is not valid only character is allowed"
            return {"status": BAD_REQUEST, "msg": msg}, BAD_REQUEST
        except InvalidMobileNumber:
            msg = "Mobile is not valid should have length 10/should contais only number"
            return {"status": BAD_REQUEST, "msg": msg}, BAD_REQUEST
        except InvalidEmail:
            msg = "Email is is not valid"
            return {"status": BAD_REQUEST, "msg": msg}, BAD_REQUEST
        except EmployeeNotFound:
            msg = "Empolyee does not exist"
            return {"status": BAD_REQUEST, "msg": msg}, BAD_REQUEST
        except:
            import traceback
            app.logger.error('Unknown Error in Employee api'.format(str(traceback.print_exc())))
            sentry.captureException()
            return {"status": INTERNAL_SERVER_ERROR, "msg": "some error occured"}, INTERNAL_SERVER_ERROR
