#!/bin/bash
red='\033[1;31m'
green='\033[1;32m'
default='\033[0m'

_ps_status() {
  if [ $# -ne 1 ]; then
    echo "needs process-name or string"
    exit 1
  fi
  ps -ef | grep "$1" | grep -v grep | awk 'BEGIN{status=1} { print $2; status=0 } END{exit status}' &>/dev/null
}

backend_status() {
  printf "%-40s" "backend flask servers ... " && \
    _ps_status 'community-discussion/venv/bin/flask' && \
    printf "$green%10.10s$default\n" "[ OK ]" || printf "$red%10.10s$default\n" "[ FAILED ]"

  printf "%-40s" "backend chat server ..." && \
    _ps_status 'chat/app.py' && \
    printf "$green%10.10s$default\n" "[ OK ]" || printf "$red%10.10s$default\n" "[ FAILED ]"
}

frontend_status() {
  printf "%-40s" "frontend node server ... " && \
    _ps_status 'community-discussion/frontend/node_modules/.bin/vue-cli-service' && \
    printf "$green%10.10s$default\n" "[ OK ]" || printf "$red%10.10s$default\n" "[ FAILED ]"
}


_docker_service_status() {
  if [ $# -eq 0 ]; then
    return
  fi

  printf "%-40s" "$1 service ... " && \
    docker ps -f name=$1 -q &>/dev/null && \
    printf "$green%10.10s$default\n" "[ OK ]" || printf "$red%10.10s$default\n" "[ FAILED ]"
}

mongo_status() {
  _docker_service_status "mongo"
}

kafka_status() {
  _docker_service_status "kafka"
  _docker_service_status "zookeeper"
}

spark_status() {
  _docker_service_status "spark-master"
  _docker_service_status "spark-worker"
}

logs_status() {
  printf "%-40s" "logs ... " && \
    _ps_status 'logs/c18n.log' && \
    printf "$green%10.10s$default\n" "[ OK ]" || printf "$red%10.10s$default\n" "[ FAILED ]"

}

if [ $# -eq 1 -a "$1" = '-h' ]; then
  cat <<EOF
usage
$0
  status of all the components.

$0 component [component] ... 
  status of only the given component(s)

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
    kafka_status
    spark_status
    mongo_status
    backend_status
    frontend_status
    logs_status
    ;;
  *)
    for i in $@ ; do
      ${i}_status
    done
  ;;
esac
