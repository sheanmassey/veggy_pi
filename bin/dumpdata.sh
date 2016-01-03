#!/bin/sh

# output directory is relative to the PATH of the manage.py command
$PROJECT_HOME/manage.py dumpdata veggy_pi.RPiPin --format=json -o veggy_pi/fixtures/RPi/rpi_pin.json
$PROJECT_HOME/manage.py dumpdata veggy_pi.RpiPin --format=yaml -o veggy_pi/fixtures/RPi/rpi_pin.yaml
