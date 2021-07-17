## Pre-requisites

> python 3.7+  
> node v15.x  
> yarn v1.22.x
> mongodb v4.4.0

## Clone Repo

> $ git clone https://github.com/paljsingh/community-discussion.git  
> $ cd community-discussion

## Install / Run

Tested on OSX 11.4 with  
> python v3.9.2  
> node v15.11.0  
> yarn v1.22.5  
> mongodb v4.4.0

#### Install Components  

Mongo db
> $ brew install mongodb-community  
> $ brew install mongodb-database-tools  
> $ mongod -f /usr/local/etc/mongod.conf  

Apache Kafka

Apache Storm

Kafka Streams

Mongo gridfs

Elastic Search

Redis

#### Run Backend

> $ ./run-backend.sh  
> $ tail -F backend/users/logs/c18n.log  

#### Run Frontend

> $ cd frontend && yarn install && yarn start  
> 

Visit <http://localhost:8080>