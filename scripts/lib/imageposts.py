import json
import os
import random
import sys
import requests
from faker import Faker
from PIL import Image


class ImagePostCreator:

    def __init__(self, url, token):
        self.url = url
        self.token = token

    def create(self):
        f = Faker()
        name = '{}.png'.format(f.word())
        path = 'var/data/images/{}'.format(name)
        # generate a random single color image of size 100x100
        file = Image.new('RGB', (100, 100), color=(
            random.randint(1, 255), random.randint(1, 255), random.randint(1, 255)))
        file.save(path)

        with open(path, 'rb') as fh:
            files = {
                'json': (None, json.dumps({'name': name}), 'application/json'),
                'content': (name, fh, 'application/octet-stream')
            }
            resp = requests.post('{}/new'.format(self.url), files=files,
                                 headers={'Authorization': 'Bearer {}'.format(self.token)})

            if resp.status_code == 200:
                data = resp.json()
                print(data['_id'], data['name'])
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

    ImagePostCreator(os.environ.get('POSTS_API_ENDPOINT'), os.environ.get('TOKEN')).create()
