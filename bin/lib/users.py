import os
import sys
import requests


class UserCreator:

    def __init__(self, url, admin_token):
        self.url = url
        self.admin_token = admin_token

    def create(self):
        resp = requests.post('{}/new'.format(self.url),
                             headers={'Authorization': 'Bearer {}'.format(self.admin_token)})

        if resp.status_code == 200:
            data = resp.json()
            print(data['_id'], data['name'])
            return data
        else:
            print("ERROR - {}".format(resp.content))


if __name__ == '__main__':

    if not os.environ.get('USERS_API_ENDPOINT'):
        print("export USERS_API_ENDPOINT")
        sys.exit(1)

    if not os.environ.get('ADMIN_TOKEN'):
        print("export ADMIN_TOKEN")
        sys.exit(1)

    UserCreator(os.environ.get('USERS_API_ENDPOINT'), os.environ.get('ADMIN_TOKEN')).create()
