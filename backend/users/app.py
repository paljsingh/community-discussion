#!/usr/bin/env python3
from typing import Callable

from flask import Flask, make_response
from okta_jwt_verifier import JWTVerifier
from okta_jwt_verifier.exceptions import JWTValidationException
from flask_cors import CORS
from flask import request


import logging.config
from datetime import datetime
import uuid
import jwt

from users.config import Config
from users.db import Db

logging.config.fileConfig("../logging.conf")
logger = logging.getLogger(__name__)

config = Config.load()
db_obj = Db(config.get('db_uri'), config.get('db_name'))


app = Flask(__name__)
CORS(app)


def verify_jwt_token(func: Callable):
    # TODO: Support custom jwt tokens.
    async def wrapper(*args, **kwargs):
        jwt_token = request.headers.get('Authorization').split(' ')[1]
        jwt_verifier = JWTVerifier(config.get('issuer'), config.get('client_id'), config.get('audience'))
        await jwt_verifier.verify_access_token(jwt_token)
        return func(*args, **kwargs)
    return wrapper


@app.route("/api/v1/users/new", methods=['POST'])
@verify_jwt_token
def create_new_user():
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
    jwt_token = jwt.encode(user_info, config.get('secret_key'), algorithm="HS256")

    # save the user details to the db.
    user_obj = {**user_info, 'token': jwt_token, '_id': user_id}
    db_obj.save(user_obj, 'users')

    # send response
    return make_response(user_obj)


@app.route("/api/v1/users", methods=['GET'])
@verify_jwt_token
def get_all_users():
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
        "data": [user for user in db_obj.get_collection('users').find()]
    }
    # send response
    return make_response(users)