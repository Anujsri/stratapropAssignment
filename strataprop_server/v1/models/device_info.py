import time
from strataprop_server.v1.common.constants import  DEVICE_INFO,EMPLOYEE_INFO
from strataprop_server.v1.common.functions import generate_id
from strataprop_server import db


class DeviceInfo(db.Model):
    __tablename__ = DEVICE_INFO
    __bind_key__ = 'DATABASE_URI'
    id = db.Column(db.String, primary_key=True)
    device_name = db.Column(db.String,nullable=False,unique=True)
    created_on = db.Column(db.Float, default=round(time.time() * 1000))
    is_free = db.Column(db.Boolean, default=True)
    employee_id = db.Column(db.String, db.ForeignKey('{}.id'.format(EMPLOYEE_INFO)),nullable=True)
    model_name = db.Column(db.String)

    def __init__(self, *args, **kwargs):
        self.id = kwargs.get('uuid', kwargs.get('id', generate_id()))
        self.device_name = kwargs.get('device_name')
        self.created_on = kwargs.get('created_on')
        self.is_free = kwargs.get('is_free', True)
        self.employee_id = kwargs.get('employee_id')
        self.model_name = kwargs.get('model_name')
