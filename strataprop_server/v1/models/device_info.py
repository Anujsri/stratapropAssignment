import time
from strataprop_server.v1.common.constants import  DEVICE_INFO
from strataprop_server.v1.common.functions import generate_id
from strataprop_server import db


class DeviceInfo(db.Model):
    __tablename__ = DEVICE_INFO
    __bind_key__ = 'DATABASE_URI'
    id = db.Column(db.String, primary_key=True)
    device_name = db.Column(db.String,nullable=False,unique=True)
    created_on = db.Column(db.Float, default=round(time.time() * 1000))
    is_free = db.Column(db.Boolean, default=True)

    def __init__(self, *args, **kwargs):
        self.id = kwargs.get('uuid', kwargs.get('id', generate_id()))
        self.device_name = kwargs.get('device_name')
        self.created_on = kwargs.get('created_on')
        elf.is_free = kwargs.get('is_free', True)

