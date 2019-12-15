import os
import re
import time
from sqlalchemy import or_, false, true
from sqlalchemy.orm.exc import NoResultFound
from strataprop_server import db, celery, app,sentry
from strataprop_server.v1.status_codes import *
from strataprop_server import DeviceInfo
from strataprop_server.v1.common.functions import  check_is_alpha
from strataprop_server.v1.common.exceptions import  *
import json

def get_device(device_id=None):
    if(device_id):
        device = db.session.query(DeviceInfo).filter(DeviceInfo.id == device_id).first()
        if not device:
            raise DeviceNotFound
        try:
            data_to_fetch = ['device_name','created_on']
            device_details = dict()
            for attr in data_to_fetch:
                if getattr(device, attr):
                    if attr == 'created_on':
                        device_details[attr] = int(getattr(device, attr) or 0)
                    else:
                        device_details[attr] = getattr(device, attr)
                else:
                    device_details[attr] = None
            return device_details, "", OK
        except:
            db.session.rollback()
            import traceback
            app.logger.error('Unknown Error in Device api'.format(str(traceback.print_exc())))
            sentry.captureException()
            raise BadRequest
    else:
        try:
            devices = db.session.query(DeviceInfo).all()
            result = {}
            result['devices']  = []
            if devices:
                for device in devices:
                    d = {}
                    d['device_name'] = device.device_name
                    d['created_on'] = device.created_on
                    result['devices'].append(d)
            return result['devices'], "", OK
        except:
            db.session.rollback()
            import traceback
            app.logger.error('Unknown Error in Device list api'.format(str(traceback.print_exc())))
            sentry.captureException()
            raise BadRequest


def create_device(form_data):
    from strataprop_server.v1.common.functions import generate_id

    device_name = form_data.get('device_name')

    if not device_name:
        raise DeviceNotFound

    if not check_is_alpha(device_name):
        raise InvalidDeviceNameException

    device = db.session.query(DeviceInfo).filter(DeviceInfo.device_name == device_name).first()
    if device:
        raise DuplicateEntry

    device_obj = DeviceInfo(
        uuid = generate_id(),
        device_name =device_name
    )
    try:
        db.session.add(device_obj)
        db.session.commit()
        return "OK", "Data Inserted", OK
    except Exception:
        db.session.rollback()
        import traceback
        app.logger.error('Unknown Error in Device api'.format(str(traceback.print_exc())))
        sentry.captureException()
        raise BadRequest


def update_device(form_data,device_id):
    device = db.session.query(DeviceInfo).filter(DeviceInfo.id == device_id).first()
    if not device:
        raise DeviceNotFound

    device_name = form_data.get('device_name')

    if not device_name:
        raise DeviceNotFound

    if not check_is_alpha(device_name):
        raise InvalidDeviceNameException

    device.device_name = device_name

    try:
        db.session.add(device)
        db.session.commit()
        return "OK", "Data Updated", OK
    except:
        db.session.rollback()
        import traceback
        app.logger.error('Unknown Error in Device api'.format(str(traceback.print_exc())))
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
