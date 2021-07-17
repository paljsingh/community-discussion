import uuid
from datetime import datetime
import jwt
from flask import Flask, request, make_response

from common.config import Config
from common.db import Db


class CustomFlask(Flask):
    def __init__(self, name):
        super().__init__(name)
        self.conf = Config.load()
        self.db = Db(self.conf.get('db_uri'), self.conf.get('db_name'))

    def process_response(self, response):
        # hide server info.
        response.headers['server'] = "Custom Web Server"
        super(CustomFlask, self).process_response(response)
        return(response)

    def create_new_user(self):
        print(request.headers)
        # create a new user - use uuid for unique identifier.
        user_id = 'user-{}'.format(uuid.uuid4())
        user_info = {
            "name": user_id,
            "sub": user_id,
            "email": '{}@localhost'.format(user_id),
            "ver": 1,
            "iat": datetime.utcnow().timestamp(),
            "exp": datetime.utcnow().timestamp() + 7 * 86400,   # 1 week from now.
        }
        # create a JWT token for this user.
        jwt_token = jwt.encode(user_info, self.conf.get('secret_key'), algorithm="HS256")

        # save the user details to the db.
        user_obj = {**user_info, 'token': jwt_token, '_id': user_id}
        self.db.save(user_obj, 'users')

        # send response
        return make_response(user_obj)

    def get_all_users(self):
        # TODO: get user data from cache
        # TODO: support pagination.
        users = {
            "links": {
                "pagination": {
                    "total": 50,
                    "per_page": 15,
                    "current_page": 1,
                    "last_page": 4,
                    "next_page_url": "...",
                    "prev_page_url": "...",
                    "from": 1,
                    "to": 15,
                }
            },
            "data": [user for user in self.db.get_collection('users').find()]
        }
        # send response
        return make_response(users)
