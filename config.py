# -*- coding: utf-8 -*-
import os

from celery.schedules import crontab

basedir = os.path.abspath(os.path.dirname(__file__))


SECURITY_EMAIL_SENDER = 'no-reply@loktra.com'
MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True

CELERY_DEFAULT_QUEUE = "default"
CELERY_QUEUES = {
    'default': {
        'exchange': 'default',
        'binding_key': 'default',
        'routing_key': 'default'
    },
    'retry': {
        'exchange': 'retry',
        'routing_key': 'retry'
    },
    'trigger': {
        'exchange': 'trigger',
        'routing_key': 'trigger'
    }
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,

    'formatters': {
        'console': {
            'format': '[%(asctime)s][%(levelname)s] %(name)s '
                      '%(filename)s:%(funcName)s:%(lineno)d | %(message)s \n',
            'datefmt': '%Y-%m-%d %H:%M:%S %z',
        },
        'sentry': {
            'format': '[%(asctime)s][%(levelname)s] %(name)s '
                      '%(filename)s:%(funcName)s:%(lineno)d | %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S %z',
        }
    },

    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'console'
        },
        'sentry': {
            'level': 'INFO',
            'class': 'raven.handlers.logging.SentryHandler',
            # 'dsn': 'https://550053cd21ac437483a2e9351993f13a:d221e97252664bd08b919e2b7a137ec7@sentry.io/1227928',
            'formatter': 'sentry'
        },
    },

    'loggers': {
        '': {
            'propagate': False,
            'handlers': ['console'],
            'level': 'DEBUG',
        }
    }
}


class Config(object):
    MAIL_USERNAME = os.environ['MAIL_USERNAME']
    MAIL_PASSWORD = os.environ['MAIL_PASSWORD']
    # LOGIN_API = os.environ['LOGIN_API'] if os.environ['LOGIN_API'] and len(os.environ['LOGIN_API']) > 0 else None
    # LOGGING_API_KEY = os.environ['LOGGING_API_KEY']
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SECRET_KEY = os.environ['APP_SECRET_KEY']
    APP_KEY = os.environ['APP_KEY']
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_BINDS = {
        'DATABASE_URI': os.environ.get('DATABASE_URL')
    }
    DATABASE_USER = os.environ.get('DATABASE_USER')
    DATABASE_PASSWORD = os.environ.get('DATABASE_PASSWORD')
    REDIS_URL = os.environ['REDIS_URL']
    CELERY_BROKER_URL = REDIS_URL 
    CELERY_RESULT_BACKEND = REDIS_URL 
    MAIL_SERVER = MAIL_SERVER
    MAIL_PORT = MAIL_PORT
    MAIL_USE_TLS = MAIL_USE_TLS
    MAIL_USE_SSL = MAIL_USE_SSL
    MAIL_USERNAME = MAIL_USERNAME
    MAIL_PASSWORD = MAIL_PASSWORD
    LOGGING = LOGGING
    SQLALCHEMY_POOL_SIZE = 200
    SQLALCHEMY_POOL_RECYCLE = 300
    CELERY_QUEUES = CELERY_QUEUES
    CELERY_DEFAULT_QUEUE = CELERY_DEFAULT_QUEUE
    # CELERYBEAT_SCHEDULE = CELERYBEAT_SCHEDULE
    MANDRILL_API_KEY = '9o68rvv-VGPKBK0uLjOLQg'


class ProductionConfig(Config):
    DEBUG = False
    LOCATION_LENGTH_MAX = 5


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    TESTING = True


class TestingConfig(Config):
    TESTING = True
