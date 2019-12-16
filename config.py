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
