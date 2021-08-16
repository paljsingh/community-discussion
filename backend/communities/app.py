from pymodm import MongoModel
from pymodm.fields import CharField, DateTimeField, ListField
from pymongo.write_concern import WriteConcern

from http import HTTPStatus
from random import Random

import uuid
import logging.config
from faker import Faker
from datetime import datetime
from common.customflask import CustomFlask
from common.customverifier import CustomJWTVerifier
from werkzeug.exceptions import HTTPException, abort
from flask import request

from common.db import Db
from common.utils import FlaskUtils
from usergroups.app import Usergroup

logging.config.fileConfig('../logging.conf')
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = CustomFlask(__name__)
app.config['MONGODB_SETTINGS'] = {'host': app.conf.get('db_uri')}
db = Db()


for cls in HTTPException.__subclasses__():
    app.register_error_handler(cls, CustomJWTVerifier.handle_error)


@app.route("/api/v1/communities/new", methods=['POST'])
@CustomJWTVerifier.verify_jwt_token
def create_new_community(my_id, is_admin=False):

    data = request.get_json()
    new_community = Community(created_by=my_id)
    new_community.fake_info()

    # override with any data available in the post body.
    if data and data.get('name'):
        new_community.name = data['name']
    if data and data.get('tags'):
        new_community.tags = data['tags']
    if data and data.get('users'):
        new_community.users = data['users']

    new_community.save()
    return app.make_response(new_community.to_son())


@app.route("/api/v1/communities", methods=['GET'])
@CustomJWTVerifier.verify_jwt_token
def get_communities(my_id, is_admin=False):
    """
    if name field is provided, return filtered results by matching name / tags, else
    all the communities (paginated response)
    :param my_id:
    :param is_admin:
    :return:
    """
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

    return app.make_response(db.retrieve(Community, filters=filters))


@app.route('/api/v1/communities/<community_id>', methods=['GET'])
@CustomJWTVerifier.verify_jwt_token
def get_community(community_id, my_id, is_admin=False):
    return app.make_response(db.get(Community, community_id))


@app.route('/api/v1/communities/<community_id>/users/<user_id>/invite', methods=['POST'])
@CustomJWTVerifier.verify_jwt_token
def invite_user_to_community(community_id, user_id, my_id, is_admin=False):
    community = db.get(Community, community_id)
    filters = {'invite_for_resource_type': 'community', 'invite_for_resource_id': community_id,
               'invite_by_user': my_id, 'invite_to_user': user_id}
    invite = db.get(Invite, filters=filters, to_son=False)

    # no such invite exists, create one.
    if not invite:
        invite = Invite(**filters)
        invite.save()
    invite_id = invite.id
    resp = app.make_response(community)
    resp.headers['Location'] = '/api/v1/communities/{}/users/{}/invite/{}'.format(
        community_id, user_id, invite_id)
    return resp


@app.route('/api/v1/communities/<community_id>/invite/<invite_id>/accept', methods=['PUT'])
@CustomJWTVerifier.verify_jwt_token
def accept_invite_to_community(community_id, invite_id, my_id, is_admin=False):
    community = db.get(Community, community_id, to_son=False)

    # accept the invite
    invite = db.get(Invite, invite_id, to_son=False)
    if invite:
        if my_id != invite.invite_to_user:    # ensure, only the intended user can accept the invite.
            abort(HTTPStatus.FORBIDDEN)

        if invite.status == 'accepted':
            return app.make_response({})

        invite.status = 'accepted'
        invite.updated_on = datetime.utcnow()
        invite.save()

        # add user to the community list
        community.add_user(my_id)

        resp = app.make_response(community.to_son())
        resp.headers['Location'] = '/api/v1/communities/{}'.format(community_id)
        return resp
    else:   # lost invite ?
        return app.make_response({})


@app.route('/api/v1/communities/<community_id>/invite/<invite_id>/decline', methods=['PUT'])
@CustomJWTVerifier.verify_jwt_token
def decline_invite_to_community(community_id, invite_id, my_id, is_admin=False):
    # decline the invite
    invite = db.get(Invite, invite_id, to_son=False)
    if invite:
        invite.status = 'declined'
        invite.updated_on = datetime.utcnow()
        invite.save()

    return app.make_response({})


