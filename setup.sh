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

# setting up yarn packages
cd frontend ; yarn install ; cd - 1>/dev/null
