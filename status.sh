#!/bin/bash
red='\033[1;31m'
green='\033[1;32m'
default='\033[0m'

_ps_status() {
  if [ $# -ne 1 ]; then
    echo "needs process-name or string"
    exit 1
  fi
  ps -ef | grep "$1" | grep -v grep | awk 'BEGIN{status=1} { print $2; status=0 } END{exit status}' &>/dev/null && \
    printf "$green%20.20s$default\n" "[ RUNNING ]" || printf "$red%20.20s$default\n" "[ NOT RUNNING ]"
}

backend_status() {
  printf "%-40s" "backend flask servers ... " && \
    _ps_status 'community-discussion/venv/bin/flask'

  printf "%-40s" "backend chat server ..." && \
    _ps_status 'chat/app.py'
}

frontend_status() {
  printf "%-40s" "frontend node server ... " && \
    _ps_status 'community-discussion/frontend/node_modules/.bin/vue-cli-service'
}


_docker_service_status() {
  if [ $# -eq 0 ]; then
    return
  fi
  printf "%-40s" "$1 service ... " && \
    docker ps -a | grep -q $1 && \
    printf "$green%20.20s$default\n" "[ RUNNING ]" || printf "$red%20.20s$default\n" "[ NOT RUNNING ]"
}

mongo_status() {
  _docker_service_status "mongo"
}

kafka_status() {
  _docker_service_status kafka
  _docker_service_status zookeeper
}

spark_status() {
  _docker_service_status "spark-master"
  _docker_service_status "spark-worker"
}

sparkbatch_status() {
  printf "%-40s" "spark batch ... " && \
    _ps_status 'spark-batch'
}

sparkspeed_status() {
  printf "%-40s" "spark speed ... " && \
    _ps_status 'spark-speed'
}
elasticsearch_status() {
  _docker_service_status 'elasticsearch'
}

logs_status() {
  printf "%-40s" "logs ... " && \
    _ps_status 'logs/c18n.log'

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
  sparkspeed
  sparkbatch
  elasticsearch
  backend
  frontend
  logs
EOF
exit 0
fi

case $# in
  0)
    kafka_status
    spark_status
    sparkbatch_status
    sparkspeed_status
    mongo_status
    elasticsearch_status
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
