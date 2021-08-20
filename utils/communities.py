import os
import random
import sys
import requests
from faker import Faker


class CommunityCreator:

    def __init__(self, url, token):
        self.url = url
        self.token = token

    def create(self):
        f = Faker()
        name = '{} {}'.format(f.word(), f.word())
        tags = ','.join([f.word() for i in range(random.randint(1, 5))])
        resp = requests.post('{}/new'.format(self.url), {'name': name, 'tags': tags},
                             headers={'Authorization': 'Bearer {}'.format(self.token)})

        if resp.status_code == 200:
            data = resp.json()
            print(data['_id'], data['name'], data['tags'])
        else:
            print("ERROR - {}".format(resp.content))


if __name__ == '__main__':
    if not os.environ.get('COMMUNITIES_API_ENDPOINT'):
        print("export COMMUNITIES_API_ENDPOINT")
        sys.exit(1)

    if not os.environ.get('TOKEN'):
        print("export TOKEN")
        sys.exit(1)

    CommunityCreator(os.environ.get('COMMUNITIES_API_ENDPOINT'), os.environ.get('TOKEN')).create()
