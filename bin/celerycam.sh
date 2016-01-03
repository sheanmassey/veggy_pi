#!/bin/sh

nohup python $PROJECT_HOME/manage.py celerycam &
printf "celerycam_pid: $!\n" >> "$PID_FILE"
