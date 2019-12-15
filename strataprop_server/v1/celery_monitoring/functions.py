import time

from strataprop_server import app, db, celery


def get_celery_worker_status():
    from strataprop_server.v1.models.celery_workers_status_info import CeleryWorkersStatusInfo
    workers = CeleryWorkersStatusInfo.query.all()
    result = dict()
    for worker in workers:
        result[worker.worker_name] = ('active' if worker.is_active else 'inactive'), worker.last_active_time

    return [{'worker_name': key, 'status': val[0], 'last_active_time': val[1]} for key, val in result.items()]


@celery.task
def update_worker_status(worker_name):
    from strataprop_server.v1.models.celery_workers_status_info import CeleryWorkersStatusInfo
    try:
        obj = CeleryWorkersStatusInfo.query.filter_by(worker_name=worker_name).first()
        if not obj:
            app.logger.info("No record found for worker_name: {}".format(worker_name))
            return "Failed"
        obj.is_active = True
        obj.last_active_time = round(time.time() * 1000)
        db.session.commit()
        return "Success"
    except:
        import traceback
        app.logger.error("Error in updating celery worker status")
        app.logger.error(traceback.print_exc())
        return "Failed"


@celery.task
def check_all_celery_workers():
    from strataprop_server.v1.models.celery_workers_status_info import CeleryWorkersStatusInfo

    # CeleryWorkersStatusInfo.query.update({'is_active': False}, synchronize_session=False)
    # db.session.commit()

    workers = CeleryWorkersStatusInfo.query.all()
    for worker in workers:
        update_worker_status.apply_async(
            queue=worker.worker_name,
            routing_key=worker.worker_name,
            args=[worker.worker_name]
        )
    return "Assigned task to all celery workers"
