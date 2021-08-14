from pymodm import MongoModel
from pymodm.fields import CharField, DateTimeField, ListField
from pymongo.write_concern import WriteConcern

import logging.config
from datetime import datetime
from random import Random

from werkzeug.exceptions import HTTPException
from faker import Faker
from flask import request
import uuid

from common.customflask import CustomFlask
from common.customverifier import CustomJWTVerifier
from common.db import Db
from common.utils import FlaskUtils
from communities.app import Community

logging.config.fileConfig('../logging.conf')
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = CustomFlask(__name__)
app.config['MONGODB_SETTINGS'] = {'host': app.conf.get('db_uri')}
db = Db()


for cls in HTTPException.__subclasses__():
    app.register_error_handler(cls, CustomJWTVerifier.handle_error)


@app.route("/api/v1/communities/<community_id>/usergroups/new", methods=['POST'])
@CustomJWTVerifier.verify_jwt_token
def create_usergroup(community_id, my_id, is_admin=False):
    data = request.get_json()
    new_usergroup = Usergroup(created_by=my_id)
    new_usergroup.fake_info()

    # override with any data available in the post body.
    if data and data.get('name'):
        new_usergroup.name = data['name']
    if data and data.get('tags'):
        new_usergroup.tags = data['tags']
    if data and data.get('users'):
        new_usergroup.users = data['users']

    new_usergroup.save()
    return app.make_response(new_usergroup.to_son())


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

    # find all usergroup ids in the community
    community = db.get(Community, community_id, to_son=False)
    usergroup_ids = community.usergroups

    select_columns = ["name", "users"]
    if is_admin:
        select_columns = None

    # not using auto_dereferencing, instead create a bulk query to fetch all usergroups together.

    # collect usergroups for the above usergroup ids.
    usergroups = db.retrieve(
        Usergroup, filters={'id': {'$in': usergroup_ids}},
        select_columns=select_columns)

    return app.make_response(usergroups)


@app.route('/api/v1/usergroups/search', methods=['GET'])
@CustomJWTVerifier.verify_jwt_token
def search_usergroups(my_id, is_admin=False):
    name, = FlaskUtils.get_url_args('name')

    # search for given name in indexed text-fields
    usergroups = db.retrieve(Usergroup, {
        '$text': {
            '$search': name,
            '$caseSensitive': False,
            '$diacriticSensitive': False,   # treat é, ê the same as e
        }
    })

    # TODO: any history updates / events here.

    return app.make_response(usergroups)

# TODO
# api to fetch my user groups
# api to update user group info


class Usergroup(MongoModel):
    id = CharField(required=True, primary_key=True, default=uuid.uuid4)
    name = CharField(required=True)
    users = ListField(required=False, blank=True)
    creation_date = DateTimeField(required=True, default=datetime.utcnow)
    created_by = CharField(required=True)
    tags = ListField(required=False, blank=True)

    def fake_info(self):
        f = Faker()
        # give it a random 1 - 3 word name
        self.name = ' '.join([str.title(f.words()) for i in range(Random().randint(1, 3))])
        return self

    class Meta:
        write_concern = WriteConcern(j=True)
        connection_alias = 'my-app'
