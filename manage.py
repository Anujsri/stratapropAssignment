import os
import time
import tempfile
import shutil

from flask import g, request, abort, url_for
# from strataprop_server.v1.auth.functions import get_current_user
# from strataprop_server.v1.common.exceptions import UnKnownException
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager, prompt_bool
from strataprop_server import app, db, celery
from strataprop_server.v1.employee import employee_blueprint
from strataprop_server.v1.device import device_blueprint
from strataprop_server.v1.celery_monitoring import celery_monitoring_blueprint
from strataprop_server.v1.common.exceptions import UnKnownException
from subprocess import call


migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

migrate_flag = os.path.join(tempfile.gettempdir(), "MIGRATION_FLAG")
migrate_file_flag = os.path.join(tempfile.gettempdir(), "MIGRATE")
workers_flag = os.path.join(tempfile.gettempdir(), "WORKERS_FLAG")

def file_put_contents(self,file_name,contents='',mode='w'):
    try:
        with open(file_name, mode) as f:
            f.write(contents)
            return True
    except:
        return False

def do_migrate():
    try:
        use_by = time.time() - 120
        if os.path.exists(migrate_flag) and os.path.getatime(migrate_flag) < use_by:
            os.remove(migrate_flag)
        if not os.path.exists(migrate_flag):
            file_put_contents(migrate_flag,'')
            if os.path.exists(migrate_file_flag):
                app.logger.info("----------------running migrations-----------------")
                migration_upgrade = True
                migration_downgrade = False
                migration_migrate = True
                os.remove(migrate_file_flag)
            else:
                migration_upgrade = False
                migration_downgrade = False
                migration_migrate = False
            run_once = os.path.join(tempfile.gettempdir(), 'RUN_ONCE')
            if os.path.exists(run_once):
                migrations_versions = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'migrations','versions')
                migrations_versions_backup = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'migrations', 'versions_backup')
                if os.path.exists(migrations_versions):
                    shutil.rmtree(migrations_versions)
                    os.makedirs(migrations_versions)
                if os.path.exists(migrations_versions_backup):
                    shutil.rmtree(migrations_versions_backup)
                    os.makedirs(migrations_versions_backup)
            if not os.path.isdir(os.path.join(os.getcwd(), 'migrations')):
                call(["python", "manage.py", "db", "init"])
            if migration_migrate:
                call(["python", "manage.py", "db", "migrate"])
                modify_alembic_versions()
            if migration_upgrade:
                call(["python", "manage.py", "db", "upgrade"])
            if migration_downgrade:
                call(["python", "manage.py", "db", "downgrade"])
            if os.path.exists(run_once):
                time.sleep(10)
            
    except UnKnownException:
        app.logger.info("___in upgrade exception__")
        import traceback
        app.logger.info(traceback.print_exc())


do_migrate()

app.register_blueprint(employee_blueprint)
app.register_blueprint(device_blueprint)
app.register_blueprint(celery_monitoring_blueprint)
celery.conf.update(app.config)


@app.before_first_request
def clear_migration_flag():
    if os.path.isfile(migrate_flag):
        os.remove(migrate_flag)


# @app.before_request
# def before_request():
#     if not request.endpoint:
#         abort(404)
#     g.user = get_current_user()


# @app.after_request
# def add_cors_headers(response):
#     from strataprop_server.v1.common.functions import unauthorized_view
#     # org_ob = OrganizationDetails.query.first()
#     # org_url = org_ob.org_server if org_ob else ''
#     # r = request.headers.get('Origin') or org_url or 'org_url_unset'
#     white_listed_origins = ['http://frontend.loktra.com','http://0.0.0.0:8000']
#     # if r not in white_listed_origins:
#         # return unauthorized_view()
#     # response.headers.add('Access-Control-Allow-Origin', r)
#     response.headers.add('Access-Control-Allow-Credentials', 'true')
#     if r == 'http://frontend.loktra.com':
#         response.headers.add('Access-Control-Allow-Methods', 'GET, POST, OPTIONS, PUT, DELETE')
#         requested_headers = (request.headers.get('Access-Control-Request-Headers') or '').split(',')
#         for header in requested_headers:
#             response.headers.add('Access-Control-Allow-Headers', header.capitalize())

#     return response


@manager.command
def runserver():
    """ overriding the runserver command
    """
    app.run(host='0.0.0.0', port=8000, debug=True)


@manager.command
def drop_all():
    """Drops database tables"""
    if prompt_bool("Are you sure you want to lose all your data"):
        db.drop_all()


@manager.option('--bind', help='Specify Bind')
def create_all(bind):
    """Creates database tables"""
    db.create_all(bind=bind)


if __name__ == '__main__':
    try:
        manager.run()
    except StopIteration:
        app.logger.info("error")
    


def has_no_empty_params(rule):
    defaults = rule.defaults if rule.defaults is not None else ()
    arguments = rule.arguments if rule.arguments is not None else ()
    return len(defaults) >= len(arguments)


@app.route("/site-map")
def site_map():
    import json
    links = []
    for rule in app.url_map.iter_rules():
        # Filter out rules we can't navigate to in a browser
        # and rules that require parameters
        if "GET" in rule.methods and has_no_empty_params(rule):
            url = url_for(rule.endpoint, **(rule.defaults or {}))
            links.append((url, rule.endpoint))
    # links is now a list of url, endpoint tuples
    app.logger.info(links)
    return json.dumps(links)
