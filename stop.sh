#!/bin/bash
red='\033[1;31m'
green='\033[1;32m'
default='\033[0m'
printf "%-40s" "stopping backend flask servers ... " && \
  ps -ef | grep community-discussion/venv/bin/flask | grep -v grep | awk '{ print $2 }' | xargs kill -9 && \
  printf "$green%10.10s$default\n" "[ OK ]" || printf "$red%10.10s$default\n" "[ FAILED ]"

printf "%-40s" "stopping backend chat server ..." && \
  ps -ef | grep chat/app.py | grep -v grep | awk '{ print $2 }' | xargs kill -9 && \
  printf "$green%10.10s$default\n" "[ OK ]" || printf "$red%10.10s$default\n" "[ FAILED ]"

printf "%-40s" "stopping frontend node server ... " && \
  ps -ef | grep community-discussion/frontend/node_modules/.bin/vue-cli-service | grep -v grep | awk '{ print $2 }' | xargs kill -9 && \
  printf "$green%10.10s$default\n" "[ OK ]" || printf "$red%10.10s$default\n" "[ FAILED ]"

for service in mongo zookeeper kafka; do
  printf "%-40s" "stopping $service service ... " && \
    docker stop $service && \
    printf "$green%10.10s$default\n" "[ OK ]" || printf "$red%10.10s$default\n" "[ FAILED ]"
done
