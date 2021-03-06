#!/bin/bash

network="c18n-network"
run_kafka() {
  echo "creating docker network"
  if ! docker network inspect $network &>/dev/null; then
      docker network create $network --driver bridge
  fi

  echo "starting zookeeper"
  if ! docker ps -a | grep zookeeper; then
    docker run --rm -d --name zookeeper \
      -p 2181:2181 \
      --network $network \
      -e ALLOW_ANONYMOUS_LOGIN=yes \
      bitnami/zookeeper:latest 
  fi

  echo "starting kafka"
  if ! docker ps -a | grep kafka; then
    docker run --rm -d --name kafka \
      --network $network \
      -e ALLOW_PLAINTEXT_LISTENER=yes \
      -e KAFKA_CFG_ZOOKEEPER_CONNECT=zookeeper:2181 \
      -e KAFKA_CFG_ADVERTISED_LISTENERS=PLAINTEXT://localhost:9092 \
      -p 9092:9092 \
      bitnami/kafka:latest
  fi

  echo "creating kafka topics"
  sleep 10
  python3 scripts/kafka-topics.py create
}

run_mongo() {
  echo "starting mongo db"
  if ! docker ps -a | grep mongo; then
    docker run --name mongo --rm -d \
      --network $network \
      -p 27017:27017 -p 28017:28017 \
      -v $PWD/var/data/mongo:/data/db \
      -v $PWD/var/config/mongo:/data/configdb \
      xemuliam/mongo
  fi

  echo "creating mongo indexes"
  sleep 5
  echo 'db.user.createIndex({name: "text"})' | mongo c18n 1>/dev/null
  echo 'db.community.createIndex({name: "text", tags: "text"})' | mongo c18n 1>/dev/null
  echo 'db.usergroup.createIndex({name: "text"})' | mongo c18n 1>/dev/null
  echo 'db.post.createIndex({content: "text"})' | mongo c18n 1>/dev/null
  echo 'db.comment.createIndex({content: "text"})' | mongo c18n 1>/dev/null

}

run_elasticsearch() {
  echo "starting elasticsearch"
  if ! docker ps -a | grep elasticsearch; then
    docker run --name elasticsearch --rm -d \
      --net $network \
      -p 9200:9200 -p 9300:9300 \
      -e "discovery.type=single-node" \
      docker.elastic.co/elasticsearch/elasticsearch:7.14.0
  fi
}

run_kibana() {
  echo "starting kibana"
  if ! docker ps -a | grep kibana; then
    docker run --name kibana --rm -d \
      --net $network \
      -p 5601:5601 \
      docker.io/library/kibana:7.14.0
  fi
}

run_spark() {
  echo "starting spark cluster"
  if ! docker ps -a | grep spark; then
    docker run --rm -d --name spark-master \
      --network=$network \
      -e SPARK_MODE=master \
      -p 7077:7077 \
      -p 7080:8080 \
      bitnami/spark

    docker run --rm -d --name spark-worker \
      --network=$network \
      -e SPARK_MASTER_URL=spark://spark-master:7077 \
      -e SPARK_MODE=worker \
      -p 7081:8081 \
      bitnami/spark
  fi
}

declare -a components=("users" "communities" "posts")
run_backend() {

  flask_run_port=${FLASK_RUN_PORT:-5000}
  flask_env=${FLASK_ENV:-development}

  for i in ${components[@]}; do
    cd "backend/$i" 1>/dev/null
    echo "running backend component '$i' on port $flask_run_port ..."
    FLASK_ENV=$flask_env FLASK_RUN_PORT=$flask_run_port FLASK_APP=app.py flask run &
    flask_run_port=$(expr $flask_run_port + 1)
    cd - 1>/dev/null
  done
}

run_chat() {
  export WEBSOCKET_PORT=${WEBSOCKET_PORT:-5010}
  cd backend/chat
  python3 app.py  &
  cd - 1>/dev/null
}

run_frontend() {
  cd frontend
  yarn install

  yarn_run_mode=${YARN_RUN_MODE:-dev}
  yarn start --mode $yarn_run_mode &
  cd - 1>/dev/null
}

tail_logs() {
  log_files=""
  for i in ${components[@]}; do
    log_files="$log_files backend/$i/logs/c18n.log"
  done
  log_files="$log_files backend/chat/logs/c18n.log"

  echo tail -F $(echo $log_files)
  tail -F $(echo $log_files) &
}

topics="users communities posts images videos usergroups"
run_sparkbatch() {
  for topic in $(echo $topics); do
    python3 scripts/spark-batch.py $topic &
  done
}

run_sparkspeed() {
  for topic in $(echo $topics); do
    echo "starting consumer for topic $topic"
    python3 scripts/spark-speed.py $topic &
    sleep 1
  done
}

source $PWD/venv/bin/activate

if [ $# -eq 1 -a "$1" = '-h' ]; then
  cat <<EOF
usage
$0
  run all the components.

$0 component [component] ... 
  run only the given component(s)

  components can be one of:
  mongo
  kafka
  spark
  sparkspeed
  sparkbatch
  elasticsearch
  kibana
  backend
  chat
  frontend
  logs
EOF
exit 0
fi

case $# in
  0)
    run_kafka
    run_spark
    run_mongo
    run_backend
    run_chat
    run_elasticsearch
    run_kibana
    run_frontend
    tail_logs
    ;;
  *)
    for i in $@ ; do
      run_$i
    done
  ;;
esac
