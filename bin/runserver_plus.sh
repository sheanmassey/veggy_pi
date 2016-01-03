#!/bin/sh

nohup python $PROJECT_HOME/manage.py runserver_plus &
printf "runserver_plus: $!\n" >> "$PID_FILE"
