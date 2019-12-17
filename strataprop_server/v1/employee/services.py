from strataprop_server import db, celery, app,sentry
from strataprop_server.v1.status_codes import *
from strataprop_server import EmployeeInfo
from strataprop_server.v1.common.functions import  check_is_alpha,send_mail
from strataprop_server.v1.common.exceptions import  *
import json
import re
from sqlalchemy import func

def get_employee(employee_code=None):
    if(employee_code):
        emaployee = db.session.query(EmployeeInfo).filter(EmployeeInfo.employee_code == employee_code).first()
        if not emaployee:
            raise EmployeeNotFound
        try:
            data_to_fetch = ['first_name', 'last_name', 'email', 'mobile_number','created_on','employee_code']
            employee_details = dict()
            for attr in data_to_fetch:
                if getattr(emaployee, attr):
                    if attr == 'created_on':
                        employee_details[attr] = int(getattr(emaployee, attr) or 0)
                    else:
                        employee_details[attr] = getattr(emaployee, attr)
                else:
                    employee_details[attr] = None
            return employee_details, "", OK
        except:
            db.session.rollback()
            import traceback
            app.logger.error('Unknown Error in Empolyee list api'.format(str(traceback.print_exc())))
            sentry.captureException()
            raise BadRequest
    else:
        try:
            emaployees = db.session.query(EmployeeInfo).all()
            result = {}
            result['emaployees']  = []
            if emaployees:
                for emaployee in emaployees:
                    d = {}
                    d['first_name'] = emaployee.first_name
                    d['last_name'] = emaployee.last_name
                    d['email'] = emaployee.email
                    d['mobile_number'] = emaployee.mobile_number
                    d['created_on'] = emaployee.created_on
                    d['employee_code'] = emaployee.employee_code
                    result['emaployees'].append(d)
            return result['emaployees'], "", OK
        except:
            db.session.rollback()
            import traceback
            app.logger.error('Unknown Error in Empolyee list api'.format(str(traceback.print_exc())))
            sentry.captureException()
            raise BadRequest



def create_employee(form_data):
    from strataprop_server.v1.common.functions import generate_id,generate_random_code

    first_name = form_data.get('first_name')
    last_name = form_data.get('last_name')
    email = form_data.get('email')
    mobile_number = form_data.get('mobile_number')

    if not first_name or not last_name or not email or not mobile_number:
        raise EmployeeBasicInfoNotFoundException

    if not check_is_alpha(first_name) or not check_is_alpha(last_name):
        raise InvalidEmployeeNameException

    if not validate_mobile(mobile_number):
        raise InvalidMobileNumber
    
    if not check(email):
        raise InvalidEmail

    employee_code = generate_random_code()

    emaployee = db.session.query(EmployeeInfo).filter(EmployeeInfo.email == email).first()
    if emaployee:
        raise DuplicateEntry

    employee_obj = EmployeeInfo(
        uuid = generate_id(),
        first_name =first_name,
        last_name = last_name,
        mobile_number = mobile_number,
        email = email,
        employee_code = employee_code
    )
    try:
        db.session.add(employee_obj)
        db.session.commit()
        return "OK", "Data Inserted", OK
    except Exception:
        db.session.rollback()
        import traceback
        app.logger.error('Unknown Error in Empolyee list api'.format(str(traceback.print_exc())))
        sentry.captureException()
        raise BadRequest


def update_employee(form_data,employee_code):
    emaployee = db.session.query(EmployeeInfo).filter(EmployeeInfo.employee_code == employee_code).first()
    if not emaployee:
        raise EmployeeNotFound

    first_name = form_data.get('first_name')
    last_name = form_data.get('last_name')
    email = form_data.get('email')
    mobile_number = form_data.get('mobile_number')

    if not first_name or not last_name or not email or not mobile_number:
        raise EmployeeBasicInfoNotFoundException

    if not check_is_alpha(first_name) or not check_is_alpha(last_name):
        raise InvalidEmployeeNameException

    if not validate_mobile(mobile_number):
        raise InvalidMobileNumber
    
    if not check(email):
        raise InvalidEmail

    emaployee.first_name = first_name if first_name else emaployee.first_name
    emaployee.last_name = last_name if last_name else emaployee.last_name
    emaployee.mobile_number = mobile_number if mobile_number else emaployee.mobile_number
    emaployee.email = email if email else emaployee.email
    try:
        db.session.add(emaployee)
        db.session.commit()
        return "OK", "Data Updated", OK
    except:
        db.session.rollback()
        import traceback
        app.logger.error('Unknown Error in Empolyee list api'.format(str(traceback.print_exc())))
        sentry.captureException()
        raise BadRequest



# Define a function for for validating an Email 
def check(email):  
    regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
    # pass the regualar expression and the string in search() method 
    if(re.search(regex,email)):  
        return True  
          
    else:  
        return False


def validate_mobile(mobile_number):
    if (not mobile_number.isdigit()) or (len(mobile_number) !=10) :
        return False
    else:
        return True
