import json
from functools import partial
from http import HTTPStatus

from pymodm import MongoModel
from pymodm.fields import CharField, DateTimeField, ListField
from pymongo.write_concern import WriteConcern

import logging.config
from datetime import datetime
from random import Random

from werkzeug.exceptions import HTTPException, abort
from faker import Faker
from flask import request
import uuid

from common.customflask import CustomFlask
from common.customverifier import CustomJWTVerifier
from common.db import Db
from common.utils import FlaskUtils
from users.app import User
from kafka import KafkaProducer
import atexit

logging.config.fileConfig('../logging.conf')
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = CustomFlask(__name__)
app.config['MONGODB_SETTINGS'] = {'host': app.conf.get('db_uri')}
db = Db()

producer = KafkaProducer(bootstrap_servers=app.conf.get('kafka_endpoints'),
                         value_serializer=lambda v: json.dumps(v).encode('utf-8'))

atexit.register(partial(FlaskUtils.graceful_shutdown, db=db, kafka_producer=producer))

for cls in HTTPException.__subclasses__():
    app.register_error_handler(cls, CustomJWTVerifier.handle_error)


@app.route("/api/v1/usergroups/new", methods=['POST'])
@CustomJWTVerifier.verify_jwt_token
def create_temp_usergroup(my_id, is_admin=False):
    """
    a temporary user group, not associated with a community.
    This will be used for a user-user direct chat.
    :param my_id:
    :param is_admin:
    :return:
    """

    data = request.get_json()
    other_user_id = data.get('user_id')

    if not other_user_id:
        abort(HTTPStatus.PRECONDITION_FAILED)

    user_ids = [my_id, other_user_id]
    # check is a usergroup exists already for these 2 users
    usergroups = db.retrieve(
        Usergroup, filters={'users': {'$all': user_ids}}, to_son=False, pagination=False
    )

    if not usergroups:

        new_usergroup = Usergroup(created_by=my_id)
        new_usergroup.fake_info()
        # override with any data available in the post body.
        if data and data.get('name'):
            new_usergroup.name = data['name']
        if data and data.get('tags'):
            new_usergroup.tags = data['tags']
        if user_ids:
            new_usergroup.users = user_ids
        new_usergroup.save()
        usergroup = new_usergroup

        # push a new usergroup event
        producer.send('usergroups', '{id},{name},{community_id},{tags},{created_by},{creation_date},{action}'.format(
            id=usergroup.id, community_id='', usergroup_id=usergroup.id, created_by=my_id, name=new_usergroup.name,
            creation_date=datetime.utcnow().isoformat(), action='new usergroup', tags=' '.join(new_usergroup.tags)))

    else:
        usergroup = usergroups[0]

    users = db.retrieve(User, filters={'_id': {'$in': user_ids}}, select_columns=['_id', 'name'],
                        pagination=False, to_son=True)
    print("post usergroups, users from db", users)

    usergroup.users = users
    return app.make_response(usergroup.to_son())


@app.route("/api/v1/usergroups/mine", methods=['GET'])
@CustomJWTVerifier.verify_jwt_token
def get_my_usergroups(my_id, is_admin=False):
    """
    :param my_id:
    :param is_admin: if admin, return all data for the user groups.
    for non-admins, return only the public data.
    :return:
    """
    app.make_response(db.retrieve(Usergroup, filters={'users': {'$in': [my_id]}}))


@app.route("/api/v1/usergroups", methods=['GET'])
@CustomJWTVerifier.verify_jwt_token
def get_usergroups(my_id, is_admin=False):
    name, = FlaskUtils.get_url_args('name')
    # search for given str in indexed text-fields.
    filters = {}
    if name:
        filters = {
            '$text': {
                '$search': name,
                '$caseSensitive': False,
                '$diacriticSensitive': False,   # treat é, ê the same as e
            }}

    return app.make_response(db.retrieve(Usergroup, filters=filters))


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
    messages = ListField(required=False, blank=True)

    def fake_info(self):
        f = Faker()
        # give it a random 1 - 3 word name
        self.name = ' '.join([str.title(f.word()) for i in range(Random().randint(1, 3))])
        return self

    class Meta:
        write_concern = WriteConcern(j=True)
        connection_alias = 'my-app'
