import logging.config
from datetime import datetime
from random import Random
from typing import List

from werkzeug.exceptions import HTTPException
from faker import Faker
from flask import request
import uuid

from common.customflask import CustomFlask
from common.customverifier import CustomJWTVerifier
from common.utils import FlaskUtils

logging.config.fileConfig('../logging.conf')
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = CustomFlask(__name__)
conf = app.conf
db = app.db

for cls in HTTPException.__subclasses__():
    app.register_error_handler(cls, CustomJWTVerifier.handle_error)


@app.route("/api/v1/communities/<community_id>/usergroups/new", methods=['POST'])
@CustomJWTVerifier.verify_jwt_token
def create_usergroup(community_id, my_id, is_admin=False):

    new_usergroup = Usergroup(my_id).fake_info()

    data = request.get_json()
    # override with any data available in the post body.
    if data and data.get('name'):
        new_usergroup.with_name(data.get('name'))
    if data and data.get('users'):
        new_usergroup.with_users(data.get('users'))
    new_usergroup.save()
    return app.make_response(new_usergroup.__dict__())


@app.route("/api/v1/communities/<community_id>/usergroups", methods=['GET'])
@CustomJWTVerifier.verify_jwt_token
def get_usergroups(community_id, my_id, is_admin=False):
    """
    :param my_id:
    :param community_id:
    :param is_admin: if admin, return all data for the user groups.
    for non-admins, return only the public data.
    :return:
    """
    community = db.retrieve('communities', {'_id': community_id}, limit=1)
    usergroup_ids = community['usergroups']

    skip, limit = FlaskUtils.get_skip_limit()
    if is_admin:
        usergroups = db.retrieve("usergroups", filters={'_id': {'$in': usergroup_ids}}, skip=skip, limit=limit)
    else:
        usergroups = db.retrieve("usergroups", filters={'_id': {'$in': usergroup_ids}},
                                 select_columns=["_id", "name", "users"], skip=skip, limit=limit)

    for ug in usergroups:
        for user in ug.get('users'):
            filtered_user = {"_id": user.get("_id"), "name": user.get("name")}
            ug['users'] = filtered_user
    # send response
    return app.make_response(usergroups)


@app.route('/api/v1/usergroups/search', methods=['GET'])
@CustomJWTVerifier.verify_jwt_token
def search_users(my_id, is_admin=False):
    select_columns = []
    if not is_admin:
        select_columns = ['_id', 'name']

    # The comma is not a typo.
    # get_url_args returns a tuple, the syntax is needed to expand it inline when receiving a single argument.
    name, = FlaskUtils.get_url_args('name')

    skip, limit = FlaskUtils.get_skip_limit()

    # search for given name in indexed text-fields
    users = db.retrieve('users', {
        '$text': {
            '$search': name,
            '$caseSensitive': False,
            '$diacriticSensitive': False,   # treat é, ê the same as e
        }
    }, select_columns=select_columns, limit=limit, skip=skip)

    # TODO: any history updates / events here.

    return app.make_response(users)


class Usergroup:

    def __init__(self, created_by):
        self._id = '{}'.format(uuid.uuid4())
        self.name = None
        self.users = set()
        self.creation_date = datetime.utcnow().timestamp()
        self.created_by = created_by
        pass

    def fake_info(self):
        f = Faker()
        # give it a random 1 - 3 word name
        self.name = ' '.join([str.title(f.words()) for i in range(Random().randint(1, 3))])
        return self

    def with_name(self, name: str):
        self.name = name
        return self

    def with_users(self, users: List):
        self.users.update(users)
        return self

    def __dict__(self):
        return {
            '_id': self._id,
            'name': self.name,
            'creation_date': self.creation_date,
            'created_by': self.created_by
        }

    def save(self):
        db.save(self.__dict__(), 'usergroups')

    @staticmethod
    def get(usergroup_id: str, select_columns: List = None):
        return db.retrieve('usergroups', filters={'_id': usergroup_id}, select_columns=select_columns, limit=1)
