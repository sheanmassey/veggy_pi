#!/bin/sh

CWD="`basename ${0%/*}`"
PROJECT_BASE="$(dirname "$CWD")"

PROJECT_HOME="$PROJECT_BASE/www"
PROJECT_BIN="$PROJECT_HOME/bin"
PROJECT_LOG="$PROJECT_HOME/log"
PID_FILE="$PROJECT_LOG/pid.lck"
PATH="$PATH:$PROJECT_BIN"
DJANGO_SETTINGS_MODULE=www.settings
export DJANGO_SETTINGS_MODULE CWD PROJECT_BASE PROJECT_HOME PROJECT_BIN PATH PROJECT_LOG PID_FILE