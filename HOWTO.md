## Pre-requisites

> python 3.7+  
> node v15.x  
> yarn v1.22.x
  docker-desktop 3.5+

## Clone Repo

> $ git clone https://github.com/paljsingh/community-discussion.git  
> $ cd community-discussion

## Install / Run

Tested on OSX 11.5.2 with  
> python v3.9.2  
> node v15.11.0  
> yarn v1.22.5  
  docker-desktop 3.5.2

---

Installation

$ ./setup.sh

This will -
    - pull the docker images for 
      - kafka
      - zookeeper
      - mongo db
      - spark
      - elasticsearch

    also, 
    - install python dependencies for the backend services
    - install node / vue.js dependencies for the frontend service.
    - set up data, config and log directories for the applications.
    - download additional jars for spark/kafka and spark/elasticsearch integration.

---

Run

$ ./start.sh

This will - 

    - Create a docker network
    - Run zookeeper
    - Run Kafka
      - create kafka topics
    - Run mongo db
      - create indexes for mongo collections for text based search.
    - Run spark (master and worker nodes)
    - Run elasticsearch
    - Run flask server for each of the backend services
    - Run flask/websocket application
    - Run frontend vue.js server
    - Tail the logs for all the components

One can also start a single component as:

./start.sh [kafka|mongo|spark|backend|frontend]

---

UI

Visit <http://localhost:8080>

Login as admin by using the okta login link.
To obtain admin token, Go to Profile link -> Admin JWT Token
or
copy it from Developer Tools -> Application -> Local Storage -> http://localhost:8080/ -> okta-token-storage -> accessToken -> accessToken

Admin users can copy the JWT tokens of other users by visiting the users tab, and clicking on the 'Copy Token' button for one of the users.

Another incognito windows (or a new firefox/chrome profile) can be used to impersonate / login as a non-admin user, by pasting their JWT token on the login page.

Users can view other users, view/create communities, create usergroups or chat with other users.


Caveat:
    - All the incognito windows in Firefox/Chrome share the user cookies/tokens, so it is not possible to open multiple incognito windows to impersonate multiple users.
    One can however, 
      - Create a new chrome/firefox profile and impersonate 2 new users (1 with incognito window, 1 with non-incognito window of the new profile)
      - Use another browser

---

Spark Speed / Batch processing

In another terminal, run
python3 ./start.sh sparkspeed
python3 ./start.sh sparkbatch

These will launch the spark speed and batch job, which display the incoming flow of events on console as well as dumps it to elasticsearch.

---
Generate random requests to create users, communities, posts etc.

export ADMIN_TOKEN='jwt-token-of-the-admin-user'
python3 scripts/chaos.py
or
python3 scripts/chaos.py 1000

The script above creates a total of given number of resources (100 if no arguments specified). The resources can be one of - 
users
communities
usergroups
text posts
image posts
video posts

The distribution of number of resources of each type are controlled by the configs defined in scripts/etc/chaos.yaml

For creating the users, admin jwt token is used.
All the other requests use a random non-admin user's JWT token to simulate cases like:

- users creating a community
- users creating user groups and adding other users to it.
- users posting text / image / video content to the communities

---
Status

$ ./status.sh 
or
./status.sh [mongo|kafka|spark|backend|frontend]

---

Stop services

$ ./stop.sh 
or
./stop.sh [mongo|kafka|spark|backend|frontend]

---


