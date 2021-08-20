import argparse
import os

from kafka import KafkaAdminClient
from kafka.errors import TopicAlreadyExistsError, UnknownTopicOrPartitionError
from kafka.admin import NewTopic
import json
import sys

kac = KafkaAdminClient()


def create_topics(topics=None):
    if not topics:
        abs_path = os.path.abspath(sys.argv[0])
        with open(os.path.join(os.path.dirname(abs_path), "etc/topics.json"), "r") as fh:
            topics_json = json.load(fh)
        topics = [NewTopic(**x) for x in topics_json]
    else:
        topics = [NewTopic(name=x, replication_factor=1, num_partitions=3) for x in topics]

    for topic in topics:
        try:
            kac.create_topics(new_topics=[topic])
            print("topic {} created".format(topic.name))
        except TopicAlreadyExistsError as ex:
            print("topic {} already exists".format(topic.name))


def list_topics(topics=None):
    if not topics:
        return kac.list_topics()
    return [x for x in kac.list_topics() if x in topics]


def delete_topics(topics=None):
    if not topics:
        topics = kac.list_topics()
    for topic in topics:
        try:
            kac.delete_topics([topic])
            print("topic {} deleted".format(topic))
        except UnknownTopicOrPartitionError as ex:
            print("topic {} does not exist.".format(topic))


def describe_topics(topics=None):
    if not topics:
        topics = kac.list_topics()
    return kac.describe_topics(topics)


epilog = """
Create, Delete, List or Describe kafka topics.

Usage: 
python3 {app} create
    Reads topics.json file to create topics.
python3 {app} create topic1 [topic2] .. 
    Create topics with given names, with num_partitions=3, replication_factor=1 as default.

python3 {app} list
    List all topics.
python3 {app} list topic1 [topic2] .. 
    List given topics.
     
python3 {app} delete
    Delete all topics. 
python3 {app} delete topic1 [topic2] .. 
    Delete given topics.
     
python3 {app} describe
    Describe all topics. 
python3 {app} describe topic1 [topic2] .. 
    Describe given topics.
""".format(app=sys.argv[0])
parser = argparse.ArgumentParser(description='simplified kafka client', epilog=epilog,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
parser.add_argument(nargs=1, choices=['create', 'list', 'delete', 'describe'], dest='action',
                    help="action for the topics.")
parser.add_argument(nargs='*', dest='topics')

args = parser.parse_args()
action = args.action[0]

if action == 'create':
    create_topics(args.topics)
elif action == 'list':
    print(list_topics(args.topics))
elif action == 'delete':
    delete_topics(args.topics)
elif action == 'describe':
    print(describe_topics(args.topics))
else:
    print("no such option {}".format(action))