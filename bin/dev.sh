#!/bin/sh

main() {
	(
		celerycam.sh > "$PROJECT_LOG/celery_cam.log" &
	)
	(
		runserver_plus.sh > "$PROJECT_LOG/runserver_plus.log" &
	)
	(
		worker.sh > "$PROJECT_LOG/worker.log" &
	)
}

main
sleep 10
# enable events
celery control enable_events
