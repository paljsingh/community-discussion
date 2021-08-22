import os
import random
import sys

from lib.communities import CommunityCreator
from lib.imageposts import ImagePostCreator
from lib.posts import PostCreator
from lib.usergroups import UserGroupCreator
from lib.users import UserCreator
from lib.videoposts import VideoPostCreator


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
        sum_vd = sum([v for k, v in Chaos.volume_distribution.items()])
        prob = dict({k: v/sum_vd for k, v in Chaos.volume_distribution.items()})

        # keep the order as is, so that we have users and communities created before adding posts to them.
        users = []
        print("user: id\tname")
        for j in range(int(prob['users']*total)):
            users.append(UserCreator(kvargs['user_api_endpoint'], admin_token).create())
        print("created {} users.".format(len(users)))

        communities = []
        print("community: id\tname\t[tags]")
        for j in range(int(prob['communities']*total)):
            # fetch a random user token
            user_token = users[random.randint(0, len(users)-1)]['token']
            communities.append(CommunityCreator(kvargs['communities_api_endpoint'], user_token).create())
        print("created {} communities.".format(len(communities)))

        usergroups = []
        print("usergroups: id\tname\t[tags]")
        for j in range(int(prob['usergroups']*total)):
            # fetch a random user token
            rand1 = random.randint(0, len(users)-1)
            rand2 = random.randint(0, len(users)-1)
            user1_token = users[rand1]['token']
            user1_id = users[rand1]['_id']
            user2_id = users[rand2]['_id']

            usergroups.append(UserGroupCreator(kvargs['usergroups_api_endpoint'], user1_token, [user1_id, user2_id]).create())
        print("created {} usergroups.".format(len(usergroups)))

        posts = []
        print("text posts: id\tcontent")
        for j in range(int(prob['posts']*total)):
            # fetch a random user token
            user_token = users[random.randint(0, len(users)-1)]['token']
            # fetch a random community
            community_id = communities[random.randint(0, len(communities)-1)]['_id']
            posts.append(PostCreator(kvargs['text_posts_api_endpoint'].replace(
                '<community_id>', community_id), user_token).create())
        print("created {} posts.".format(len(posts)))

        image_posts = []
        print("image posts: id\tfilename")
        for j in range(int(prob['image_posts']*total)):
            # fetch a random user token
            user_token = users[random.randint(0, len(users)-1)]['token']
            community_id = communities[random.randint(0, len(communities)-1)]['_id']
            image_posts.append(ImagePostCreator(kvargs['image_posts_api_endpoint'].replace(
                '<community_id>', community_id), user_token).create())
        print("created {} image posts.".format(len(image_posts)))

        video_posts = []
        print("video posts: id\tfilename")
        for j in range(int(prob['video_posts']*total)):
            # fetch a random user token
            user_token = users[random.randint(0, len(users)-1)]['token']
            community_id = communities[random.randint(0, len(communities)-1)]['_id']
            video_posts.append(VideoPostCreator(kvargs['video_posts_api_endpoint'].replace(
                '<community_id>', community_id), user_token).create())
        print("created {} video posts.".format(len(video_posts)))


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
        'communities_api_endpoint': '{}:{}/api/v1/communities'.format(host, 5001),
        'usergroups_api_endpoint': '{}:{}/api/v1/communities/<community_id>/usergroups'.format(host, 5001),
        'text_posts_api_endpoint': '{}:{}/api/v1/communities/<community_id>/posts'.format(host, 5003),
        'image_posts_api_endpoint': '{}:{}/api/v1/communities/<community_id>/images'.format(host, 5003),
        'video_posts_api_endpoint': '{}:{}/api/v1/communities/<community_id>/videos'.format(host, 5003)
    }

    total_requests = int(sys.argv[1]) if len(sys.argv) > 1 else 1000
    Chaos.create_everything(os.environ.get('ADMIN_TOKEN'), total_requests, **endpoints)
