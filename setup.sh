#!/bin/bash

# setup virtualenv and python dependencies.
virtualenv venv
source venv/bin/activate
pip3 install -r backend/requirements.txt

# pull kafka/zookeeper images
docker pull bitnami/zookeeper:latest
docker pull bitnami/kafka:latest

# pull mongodb (image with gridfs support)
docker pull xemuliam/mongo:latest

# pull apache spark image
docker pull bitnami/spark:latest

# pull elastic search image
docker pull docker.elastic.co/elasticsearch/elasticsearch:7.14.0

# setting up yarn packages
cd frontend ; yarn install ; cd - 1>/dev/null

# setting up directories
mkdir -p var/data/{mongo,kafka,spark,images,videos} var/config/{mongo,kafka,spark}
for i in backend/{users,usergroups,communities,posts,chat} ; do
  mkdir $i/logs
  touch $i/logs/c18n.log
done
