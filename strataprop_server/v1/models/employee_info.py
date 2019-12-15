import time
from strataprop_server.v1.common.constants import EMPLOYEE_INFO
from strataprop_server.v1.common.functions import generate_id
from strataprop_server import db


class EmployeeInfo(db.Model):
    __tablename__ = EMPLOYEE_INFO
    __bind_key__ = 'DATABASE_URI'
    id = db.Column(db.String, primary_key=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    email = db.Column(db.String,unique=True, nullable=False)
    mobile_number = db.Column(db.String)
    created_on = db.Column(db.Float, default=round(time.time() * 1000))

    def __init__(self, *args, **kwargs):
        self.id = kwargs.get('uuid', kwargs.get('id', generate_id()))
        self.first_name = kwargs.get('first_name')
        self.last_name = kwargs.get('last_name')
        self.email = kwargs.get('email')
        self.created_on = kwargs.get('created_on')
        self.mobile_number = kwargs.get('mobile_number')

