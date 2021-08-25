# communitiy-discussion
SPA assignment 1

The community-discussion (c18n) is a PoC app to demonstrate the use of streaming technologies
to provide a community chat and discussion platform.

### Components

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

#### Streaming

Kafka

User facing backend servers redirect the input events to a Kafka server, multiple subscribers to the Kafka topics can then 
be updated to pick up and process the incoming events. Example workflows may include - 

Notifying all the users of a community about a new post, generating suggestions for users to join a community based on their
interests, Notifying the moderators to approve a post, flagging a post based on reactions / content analysis.
    
Mongo db

Kafka consumers process and persist the events (messages, posts, likes, share) into a mondo database. At present the user info for 
dummy users (generated for demonstration purposes) is also stored in mongo db.
The data stored in mongo db is immutable, any updates to the data is saved a new timestamped records. This persistence serves the data
for batch layer.

S3 / hdfs / GridFS (planned)

Media files attached with the posts / messages are saved on a distributed storage layer.
For the PoC, all the image and video files are < 16MB in size, that can be saved as a FileField in the mongo db itself.


Spark streaming

Spark streaming serves for the speed layer of the lambda architecture. It generates the real time view and also pushes the 
processed event data to redis cache.


Apache Spark

Apache Spark is used to process batch data and generate batch views.
For the PoC, the batch layer is not yet implemented in absence of any heavy analytical processing.

The overall architecture resembles more to the kappa architecture, with speed layer processing event in mini-batches at 1 second intervals.

Elastic Search / Kibana

The spark streaming layer processes the events, and transforms / dumps the data to elastic search.
Along with kibana dashboard, it is used as a dashboard to serve the analytics platform.

Redis (planned)

A cache server stores a subset of the incoming events (user auth / post / message content) and provides quicker access to the
recently generaed content.
Not implmented in PoC.

Graph db (to be explored)

For user interaction workflows, user connections it may be worth to introduce a graph db.

Analytics dashboard (kibana)
For the PoC, kibana is used to work on elasticsearch indexes, and provides a high level view of various events.
Users of the analytics dashboard can see the various events and associated data.
For the PoC, the analytics dashboard does not have any authentication in place, this can be implemented if time permits.

