#!/bin/sh

nohup celery -A veggy_pi.tasks worker --loglevel=info &
echo "worker_pid: $!" >> "$PID_FILE"
