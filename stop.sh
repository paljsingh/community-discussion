#!/bin/bash
red='\033[1;31m'
green='\033[1;32m'
default='\033[0m'

_kill_with_exit_status() {
  if [ $# -ne 1 ]; then
    echo "needs process-name or string"
    exit 1
  fi
  kill -9 $(ps -ef | grep "$1" | grep -v grep | awk 'BEGIN{status=1} { print $2; status=0 } END{exit status}') 2>/dev/null
}

stop_backend() {
  printf "%-40s" "stopping backend flask servers ... " && \
    _kill_with_exit_status 'community-discussion/venv/bin/flask' && \
    printf "$green%10.10s$default\n" "[ OK ]" || printf "$red%10.10s$default\n" "[ FAILED ]"

  printf "%-40s" "stopping backend chat server ..." && \
    _kill_with_exit_status 'chat/app.py' && \
    printf "$green%10.10s$default\n" "[ OK ]" || printf "$red%10.10s$default\n" "[ FAILED ]"
}

stop_frontend() {
  printf "%-40s" "stopping frontend node server ... " && \
    _kill_with_exit_status 'community-discussion/frontend/node_modules/.bin/vue-cli-service' && \
    printf "$green%10.10s$default\n" "[ OK ]" || printf "$red%10.10s$default\n" "[ FAILED ]"
}


_stop_service() {
  if [ $# -eq 0 ]; then
    return
  fi

  printf "%-40s" "stopping $1 service ... " && \
    docker stop $1 2>/dev/null && \
    printf "$green%10.10s$default\n" "[ OK ]" || printf "$red%10.10s$default\n" "[ FAILED ]"
}

stop_mongo() {
  _stop_service "mongo"
}

stop_kafka() {
  _stop_service "kafka"
  _stop_service "zookeeper"
}

stop_spark() {
  _stop_service "spark-master"
  _stop_service "spark-worker"
}

stop_logs() {
  printf "%-40s" "stopping logs ... " && \
    _kill_with_exit_status 'logs/c18n.log' && \
    printf "$green%10.10s$default\n" "[ OK ]" || printf "$red%10.10s$default\n" "[ FAILED ]"

}

if [ $# -eq 1 -a "$1" = '-h' ]; then
  cat <<EOF
usage
$0
  stop all the components.

$0 component [component] ... 
  stop only the given component(s)

  components can be one of:
  mongo
  kafka
  spark
  backend
  frontend
EOF
exit 0
fi

case $# in
  0)
    stop_kafka
    stop_spark
    stop_mongo
    stop_backend
    stop_frontend
    stop_logs
    ;;
  *)
    for i in $@ ; do
      stop_$i
    done
  ;;
esac
