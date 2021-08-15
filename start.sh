#!/bin/bash

run_kafka() {
  echo "creating docker network"
  network="kafka-network"
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
      -e KAFKA_CFG_ZOOKEEPER_CONNECT=zookeeper-server:2181 \
      -e KAFKA_CFG_ADVERTISED_LISTENERS=PLAINTEXT://localhost:9092 \
      -p 9092:9092 \
      bitnami/kafka:latest
  fi
}

run_mongo() {
  echo "starting mongo db"
  if ! docker ps -a | grep mongo; then
    docker run --name mongo --rm -d \
      --network $network \
      -p 27017:27017 -p 28017:28017 \
      -v $PWD/data:/data/db \
      -v $PWD/config:/data/configdb \
      xemuliam/mongo
  fi

  sleep 5
  # also create text indexes
  echo 'db.user.createIndex({name: "text"})' | mongo c18n
  echo 'db.community.createIndex({name: "text", tags: "text"})' | mongo c18n
  echo 'db.usergroup.createIndex({name: "text"})' | mongo c18n
  echo 'db.post.createIndex({content: "text"})' | mongo c18n
  echo 'db.comment.createIndex({content: "text"})' | mongo c18n

}

declare -a components=("users" "communities" "usergroups" "posts")
run_backend() {

  flask_run_port=${FLASK_RUN_PORT:-5000}
  flask_env=${FLASK_ENV:-development}

  for i in ${components[@]}; do
    cd "backend/$i" 1>/dev/null
    echo "running backend component '$i' on port $flask_run_port ..."
    FLASK_ENV=$flask_env FLASK_RUN_PORT=$flask_run_port FLASK_APP=app.py flask run 2>&1 1>/dev/null &
    flask_run_port=$(expr $flask_run_port + 1)
    cd - 1>/dev/null
  done

  export WEBSOCKET_PORT=${WEBSOCKET_PORT:-5010}
  cd backend/chat
  python3 app.py 2>&1 1>/dev/null &
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

source $PWD/venv/bin/activate
run_kafka
run_mongo
run_backend
run_frontend
tail_logs
