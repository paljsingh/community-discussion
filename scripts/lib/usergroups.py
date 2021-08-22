import os
import random
import sys
from typing import List

import requests
from faker import Faker


class UserGroupCreator:

    def __init__(self, url, token, users: List):
        self.url = url
        self.token = token
        self.users = users

    def create(self):
        f = Faker()
        name = '{}-{}-{}'.format(f.word(), f.word(), f.word())
        tags = ','.join([f.word() for i in range(random.randint(1, 5))])
        resp = requests.post('{}/new'.format(self.url), json={'name': name, 'tags': tags, 'users': self.users},
                             headers={'Authorization': 'Bearer {}'.format(self.token)})

        if resp.status_code == 200:
            data = resp.json()
            print('{}\t{}\t[{}]'.format(data['_id'], data['name'], data['tags']))
            return data
        else:
            print("ERROR - {}".format(resp.content))


if __name__ == '__main__':

    if not os.environ.get('USERGROUPS_API_ENDPOINT'):
        print("export USERGROUPS_API_ENDPOINT")
        sys.exit(1)

    if not os.environ.get('TOKEN'):
        print("export TOKEN")
        sys.exit(1)

    UserGroupCreator(os.environ.get('USERGROUPS_API_ENDPOINT'), os.environ.get('TOKEN')).create()
