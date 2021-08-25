import json
import random
from faker import Faker
from moviepy.editor import VideoFileClip
import os
import sys
import requests


class VideoPostCreator:

    def __init__(self, url, token):
        self.url = url
        self.token = token

    def create(self):
        # create random clips from the sample video available under var/data/
        start = random.randint(0, 120)   # video clip is 125 seconds long
        end = start + random.randint(1, 5)
        filepath = os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])), "./big-buck-bunny.mp4")
        video = VideoFileClip(filepath).subclip(start, end)

        f = Faker()
        name = '{}.mp4'.format(str.lower(f.word()))
        path = 'var/data/videos/{}'.format(name)

        video.write_videofile(path, fps=15)

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

    VideoPostCreator(os.environ.get('POSTS_API_ENDPOINT'), os.environ.get('TOKEN')).create()