@app.route('/api/v1/communities/<community_id>/subscribe', methods=['PUT'])
@CustomJWTVerifier.verify_jwt_token
def subscribe_to_community(community_id, my_id, is_admin=False):
    community = db.get(Community, community_id, to_son=False)

    # TODO: any history updates / events here.

    # add user to the community list
    community.add_user(my_id)

    resp = app.make_response(community.to_son())
    resp.headers['Location'] = '/api/v1/communities/{}'.format(community_id)
    return resp


@app.route('/api/v1/communities/<community_id>/unsubscribe', methods=['PUT'])
@CustomJWTVerifier.verify_jwt_token
def unsubscribe_to_community(community_id, my_id, is_admin=False):
    community = db.get(Community, community_id, to_son=False)

    # TODO: any history updates / events here.

    # add user to the community list
    community.remove_user(my_id)
    return app.make_response({})


@app.route("/api/v1/communities/mine", methods=['GET'])
@CustomJWTVerifier.verify_jwt_token
def get_my_communities(my_id, is_admin=False):
    """
    :param my_id:
    :param is_admin: if admin, return all data for the user groups.
    for non-admins, return only the public data.
    :return:
    """
    usergroups = db.retrieve(Usergroup, filters={'users': {'$in': [my_id]}}, to_son=False, pagination=False)
    if not usergroups:
        app.make_response({})

    usergroup_ids = [x['id'] for x in usergroups]
    app.make_response(db.retrieve(Community, filters={'usergroups': {'$in': usergroup_ids}}))


@app.route("/api/v1/communities/<community_id>/usergroups/new", methods=['POST'])
@CustomJWTVerifier.verify_jwt_token
def create_usergroup(community_id, my_id, is_admin=False):
    """
    Create a usergroup under a community.
    :param community_id:
    :param my_id:
    :param is_admin:
    :return:
    """
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
def get_usergroups_for_community(community_id, my_id, is_admin=False):
    """
    :param my_id:
    :param community_id:
    :param is_admin: if admin, return all data for the user groups.
    for non-admins, return only the public data.
    :return:
    """

    # find all usergroup ids in the community
    community = db.retrieve(Community, community_id, to_son=False, pagination=False)
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


# TODO
# api to update community info.
# api for invite status check.


class Community(MongoModel):
    id = CharField(required=True, primary_key=True, default=uuid.uuid4)
    name = CharField(required=True)
    created_by = CharField(required=True)
    creation_date = DateTimeField(required=True, default=datetime.utcnow)
    tags = ListField(required=False, blank=True)
    users = ListField(required=False, blank=True)
    usergroups = ListField(required=False, blank=True)

    def fake_info(self):
        f = Faker()
        self.name = ' '.join([str.capitalize(f.word()) for i in range(2)])
        self.tags = list([f.word() for i in range(Random().randint(1, 5))])

    def add_user(self, user_id):
        # add user to the community list
        s = set(self.users)
        s.add(user_id)
        self.users = list(s)
        self.save()

    def remove_user(self, user_id):
        # add user to the community list
        s = set(self.users)
        s.remove(user_id)
        if s:
            self.users = list(s)
        else:
            print("# setting to none")
            self.users = []
        self.save()

    class Meta:
        write_concern = WriteConcern(j=True)
        connection_alias = 'my-app'


class Invite(MongoModel):
    id = CharField(required=True, primary_key=True, default=uuid.uuid4)
    invite_for_resource_type = CharField(required=True)
    invite_for_resource_id = CharField(required=True)
    creation_date = DateTimeField(required=True, default=datetime.utcnow)
    status = CharField(required=False, default='pending')
    updated_on = DateTimeField(required=True, default=datetime.utcnow)
    invite_by_user = CharField(required=False)
    invite_to_user = CharField(required=False)

    class Meta:
        write_concern = WriteConcern(j=True)
        connection_alias = 'my-app'
