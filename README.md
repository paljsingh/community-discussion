*DISCLAIMER - before you clone this repo*

## The Project got me 3 / 15 marks.

*You have been warned !*

---

## Community Discussion

The community-discussion (c18n) is a PoC app to demonstrate the use of streaming technologies
to provide a community chat and discussion platform.


## Features

- A Vue.js app for the UI
- Python/Flask server endpoints for users, communities, usergroups apis
- Third party authentication with okta
- Custom user authentication with JWT tokens
- Websocket based chat server with flask-socketio
- Fake data generation via Faker
- Streaming pipeline making use of Apache Kafka, Spark+pyspark, Elasticsearch
- Analytics portal via Kibana
- Preconfigured dashboards and Elasticsearch integration with Kibana
- Kafka producers and consumers
- Spark streaming scripts
- Distributed database storage using mongo db
- Video and Image upload ability
- UI interface for viewing user posts, images and videos
- UI chatroom interface using vue-advanced-chat
- Scripts for emulating various workflows like user/community/usergroup creation, user content creation etc.
- Extensible, Configurable setup for streaming pipeline
- Scripts for easy setup/teardown/start/stop of services
- Lightweight, minimal configuration for each of the services to run everything on a single node
- Closely follows kappa architecture
- 


## Demo Vidoes

1/2

[![Part 1 of 2](https://img.youtube.com/vi/SEgkeIV7R-g/0.jpg)](https://www.youtube.com/watch?v=SEgkeIV7R-g&list=PLHpNd3jR1FMYORmWIwEz2EUgYofL-O1Ps&index=3)

2/2

[![Part 2 of 2](https://img.youtube.com/vi/8DpjFNXka5E/0.jpg)](https://www.youtube.com/watch?v=8DpjFNXka5E&list=PLHpNd3jR1FMYORmWIwEz2EUgYofL-O1Ps&index=4)



## Components

#### Frontend
    
The frontend makes use of Vue single page application pattern.
The frontend is subdivided into various Vue components - Users, UserGroups, Communities, Dashboard, Profile(user profile)
and other reusable components for messaging and search.
It also intregrates with okat single sign-on to provide user authentication.

#### Backend

Various backend web services provide apis for creating Users, UserGroups, Communities are written using the
Python/Flask web server.
The backend apis provide a rest based api interface to the frontend applications.

Other heavy usage workflows like messaging, like, share are implemented using websocket apis, which allows
the server to notify the frontend apps for any new updates.

#### Streaming (Kafka)

User facing backend servers redirect the input events to a Kafka server, multiple subscribers to the Kafka topics can then 
be updated to pick up and process the incoming events. Example workflows may include - 

Notifying all the users of a community about a new post, generating suggestions for users to join a community based on their
interests, Notifying the moderators to approve a post, flagging a post based on reactions / content analysis.
    
#### Mongo db

Kafka consumers process and persist the events (messages, posts, likes, share) into a mondo database. At present the user info for 
dummy users (generated for demonstration purposes) is also stored in mongo db.
The data stored in mongo db is immutable, any updates to the data is saved a new timestamped records. This persistence serves the data
for batch layer.

#### S3 / hdfs (planned)

Media files attached with the posts / messages are saved on a distributed storage layer.
For the PoC, images / videos are saved locally using GridFS support.


#### Spark streaming

Spark streaming serves for the speed layer of the lambda architecture. It generates the real time view and also pushes the 
processed event data to redis cache.


#### Apache Spark (TBD)

Apache Spark shall be used to process batch data and generate batch views.
For the PoC, the batch layer is not yet implemented in absence of any heavy analytical processing.

The overall architecture resembles more to the kappa architecture, with speed layer processing event in mini-batches at 5 second intervals.

#### Elastic Search

The spark streaming layer processes the events, and transforms / dumps the data to elastic search.

#### Analytics dashboard (kibana)
An analytics Dashboard is served via Kibana.  

Users of the analytics dashboard can see the various events and associated data.  
For the PoC, the analytics dashboard does not have any authentication in place, this can be implemented later if time permits.


#### Redis (TBD)

A cache server stores a subset of the incoming events (user auth / post / message content) and provides quicker access to the
recently generaed content.  
[Not implemented in PoC.]

#### Graph db (to be explored)

For user interaction workflows, user connections it may be worth to introduce a graph db.


