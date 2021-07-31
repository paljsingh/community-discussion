from datetime import datetime
from faker import Faker
from flask_cors import CORS
import jwt
import logging.config
import uuid
from werkzeug.exceptions import HTTPException

from common.config import Config
from common.db import Db
from common.pagination import Pagination
from common.customflask import CustomFlask
from common.customverifier import CustomJWTVerifier

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
def create_dummy_user(is_admin=False):
    if not is_admin:
        print("/api/v1/users/new needs admin privileges!")
        return

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
    # save the user details to the db.
    user_obj = {**user_info, 'token': jwt_token, '_id': user_id}
    db.save(user_obj, 'users')

    # send response
    return app.make_response(user_obj)


@app.route("/api/v1/users", methods=['GET'])
@CustomJWTVerifier.verify_jwt_token
def get_all_users(is_admin=False):
    if is_admin:
        users = Pagination.get_paginated_records("users")
    else:
        users = Pagination.get_paginated_records("users", ["_id", "name"])
    # send response
    return app.make_response(users)
