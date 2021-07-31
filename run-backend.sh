#!/bin/bash

declare -a components=("users" "usergroups")

flask_run_port=${FLASK_RUN_PORT:-5000}
flask_env=${FLASK_ENV:-development}

log_files=""
for i in ${components[@]}; do
  cd "backend/$i" 1>/dev/null
  echo "running backend component '$i' on port $flask_run_port ..."
  FLASK_ENV=$flask_env FLASK_RUN_PORT=$flask_run_port FLASK_APP=app.py flask run &
  flask_run_port=$(expr $flask_run_port + 1)
  log_files="$log_files backend/$i/logs/c18n.log"
  cd - 1>/dev/null
done

export WEBSOCKET_PORT=${WEBSOCKET_PORT:-5010}
cd backend/chat
python3 app.py &
cd - 1>/dev/null
log_files="$log_files backend/chat/logs/c18n.log"

tail -F $(echo $log_files)
