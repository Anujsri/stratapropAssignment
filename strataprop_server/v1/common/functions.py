import uuid
import json
import copy
import requests
import smtplib
import pytz
import re
import traceback
from strataprop_server import app
from strataprop_server.v1.status_codes import UNAUTHORIZED
from strataprop_server.v1.status_messages import UNAUTHORIZED_VIEW
from flask import render_template, url_for, jsonify
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import \
    BadSignature, \
    SignatureExpired
from random import randint
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def generate_id():
    return str(uuid.uuid4())

def epoch_timestamp(datetime_object):
    import datetime
    if not datetime_object:
        return None
    epoch_start = datetime.datetime.strptime('1970-01-01', '%Y-%m-%d')
    return round(((datetime_object - epoch_start).total_seconds()) * 1000)


def convert_to_datetime(epoch, time_zone=None):
    from datetime import datetime
    import pytz
    if not epoch:
        return None
    if time_zone:
        tz = pytz.timezone(time_zone)
        dt = datetime.fromtimestamp(epoch/1000, tz)
        naive_dt = dt.astimezone(tz).replace(tzinfo=None)
        return naive_dt
    return datetime.fromtimestamp(epoch/1000)


def convert_epoch_datetime(epoch_time, time_format="%d-%m-%Y"):
    try:
        import datetime
        return datetime.datetime.fromtimestamp(epoch_time/1000.0).strftime(time_format)
    except ValueError:
        import traceback
        app.logger.warning("Invalid date or time format")
        app.logger.exception(traceback.print_exc())
        return ''


def generate_random_code(length=6):
    """
    Generates a N digit random code.
    :param length: Random code which need to be generated.
    :return: random number of N digits.
    """
    range_start = 10 ** (length - 1)
    range_end = (10 ** length) - 1
    return randint(range_start, range_end)

def generate_auth_token(data, expiration=6000):
    """
    generates an auth token from the SECRET_KEY with the given data and expiration time.
    :param data: data to be added in token.
    :param expiration: expiration time in seconds.
    :return: generated token
    """
    serializer = Serializer(app.config.get('SECRET_KEY'))
    return serializer.dumps({
        'data': data
    })


def verify_auth_token(token):
    """
    Verifies the auth token from the SECRET_KEY
    :param token:
    :return:
    """
    serializer = Serializer(app.config.get('SECRET_KEY'))
    try:
        data, header = serializer.loads(token, return_header=True)
        return data
    except BadSignature:
        return None
    except SignatureExpired:
        return None

def unauthorized_view():
    response = jsonify(
        status=UNAUTHORIZED,
        msg=UNAUTHORIZED_VIEW
    )
    response.status_code = UNAUTHORIZED
    return response

def is_member_logged_in(member_id):
    try:
        from strataprop_server.v1.models.member_tokens import MemberTokens
        token_record = MemberTokens.query.filter(MemberTokens.member_id == member_id).first()
        if not token_record:
            return False
        return token_record
    except:
        app.logger.error(traceback.print_exc())
        app.logger.error("Reached Exception: is_member_logged_in")


def send_mail():
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

        msg = Message("Hello",sender="nujsrivastava@iiitdmj.ac.in",recipients=["anuj96sri@gmail.com"])
        msg.body = "testing"
        msg.html = "<b>testing</b>"
        mail.send(msg)
    except:
        import traceback
        print (traceback.print_exc())
        print ("Mail Sending Failed")


def check_is_alpha(string):
    string = str(string)
    return all([x.isalpha() or x.isspace() for x in string])
