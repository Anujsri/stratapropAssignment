import logging.config
import os

from flask import Flask, render_template
from flask_compress import Compress
from flask_redis import FlaskRedis
from flask_sqlalchemy import SQLAlchemy
from raven.contrib.flask import Sentry
from redis import StrictRedis
from strataprop_server.v1.celery_config import make_celery
from flask_cors import CORS
from flask_caching import Cache

def create_app():
    app = Flask(
        __name__,
        template_folder=os.path.join(os.getcwd(), 'templates'),
        static_url_path=os.path.join(os.getcwd(), 'static'),
    )
    app.config.setdefault('SQLALCHEMY_TRACK_MODIFICATIONS', True)

    db = SQLAlchemy(app=app)
    cache_db = SQLAlchemy(app=app)
    db.init_app(app)
    return app, db, cache_db


app, db, cdb = create_app()
app.config.from_object(os.environ['APP_SETTINGS'])
redis_store = FlaskRedis.from_custom_provider(StrictRedis, app)
app.config['SESSION_SQLALCHEMY'] = db

celery = make_celery(app)
compress = Compress(app)
sentry = Sentry(app)

# models
from strataprop_server.v1.models.employee_info import EmployeeInfo
from strataprop_server.v1.models.device_info import DeviceInfo

db.create_all()

logging.config.dictConfig(app.config.get('LOGGING'))

from flask_sqlalchemy import models_committed
