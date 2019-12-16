from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from strataprop_server import app, db, celery
from strataprop_server.v1.employee import employee_blueprint
from strataprop_server.v1.device import device_blueprint
from subprocess import call


migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

app.register_blueprint(employee_blueprint)
app.register_blueprint(device_blueprint)
celery.conf.update(app.config)

@manager.command
def runserver():
    """ overriding the runserver command
    """
    app.run(host='0.0.0.0', port=8000, debug=True)

if __name__ == '__main__':
    try:
        manager.run()
    except StopIteration:
        app.logger.info("error")
