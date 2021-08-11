#!/bin/bash

# setup virtualenv and python dependencies.
virtualenv venv
source venv/bin/activate
pip3 install -r requirements.txt

# pull kafka/zookeeper images
docker pull bitnami/zookeeper:latest
docker pull bitnami/kafka:latest


