#!/bin/bash
NAME="celery"                                           # Name of the application
PROJECT_DIR=~/Desktop/stratapropAssignment
SOCKFILE=/Users/anuj/Desktop/stratapropAssignment/venv/bin/gunicorn.sock  # we will communicte using this unix socket
USER=anuj
GROUP=anuj
NUM_WORKERS=5                                     # how many worker processes should Gunicorn spawn
FLASK_APP=manage                     # WSGI module name
#FLASK_SOCKET=flask_sockets
FLASK_SOCKET=gevent
echo "Starting $NAME as `whoami`"



# Activate the virtual environment
cd $PROJECT_DIR
source venv/bin/activate
export PYTHONPATH=$PROJECT_DIR:$PYTHONPATH
# set environment
export LANG=en_US.UTF-8
export LC_MESSAGES="C"
# Example aliases
# alias zshconfig="mate ~/.zshrc"
# alias ohmyzsh="mate ~/.oh-my-zsh"
export C_FORCE_ROOT="true"
export APP_KEY='BYTa4u9d-dsc8GM1LtnQEjs9RZVgZzRGyPQ2bMQw'
export APP_SETTINGS="config.ProductionConfig"
export SECURITY_PASSWORD_HASH='pbkdf2_sha512'
export SECURITY_PASSWORD_SALT='poiuytresdfghjkloiuytrescvbnml;p98765rdcvbnmloiuytr'
export MAIL_USERNAME='hello@loktra.com'
export MAIL_PASSWORD='LoktraTesting'
export DATABASE_NAME='assignment'
export DATABASE_USER='anuj'
export DATABASE_PASSWORD='anuj1234'
export DATABASE_HOST='localhost'
export PGPASSWORD=$DATABASE_PASSWORD
export DATABASE_URL="postgresql://anuj:anuj1234@localhost:5432/assignment"
export REDIS_URL='redis://localhost:6379/0'
export AMQP_URL='amqp://au_user:au1234@localhost/localhost'
export APP_SECRET_KEY='\xb5\x1ePn\xc7\n\xcd\x96C\xc6\xa8\x05\xe9\x7fF\x8fz\xa1\x19\x17\x19\x10g\x85'

# Create the run directory if it doesn't exist
# Start your Django Unicorn
# Programs meant to be run under supervisor should not daemonize themselves (do not use --daemon)
# exec celery worker -A manage.celery --loglevel=info --concurrency=1 --beat
exec celery worker --app=manage.celery --concurrency=1 --loglevel=INFO --queues=default -l info --beat  -n workerA

