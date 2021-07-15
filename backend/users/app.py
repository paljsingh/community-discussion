
import random

from flask import Flask, g, redirect, url_for, make_response
from flask_oidc import OpenIDConnect
from okta.client import Client
import logging.config
from datetime import datetime
import uuid
import jwt

from users.config import Config
from users.db import Db

# logging.config.fileConfig("etc/logging.conf")
logger = logging.getLogger(__name__)

config = Config.load()
db_obj = Db(config.get('db_uri'), config.get('db_name'))


app = Flask(__name__)

app.config["OIDC_CLIENT_SECRETS"] = "client_secrets.json"
app.config["OIDC_COOKIE_SECURE"] = False
app.config["OIDC_CALLBACK_ROUTE"] = "/oidc/callback"
app.config["OIDC_SCOPES"] = ["openid", "email", "profile"]

# for encrypting flask session
app.config["SECRET_KEY"] = config.get('secret_key')

oidc = OpenIDConnect(app)

client_config = {"orgUrl": config.get('org_url'), "token": config.get('access_token')}
okta_client = Client(user_config=client_config)


# what goes to database directly?
# low frequency events - user creation, community, user group creation

# what goes to kafka?
# high frequency events - posts, messages, comments, likes, shares


@app.before_request
def before_request():
    if oidc.user_loggedin:
        g.user = okta_client.get_user(oidc.user_getfield("sub"))
    else:
        g.user = None


@app.route("/api/v1/users/new", methods=['POST'])
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
def get_all_users():
    # save the user details to the db.
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
    print(users)
    # send response
    return make_response(users)



@app.route("/dashboard")
@oidc.require_login
def dashboard():
    return 'dashboard!'


@app.route("/login")
@oidc.require_login
def login():
    return redirect(url_for(".dashboard"))


@app.route("/logout")
def logout():
    oidc.logout()
    return redirect(url_for(".index"))
