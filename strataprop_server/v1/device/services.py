import os
import re
import time
from strataprop_server import db, celery, app,sentry
from strataprop_server.v1.status_codes import *
from strataprop_server import DeviceInfo,EmployeeInfo
from strataprop_server.v1.common.functions import  check_is_alpha
from strataprop_server.v1.common.exceptions import  *
import json

def get_device(device_id=None,available_devices=None):
    if(device_id):
        device = db.session.query(DeviceInfo).filter(DeviceInfo.id == device_id).first()
        if not device:
            raise DeviceNotFound
        try:
            data_to_fetch = ['device_name','created_on','model_name']
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
            if available_devices:
                devices = db.session.query(DeviceInfo).filter(DeviceInfo.is_free.isnot(False)).all()
            else:
                devices = db.session.query(DeviceInfo).all()
            result = {}
            result['devices']  = []
            if devices:
                for device in devices:
                    d = {}
                    d['device_name'] = device.device_name
                    d['created_on'] = device.created_on
                    d['model_name'] = device.model_name
                    d['is_free'] = device.is_free
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
    model_name = form_data.get('model_name')

    if not device_name:
        raise DeviceNotFound

    if not check_is_alpha(device_name):
        raise InvalidDeviceNameException

    device.device_name = device_name
    device.model_name = model_name

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

def assign_device(form_data):
    from strataprop_server.v1.common.functions import send_mail
    device_id  = form_data.get('device_id')
    employee_id = form_data.get('employee_id')

    device = db.session.query(DeviceInfo).filter(DeviceInfo.id == device_id).first()
    if not device:
        raise DeviceNotFound

    emaployee = db.session.query(EmployeeInfo).filter(EmployeeInfo.id == employee_id).first()
    if not emaployee:
        raise EmployeeNotFound

    if not device.is_free:
        raise DeviceNotFree

    device.employee_id = employee_id;
    device.is_free = False
    try:
        name = emaployee.first_name + " " + emaployee.last_name
        db.session.add(device)
        db.session.commit();
        send_mail.apply_async(
            queue='default',
            routing_key='default',
            args=[name,emaployee.email,device.device_name,device.id,device.model_name,"You have been assigned with new device"]
        )
        return "OK", "Device is assigned", OK
    except:
        db.session.rollback()
        import traceback
        app.logger.error('Unknown Error in Device api'.format(str(traceback.print_exc())))
        sentry.captureException()
        raise BadRequest


def unassign_device(form_data):
    from strataprop_server.v1.common.functions import send_mail
    device_id  = form_data.get('device_id')
    employee_id = form_data.get('employee_id')

    device = db.session.query(DeviceInfo).filter(DeviceInfo.id == device_id).first()
    if not device:
        raise DeviceNotFound

    emaployee = db.session.query(EmployeeInfo).filter(EmployeeInfo.id == employee_id).first()
    if not emaployee:
        raise EmployeeNotFound

    device.is_free = True
    device.employee_id = None

    try:
        name = emaployee.first_name + " " + emaployee.last_name
        db.session.add(device)
        db.session.commit();
        send_mail.apply_async(
            queue='default',
            routing_key='default',
            args=[name,emaployee.email,device.device_name,device.id,device.model_name,"You have been unassigned with a device"]
        )
        return "OK", "Device is unassigned", OK
    except:
        db.session.rollback()
        import traceback
        app.logger.error('Unknown Error in Device api'.format(str(traceback.print_exc())))
        sentry.captureException()
        raise BadRequest


def assign_details():
    try:
        result = []
        assigned_details = db.session.query(EmployeeInfo,DeviceInfo).filter(DeviceInfo.employee_id == EmployeeInfo.id).all()
        for data in assigned_details:
            d = {}
            d['first_name'] = data.EmployeeInfo.first_name
            d['last_name'] = data.EmployeeInfo.last_name
            d['email'] = data.EmployeeInfo.email
            d['mobile_number']  = data.EmployeeInfo.mobile_number
            d['device_name'] = data.DeviceInfo.device_name
            result.append(d)
        return result, "", OK
    except:
        db.session.rollback()
        import traceback
        app.logger.error('Unknown Error in Device api'.format(str(traceback.print_exc())))
        sentry.captureException()
        raise BadRequest



