import os
import random
import sys
import requests
from faker import Faker


class PostCreator:

    def __init__(self, url, token):
        self.url = url
        self.token = token

    def create(self):
        f = Faker()
        content = ' '.join([f.sentence() for i in range(random.randint(2, 10))])

        resp = requests.post('{}/new'.format(self.url), json={'content': content},
                             headers={'Authorization': 'Bearer {}'.format(self.token)})

        if resp.status_code == 200:
            data = resp.json()
            print(data['_id'], data['content'])
            return data
        else:
            print("ERROR - {}".format(resp.content))


if __name__ == '__main__':

    if not os.environ.get('POSTS_API_ENDPOINT'):
        print("export POSTS_API_ENDPOINT")
        sys.exit(1)

    if not os.environ.get('TOKEN'):
        print("export TOKEN")
        sys.exit(1)

    PostCreator(os.environ.get('POSTS_API_ENDPOINT'), os.environ.get('TOKEN')).create()
