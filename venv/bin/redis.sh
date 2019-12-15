#!/bin/bash
NAME="redis"
PROJECT_DIR=~/Desktop/stratapropAssignment
cd $PROJECT_DIR
source ~/Desktop/backend/venv/bin/activate
export PYTHONPATH=$PROJECT_DIR:$PYTHONPATH
# set environment
export LANG=en_US.UTF-8
export LC_MESSAGES="C"
export REDIS_URL="redis://localhost:6379/0"
exec redis-server
