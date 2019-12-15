import celery
import raven
from raven.contrib.celery import register_signal, register_logger_signal
from werkzeug.exceptions import Unauthorized

Unauthorized.description = 'Please login to access this page.'
from celery import Celery


class Celery(celery.Celery):
    """Configure celery on sentry"""

    def on_configure(self):
        client = raven.Client(
            'https://550053cd21ac437483a2e9351993f13a:d221e97252664bd08b919e2b7a137ec7@sentry.io/1227928'
        )
        # register a custom filter to filter out duplicate logs
        register_logger_signal(client)
        # hook into the Celery error handler
        register_signal(client)


def make_celery(app=None):
    celery = Celery(
        app.import_name,
        backend=app.config['CELERY_RESULT_BACKEND'],
        broker=app.config['CELERY_BROKER_URL'],
        include=[
            
        ]
    )
    client = raven.Client(
        'https://550053cd21ac437483a2e9351993f13a:d221e97252664bd08b919e2b7a137ec7@sentry.io/1227928'
    )
    register_logger_signal(client)
    register_signal(client)
    celery.conf.update(app.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask
    return celery

