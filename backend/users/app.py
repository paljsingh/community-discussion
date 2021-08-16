from pymodm import MongoModel
from pymodm.fields import CharField, DateTimeField
from pymongo.write_concern import WriteConcern

import jwt
import uuid
import logging.config
from faker import Faker
from http import HTTPStatus
from datetime import datetime
from common.customflask import CustomFlask
from common.customverifier import CustomJWTVerifier
from werkzeug.exceptions import HTTPException, abort
from flask import request
from common.db import Db
from common.utils import FlaskUtils

logging.config.fileConfig('../logging.conf')
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = CustomFlask(__name__)
app.config['MONGODB_SETTINGS'] = {'host': app.conf.get('db_uri')}
db = Db()


for cls in HTTPException.__subclasses__():
    app.register_error_handler(cls, CustomJWTVerifier.handle_error)


@app.route("/api/v1/users/new", methods=['POST'])
@CustomJWTVerifier.verify_jwt_token
def create_dummy_user(my_id, is_admin=False):
    print("called /api/v1/users/new")
    if not is_admin:
        abort(HTTPStatus.FORBIDDEN, description="/api/v1/users/new needs admin privileges!")

    new_user = User()
    new_user.fake_info()
    new_user.save()

    return app.make_response(new_user.to_son())


@app.route("/api/v1/users", methods=['GET'])
@CustomJWTVerifier.verify_jwt_token
def get_all_users(my_id, is_admin=False):
    print("------ called")
    if is_admin:
        select_columns = None
    else:
        select_columns = ["name"]

    # The comma is not a typo.
    # get_url_args returns a tuple, the syntax is needed to expand it inline when receiving a single argument.
    name, = FlaskUtils.get_url_args('name')
    name = name if len(name) >= app.conf.get('min_search_len', 3) else None

    filters = {}
    if name:
        filters = {
            '$text': {
                '$search': name,
                '$caseSensitive': False,
                '$diacriticSensitive': False,   # treat é, ê the same as e
            }
        }

    users = db.retrieve(User, filters=filters, select_columns=select_columns)
    return app.make_response(users)


@app.route('/api/v1/users/<user_id>', methods=['GET'])
@CustomJWTVerifier.verify_jwt_token
def get_user(user_id, my_id, is_admin=False):
    if my_id == user_id or is_admin:
        # return full info for self
        return app.make_response(db.get(User, user_id))
    else:
        return app.make_response(db.get(User, user_id, select_columns=['name']))


# TODO
# Update a user api


class User(MongoModel):
    id = CharField(required=True, primary_key=True, default=uuid.uuid4)
    name = CharField(required=True)
    role = CharField(required=True, default='user')
    creation_date = DateTimeField(required=True, default=datetime.utcnow)
    token = CharField(required=True)

    def fake_info(self):
        self.name = Faker().name()
        print(self.id)
        token_raw = {
            "name": self.name,
            "sub": str(self.id),
            "email": '{}@localhost'.format(self.name.replace(' ', '_').lower()),
            "role": self.role,
            "ver": 1,
            "iss": "python/flask",
            "iat": datetime.utcnow().timestamp(),
            "exp": datetime.utcnow().timestamp() + app.conf.get('token_expiry_in_days', 7) * 86400,
        }
        # create a JWT token for this user.
        self.token = jwt.encode(token_raw, app.conf.get('secret_key'), algorithm="HS256")

    class Meta:
        write_concern = WriteConcern(j=True)
        connection_alias = 'my-app'
