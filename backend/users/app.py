from typing import Dict, List

import jwt
import uuid
import logging.config
from faker import Faker
from http import HTTPStatus
from datetime import datetime
from common.customflask import CustomFlask
from common.customverifier import CustomJWTVerifier
from werkzeug.exceptions import HTTPException, abort

from common.utils import FlaskUtils

logging.config.fileConfig('./logging.conf')
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = CustomFlask(__name__)
conf = app.conf
db = app.db


for cls in HTTPException.__subclasses__():
    app.register_error_handler(cls, CustomJWTVerifier.handle_error)


@app.route("/api/v1/users/new", methods=['POST'])
@CustomJWTVerifier.verify_jwt_token
def create_dummy_user(my_id, is_admin=False):
    if not is_admin:
        abort(HTTPStatus.FORBIDDEN, description="/api/v1/users/new needs admin privileges!")

    new_user = User()
    new_user.fake_info()
    new_user.save()

    return app.make_response(new_user.__dict__())


@app.route("/api/v1/users", methods=['GET'])
@CustomJWTVerifier.verify_jwt_token
def get_all_users(my_id, is_admin=False):
    print("get_all_users called")
    skip, limit = FlaskUtils.get_skip_limit()
    if is_admin:
        users = db.retrieve("users", skip=skip, limit=limit)
    else:
        users = db.retrieve("users", select_columns=["_id", "name"], skip=skip, limit=limit)

    return app.make_response(users)


@app.route('/api/v1/users/<user_id>', methods=['GET'])
@CustomJWTVerifier.verify_jwt_token
def get_user(user_id, my_id, is_admin=False):
    print("my_id {}, user_id {}, is_admin {}".format(my_id, user_id, is_admin))
    if my_id == user_id:
        # return full info for self
        return app.make_response(User.get(my_id))
    else:
        return app.make_response(User.get(user_id, select_columns=['_id', 'name']))


class User:

    def __init__(self):
        self._id = None
        self.name = None
        self.role = None
        self.creation_date = None
        self.token = None
        pass

    def fake_info(self):
        self._id = '{}'.format(uuid.uuid4())
        self.name = Faker().name()
        self.role = 'user'
        self.creation_date = datetime.utcnow().timestamp()

        token_raw = {
            "_id": self._id,
            "name": self.name,
            "sub": self._id,
            "email": '{}@localhost'.format(self.name.replace(' ', '_').lower()),
            "role": self.role,
            "ver": 1,
            "iss": "python/flask",
            "iat": datetime.utcnow().timestamp(),
            "exp": datetime.utcnow().timestamp() + conf.get('token_expiry_in_days', 7) * 86400,
        }

        # create a JWT token for this user.
        self.token = jwt.encode(token_raw, conf.get('secret_key'), algorithm="HS256")

    def save(self):
        db.save(self.__dict__(), 'users')

    def with_id(self, _id: str):
        self._id = _id

    def with_username(self, name: str):
        self.name = name

    def __dict__(self):
        return {
            '_id': self._id,
            'name': self.name,
            'role': self.role,
            'creation_date': self.creation_date,
            'token': self.token
        }

    @staticmethod
    def get(user_id: str, select_columns: List = None):
        return db.retrieve('users', filters={'_id': user_id}, select_columns=select_columns, limit=1)
