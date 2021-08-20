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
        f = Faker()
        start = random.randint(0, 95)   # demo video clip is 100 seconds long
        end = start + random.randint(1, 5)
        video = VideoFileClip("demo.mp4").subclip(start, end)

        name = '{}.mp4'.format(str.lower(f.word()))
        video.write_videofile(name, fps=25)

        tags = ','.join([f.word() for i in range(random.randint(1, 5))])
        with open(name, 'rb') as fh:
            resp = requests.post('{}/new'.format(self.url), data={'name': name, 'tags': tags}, files={'content': fh},
                                 headers={'Authorization': 'Bearer {}'.format(self.token)})

            if resp.status_code == 200:
                data = resp.json()
                print(data['_id'], data['name'], data['tags'])
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

