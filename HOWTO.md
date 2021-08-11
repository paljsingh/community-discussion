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


Setup a kubernetes cluster
In Docker preferences -> Kubernetes -> Enable Kubernetes

Ensure docker-desktop is the default context.


Mongo db
> $ brew install mongodb-community  
> $ brew install mongodb-database-tools  
> $ mongod -f /usr/local/etc/mongod.conf  

---

Installation

$ ./setup.sh

This will -
- pull the docker images for kafka and zookeeper
- install python dependencies for the backend services
- install node / vue.js dependencies for the frontend service.

---

Run

$ ./run.sh

This will - 

- Create a docker network
- Run zookeeper
- Run Kafka
- Run flask server for each of the backend services
- Run flask/websocket application
- Run frontend vue.js server
- Tail the logs for all the components

---

Visit <http://localhost:8080>
