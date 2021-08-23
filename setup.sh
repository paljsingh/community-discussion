#!/bin/bash

# setup virtualenv and python dependencies.
virtualenv venv
source venv/bin/activate
pip3 install -r requirements.txt

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

# extra jars for spark/kafka integration
mkdir var/data/spark/jars
curl https://repo1.maven.org/maven2/org/apache/spark/spark-sql-kafka-0-10_2.12/3.0.1/spark-sql-kafka-0-10_2.12-3.0.1.jar --output var/data/spark/jars/spark-sql-kafka-0-10_2.12-3.0.1.jar
curl https://repo1.maven.org/maven2/org/apache/spark/spark-token-provider-kafka-0-10_2.12/3.0.1/spark-token-provider-kafka-0-10_2.12-3.0.1.jar --output var/data/spark/jars/spark-token-provider-kafka-0-10_2.12-3.0.1.jar
curl https://repo1.maven.org/maven2/org/apache/spark/spark-streaming-kafka-0-10-assembly_2.12/3.0.1/spark-streaming-kafka-0-10-assembly_2.12-3.0.1.jar --output var/data/spark/jars/spark-streaming-kafka-0-10-assembly_2.12-3.0.1.jar
curl https://repo1.maven.org/maven2/org/apache/spark/spark-tags_2.12/3.0.1/spark-tags_2.12-3.0.1.jar --output var/data/spark/jars/spark-tags_2.12-3.0.1.jar
curl https://repo1.maven.org/maven2/org/apache/kafka/kafka-clients/2.4.1/kafka-clients-2.4.1.jar --output var/data/spark/jars/kafka-clients-2.4.1.jar
curl https://repo1.maven.org/maven2/org/apache/commons/commons-pool2/2.6.2/commons-pool2-2.6.2.jar --output var/data/spark/jars/commons-pool2-2.6.2.jar

# for elasticsearch
curl https://repo1.maven.org/maven2/org/elasticsearch/elasticsearch-spark-20_2.10/7.14.0/elasticsearch-spark-20_2.10-7.14.0.jar --output var/data/spark/jars/elasticsearch-spark-20_2.10-7.14.0.jar

# spark warehouse
mkdir spark-warehouse
