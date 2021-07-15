#!/bin/bash
declare -a components=("users")

flask_run_port=${FLASK_RUN_PORT:-5000}
flask_env=${FLASK_ENV:-development}
for i in ${components[@]}; do
  cd "backend/$i" 1>/dev/null
  echo "running backend component '$i' on port $flask_run_port ..."
  FLASK_ENV=$flask_env FLASK_RUN_PORT=$flask_run_port FLASK_APP=app.py flask run &
  flask_run_port=$(expr $flask_run_port + 1)
  cd - 1>/dev/null
done
