#!/bin/bash

cat << EOF
WARNING WARNING WARNING

Running this script will: 
- delete "$PWD/var/" folder containing all docker configurations/data related to
  kafka
  zookeeper
  mongo
  spark
  elsticsearch
  kibana
- delete "$PWD/frontend/node_modules" folder containing node.js packages for c18n
- delete "$PWD/venv/" folder containing python dependencies for c18n.
- delete all "c18n.log" log files found under $PWD/
- delete kafka/zookeeper/mongo/elasticsearch/kibana/spark docker images.
- delete docker network 'c18n-network'
- delete __pycache__ directories.
- delete data/gridfs/{images,videos}/* , that were created when uploading images and videos.

YOU HAVE BEEN WARNED!

Type "yes" to continue -
EOF

read x 
if [ "$x" = "yes" ]; then
  rm -rf "$PWD/var/"
  rm -rf "$PWD/frontend/node_modules"
  rm -rf "$PWD/venv"
  find "$PWD" -type f -name "c18n.log*" | xargs rm

  docker stop mongo zookeeper kafka spark elaasticsearch kibana
  docker rmi \
    bitnami/zookeeper:latest \
    bitnami/kafka:latest \
    xemuliam/mongo:latest \
    bitnami/spark:latest \
    docker.elastic.co/elasticsearch/elasticsearch:7.14.0 \
    kibana:7.14.0 
    docker network rm c18n-network
fi

find . -type d -name "__pycache__" -exec rm -rfv {} \;
rm -rf data/gridfs/images/* data/gridfs/videos/*


