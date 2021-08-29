import os
import random
import sys

from lib.communities import CommunityCreator
from lib.imageposts import ImagePostCreator
from lib.posts import PostCreator
from lib.usergroups import UserGroupCreator
from lib.users import UserCreator
from lib.videoposts import VideoPostCreator
from envyaml import EnvYAML


class Chaos:
    """
    Named after the chaos-monkey,
    howver, this script will only try to /create/ resources, randomly.
    """

    def __init__(self, admin_token, total, **endpoints):
        self.total = total
        self.admin_token = admin_token
        self.endpoints = endpoints
        conf_file_path = os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])), "etc/chaos.yaml")
        self.conf = EnvYAML(conf_file_path, strict=False)

        self.volume_distribution = self.conf.get('volume_distribution')
        self.flask_host = self.conf.get('flask_host')

        sum_vd = sum([v for k, v in self.volume_distribution.items()])
        self.prob = dict({k: v/sum_vd for k, v in self.volume_distribution.items()})

    def get_resource_count(self, name):
        return int(round(self.prob[name] * self.total, 0))

    def get_endpoint(self, name, **kvargs):
        return self.conf.get(name).format(flask_host=self.flask_host, **kvargs)

    def create_everything(self):

        # keep the order as is, so that we have users and communities created before adding posts to them.
        users = []
        print("user: id\tname")
        for j in range(self.get_resource_count('users')):
            ep = self.get_endpoint('endpoints.user_api_endpoint')
            users.append(UserCreator(ep, self.admin_token).create())
        print("created {} users.".format(len(users)))
        print("---\n")

        communities = []
        print("community: id\tname\t[tags]")
        for j in range(self.get_resource_count('communities')):
            # fetch a random user token
            user_token = users[random.randint(0, len(users)-1)]['token']
            ep = self.get_endpoint('endpoints.communities_api_endpoint')
            communities.append(CommunityCreator(ep, user_token).create())
        print("created {} communities.".format(len(communities)))
        print("---\n")

        usergroups = []
        print("usergroups: id\tname\t[tags]")
        for j in range(self.get_resource_count('usergroups')):
            # fetch a random user token
            rand1 = random.randint(0, len(users)-1)
            rand2 = random.randint(0, len(users)-1)
            user1_token = users[rand1]['token']
            user1_id = users[rand1]['_id']
            user2_id = users[rand2]['_id']
            community_id = communities[random.randint(0, len(communities)-1)]['_id']
            ep = self.get_endpoint('endpoints.usergroups_api_endpoint', community_id=community_id)
            usergroups.append(UserGroupCreator(ep, user1_token, [user1_id, user2_id]).create())
        print("created {} usergroups.".format(len(usergroups)))
        print("---\n")

        posts = []
        print("text posts: id\tcontent")
        for j in range(self.get_resource_count('posts')):
            # fetch a random user token
            user_token = users[random.randint(0, len(users)-1)]['token']
            # fetch a random community
            community_id = communities[random.randint(0, len(communities)-1)]['_id']
            ep = self.get_endpoint('endpoints.text_posts_api_endpoint', community_id=community_id)
            posts.append(PostCreator(ep, user_token).create())
        print("created {} posts.".format(len(posts)))
        print("---\n")

        image_posts = []
        print("image posts: id\tfilename")
        for j in range(self.get_resource_count('image_posts')):
            # fetch a random user token
            user_token = users[random.randint(0, len(users)-1)]['token']
            community_id = communities[random.randint(0, len(communities)-1)]['_id']
            ep = self.get_endpoint('endpoints.image_posts_api_endpoint', community_id=community_id)
            image_posts.append(ImagePostCreator(ep, user_token).create())
        print("created {} image posts.".format(len(image_posts)))

        video_posts = []
        print("video posts: id\tfilename")
        for j in range(self.get_resource_count('video_posts')):
            # fetch a random user token
            user_token = users[random.randint(0, len(users)-1)]['token']
            community_id = communities[random.randint(0, len(communities)-1)]['_id']
            ep = self.get_endpoint('endpoints.video_posts_api_endpoint', community_id=community_id)
            video_posts.append(VideoPostCreator(ep, user_token).create())
        print("created {} video posts.".format(len(video_posts)))


if __name__ == '__main__':
    """
    Use ADMIN_TOKEN for creating users,
    then use jwt tokens from random users to create communities, usergroups, posts, image posts, video posts etc.
    TODO: Add chat messages for plain text / image / video
    
    An option number can be specified on the command line arguments to specify how many total requests should be sent
    by the script, default is 100 if no arguments specified.
    
    The total count of requests is divided into users, communities, posts, usergroups, image posts, video posts etc
    by their volume distribution number defined above. Higher number => higher count for the associated resource.
    """

    if not os.environ.get('ADMIN_TOKEN'):
        print("export ADMIN_TOKEN")
        sys.exit(1)

    total_requests = int(sys.argv[1]) if len(sys.argv) > 1 else 100
    Chaos(os.environ.get('ADMIN_TOKEN'), total_requests).create_everything()
