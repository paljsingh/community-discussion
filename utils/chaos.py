import os
import random
import sys

from .communities import CommunityCreator
from .imageposts import ImagePostCreator
from .posts import PostCreator
from .usergroups import UserGroupCreator
from .users import UserCreator
from .videoposts import VideoPostCreator


class Chaos:

    volume_distribution = {
        'posts': 60,
        'image_posts': 20,
        'video_posts': 5,
        'users': 10,
        'usergroups': 5,
        'communities': 5
    }

    @staticmethod
    def create_everything(admin_token, total, **kvargs):
        total = sum([v for k, v in Chaos.volume_distribution.items()])
        prob = dict({k: v/total for k, v in Chaos.volume_distribution.items()})

        for i in range(total):
            # keep the order as is, so that we have users and communities created before adding posts to them.
            users = []
            for j in range(int(prob['users']*total)):
                users.append(UserCreator(admin_token, kvargs['user_api_endpoint']).create())

            communities = []
            for j in range(int(prob['communities']*total)):
                # fetch a random user token
                user_token = users[random.randint(0, len(users))]['token']
                communities.append(CommunityCreator(user_token, kvargs['communities_api_endpoint']).create())

            usergroups = []
            for j in range(int(prob['usergroups']*total)):
                # fetch a random user token
                user_token = users[random.randint(0, len(users))]['token']
                usergroups.append(UserGroupCreator(user_token, kvargs['usergroups_api_endpoint']).create())

            posts = []
            for j in range(int(prob['posts']*total)):
                # fetch a random user token
                user_token = users[random.randint(0, len(users))]['token']
                posts.append(PostCreator(user_token, kvargs['posts_api_endpoint']).create())

            image_posts = []
            for j in range(int(prob['images']*total)):
                # fetch a random user token
                user_token = users[random.randint(0, len(users))]['token']
                image_posts.append(ImagePostCreator(user_token, kvargs['posts_api_endpoint']).create())

            video_posts = []
            for j in range(int(prob['videos']*total)):
                # fetch a random user token
                user_token = users[random.randint(0, len(users))]['token']
                video_posts.append(VideoPostCreator(user_token, kvargs['posts_api_endpoint']).create())


if __name__ == '__main__':
    """
    Use ADMIN_TOKEN for creating users,
    then use jwt tokens from random users to create communities, usergroups, posts, image posts, video posts etc.
    TODO: Add chat messages for plain text / image / video
    
    An option number can be specified on the command line arguments to specify how many total requests shoule be sent
    by the script, default is 1000 if no arguments specified.
    
    The total count of requests is divided into users, communities, posts, usergroups, image posts, video posts etc
    by their volume distribution number defined above. Higher number => higher count for the associated resource.
    """

    if not os.environ.get('ADMIN_TOKEN'):
        print("export ADMIN_TOKEN")
        sys.exit(1)

    host = 'http://localhost'
    endpoints = {
        'user_api_endpoint': '{}:{}/api/v1/users'.format(host, 5000),
        'usergroups_api_endpoint': '{}:{}/api/v1/usergroups'.format(host, 5001),
        'communities_api_endpoint': '{}:{}/api/v1/communities'.format(host, 5002),
        'posts_api_endpoint': '{}:{}/api/v1/posts'.format(host, 5003)
    }

    total_requests = sys.argv[1] if len(sys.argv) > 0 else 1000
    Chaos.create_everything(os.environ.get('ADMIN_TOKEN'), total_requests, **endpoints)
