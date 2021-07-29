import logging.config

from flask_cors import CORS

from werkzeug.exceptions import HTTPException
from flask import request

from common.customflask import CustomFlask
from common.customverifier import CustomJWTVerifier
from faker import Faker

from common.config import Config
from common.db import Db

import uuid
from datetime import datetime
import jwt
from urllib.parse import urlparse, ParseResult, parse_qs, urlencode

conf = Config.load()
db = Db(conf.get('db_uri'), conf.get('db_name'))

logging.config.fileConfig('./logging.conf')
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = CustomFlask(__name__)
app.secret_key = conf.get('secret_key')

CORS(app)

for cls in HTTPException.__subclasses__():
    app.register_error_handler(cls, CustomJWTVerifier.handle_error)


@app.route("/api/v1/users/new", methods=['POST'])
@CustomJWTVerifier.verify_jwt_token
def create_dummy_user():
    # create a new dummy user - use uuid for unique identifier.
    user_id = '{}'.format(uuid.uuid4())
    user_name = Faker().name()
    user_info = {
        "_id": user_id,
        "name": user_name,
        "sub": user_id,
        "email": '{}@localhost'.format(user_name.replace(' ', '_').lower()),
        "ver": 1,
        "iss": "python/flask",
        "iat": datetime.utcnow().timestamp(),
        "exp": datetime.utcnow().timestamp() + conf.get('token_expiry_in_days', 7) * 86400,
    }
    # create a JWT token for this user.
    jwt_token = jwt.encode(user_info, conf.get('secret_key'), algorithm="HS256")
    print("new jwt token".format(jwt_token))
    # save the user details to the db.
    user_obj = {**user_info, 'token': jwt_token, '_id': user_id}
    db.save(user_obj, 'users')

    # send response
    return app.make_response(user_obj)


@app.route("/api/v1/users", methods=['GET'])
@CustomJWTVerifier.verify_jwt_token
def get_all_users():
    users = _get_paginated_records("users")
    # send response
    print(request.url)
    print(users['pagination'])
    return app.make_response(users)


def _per_page_with_limit():
    """
    If query parameter exist, return number of items specified in query parameter, subject to a max
    configurable limit (or hardcoded number 100)
    :return:
    """
    items_per_page = int(request.args.get("itemsPerPage", conf.get("default_per_page", 10)))
    return min(items_per_page, conf.get('max_per_page', 100))


def _pagination_info(collection_name: str):
    total_records = db.get_collection(collection_name).count()
    items_per_page = _per_page_with_limit()
    current_page = int(request.args.get("page", 1))

    # skip_recoerd = (current_page - 1) * items_per_page
    # from_record = skip_recoerd + 1
    # to_record = current_page * items_per_page if current_page * items_per_page <= total_records else total_records

    return {
        "total": total_records,
        "itemsPerPage": items_per_page,
        "page": current_page,
    }


def _get_page_url(current_page: int):
    """
    Create a new url with page index updated.
    :param current_page:
    :return:
    """
    u = urlparse(request.url)
    params = parse_qs(u.query)
    params['page'] = current_page     # noqa
    res = ParseResult(scheme=u.scheme, netloc=u.hostname, path=u.path, params=u.params, query=urlencode(params),
                      fragment=u.fragment)  # noqa  - https://youtrack.jetbrains.com/issue/PY-22102
    return res.geturl()


def _get_paginated_records(collection_name: str):
    pinfo = _pagination_info(collection_name)
    skip_records = (pinfo['page'] - 1)*pinfo['itemsPerPage']
    data = [name for name in db.get_collection(collection_name).find(skip=skip_records, limit=pinfo['itemsPerPage'])]
    return {
        "pagination": pinfo,
        "data": data
    }