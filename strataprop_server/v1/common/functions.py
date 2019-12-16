import uuid
import traceback
from strataprop_server import app
from strataprop_server import celery
def generate_id():
    return str(uuid.uuid4())

@celery.task
def send_mail(name,email,device_name,device_id,message):
    from flask_mail import Mail,Message
    from flask import Flask
    import os
    app = Flask(__name__)
    app.config.from_object(os.environ['APP_SETTINGS'])
    LOGIN_USER_NAME = app.config.get('MAIL_USERNAME')
    LOGIN_PASSWD = app.config.get('MAIL_PASSWORD')
    SMTP_SERVER = app.config.get('MAIL_SERVER')
    MAIL_PORT = app.config.get('MAIL_PORT')
    MAIL_USE_TLS = app.config.get('MAIL_USE_TLS')
    MAIL_USE_SSL = app.config.get('MAIL_USE_SSL')
    app.config.update(dict(
        DEBUG = True,
        MAIL_SERVER = SMTP_SERVER,
        MAIL_PORT = MAIL_PORT,
        MAIL_USE_TLS = MAIL_USE_TLS,
        MAIL_USE_SSL = MAIL_USE_SSL,
        MAIL_USERNAME = LOGIN_USER_NAME,
        MAIL_PASSWORD = LOGIN_PASSWD,
    ))
    
    try:
        mail = Mail(app)

        msg = Message("Update on Your Device",sender="anujsrivastava@iiitdmj.ac.in",recipients=[email])
        # msg.body = "anuj testing"
        msg.html = 'Hi ' + name + ',<br>' +  message + '<br><div style="margin-right:-15px;margin-left:-15px;">' + '<div style="position:relative;min-height:1px;padding-right:15px;padding-left:15px;@media (min-width:992px){float:left};width:66.66666667%;margin-left:16.66666667%;margin-right:16.66666667%;" >' +'<div  style="padding-left:0;margin-bottom:20px">' +'<li style="position:relative;display:block;padding:10px 15px;margin-bottom:-1px;background-color:#5499C7;color : white;font-size: 20px;"><center><b>Device Details</b></center></li>' +'<li style="position:relative;display:block;padding:10px 15px;margin-bottom:-1px;background-color:#fff;border:1px solid #AEB6BF"><b>Name : </b>'  + device_name +'</li>' +'<li style="position:relative;display:block;padding:10px 15px;margin-bottom:-1px;background-color:#fff;border:1px solid #AEB6BF"><b>Device Id. :  </b>'  + device_id + '</li>' +'<li style="position:relative;display:block;padding:10px 15px;margin-bottom:-1px;background-color:#fff;border:1px solid #AEB6BF"><b>Diseases Name. :  </b>'  + '</li>' +'</div>' +'</div>' +'</div>'
        mail.send(msg)
    except:
        import traceback
        print (traceback.print_exc())
        print ("Mail Sending Failed")


def check_is_alpha(string):
    string = str(string)
    return all([x.isalpha() or x.isspace() for x in string])
