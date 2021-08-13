from http import HTTPStatus
from random import Random
from typing import List

import uuid
import logging.config
from faker import Faker
from datetime import datetime
from common.customflask import CustomFlask
from common.customverifier import CustomJWTVerifier
from werkzeug.exceptions import HTTPException, abort
from flask import request
from common.utils import FlaskUtils

logging.config.fileConfig('../logging.conf')
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = CustomFlask(__name__)
conf = app.conf
db = app.db


for cls in HTTPException.__subclasses__():
    app.register_error_handler(cls, CustomJWTVerifier.handle_error)


@app.route("/api/v1/communities/new", methods=['POST'])
@CustomJWTVerifier.verify_jwt_token
def create_new_community(my_id, is_admin=False):

    data = request.get_json()
    new_community = Community(my_id).fake_info()

    # override with any data available in the post body.
    if data and data.get('name'):
        new_community.with_name(data.get('name'))
    if data and data.get('tags'):
        new_community.with_tags(data.get('tags'))
    if data and data.get('users'):
        new_community.with_users(data.get('users'))
    new_community.save()
    return app.make_response(new_community.__dict__())


@app.route("/api/v1/communities", methods=['GET'])
@CustomJWTVerifier.verify_jwt_token
def get_all_communities(my_id, is_admin=False):
    skip, limit = FlaskUtils.get_skip_limit()
    communities = db.retrieve("communities", skip=skip, limit=limit)
    return app.make_response(communities)


@app.route('/api/v1/communities/<community_id>', methods=['GET'])
@CustomJWTVerifier.verify_jwt_token
def get_community(community_id, my_id, is_admin=False):
    community = db.retrieve("communities", {'_id': community_id}, limit=1)
    return app.make_response(community)


@app.route('/api/v1/communities/<community_id>/users/<user_id>/invite', methods=['POST'])
@CustomJWTVerifier.verify_jwt_token
def invite_user_to_community(community_id, user_id, my_id, is_admin=False):
    community = db.retrieve("communities", {'_id': community_id}, limit=1)
    invites = db.retrieve("invites", {'invite_for': 'communities', 'invite_for_resource_id': community_id,
                                     'invite_by': my_id, 'invite_to': user_id}, limit=1).get('data')

    # no such invite exists, create one.
    if not invites:
        invite = Invite(community_id, 'communities').with_invite_by(my_id).with_invite_to(user_id)
        invite_id = invite._id
        invite.save()
    else:
        invite = invites[0]
        invite_id = invite['_id']
    resp = app.make_response(community)
    resp.headers['Location'] = '/api/v1/communities/{}/users/{}/invite/{}'.format(
        community_id, user_id, invite_id)
    return resp


@app.route('/api/v1/communities/<community_id>/invite/<invite_id>/accept', methods=['PUT'])
@CustomJWTVerifier.verify_jwt_token
def accept_invite_to_community(community_id, invite_id, my_id, is_admin=False):
    community = db.retrieve("communities", {'_id': community_id}, limit=1)

    # accept the invite
    invites = db.retrieve("invites", {'_id': invite_id}, limit=1).get('data')
    if invites:
        invite = invites[0]
        if my_id != invite['invite_to']:    # ensure, only the intended user can accept the invite.
            abort(HTTPStatus.FORBIDDEN)

        invite['status'] = 'accepted'
        invite['updated_on'] = datetime.utcnow().timestamp()
        invite.save()

        # add user to the community list
        community['users'].update(my_id)
        community.save()

        resp = app.make_response(community)
        resp.headers['Location'] = '/api/v1/communities/{}'.format(community_id)
        return resp
    else:   # lost invite ?
        return app.make_response({})


@app.route('/api/v1/communities/<community_id>/invite/<invite_id>/decline', methods=['PUT'])
@CustomJWTVerifier.verify_jwt_token
def decline_invite_to_community(community_id, invite_id, my_id, is_admin=False):
    # decline the invite
    invite = db.retrieve("invites", {'_id': invite_id}, limit=1).get('data')
    if invite:
        invite['status'] = 'declined'
        invite['updated_on'] = datetime.utcnow().timestamp()
        invite.save()

    return app.make_response({})


@app.route('/api/v1/communities/<community_id>/subscribe', methods=['PUT'])
@CustomJWTVerifier.verify_jwt_token
def subscribe_to_community(community_id, my_id, is_admin=False):
    community = db.retrieve("communities", {'_id': community_id}, limit=1)

    # TODO: any history updates / events here.

    # add user to the community list
    community['users'].update(my_id)
    resp = app.make_response(community)
    resp.headers['Location'] = '/api/v1/communities/{}'.format(community_id)
    return resp


@app.route('/api/v1/communities/<community_id>/unsubscribe', methods=['PUT'])
@CustomJWTVerifier.verify_jwt_token
def unsubscribe_to_community(community_id, my_id, is_admin=False):
    community = db.retrieve("communities", {'_id': community_id}, limit=1)

    # TODO: any history updates / events here.

    # add user to the community list
    community['users'].remove(my_id)
    return app.make_response({})


@app.route('/api/v1/communities/search', methods=['GET'])
@CustomJWTVerifier.verify_jwt_token
def search_community(my_id, is_admin=False):
    name, = FlaskUtils.get_url_args('name')

    skip, limit = FlaskUtils.get_skip_limit()

    # search for given str in indexed text-fields.
    communities = db.retrieve('communities', {
        '$text': {
            '$search': name,
            '$caseSensitive': False,
            '$diacriticSensitive': False,   # treat é, ê the same as e
        }}, limit=limit, skip=skip)
    # TODO: any history updates / events here.

    return app.make_response(communities)

# TODO
# api to update community info
#


class Community:

    def __init__(self, created_by: str):
        self._id = '{}'.format(uuid.uuid4())
        self.name = None
        self.creation_date = datetime.utcnow().timestamp()
        self.created_by = created_by
        self.tags = set()
        self.users = set()
        self.usergroups = set()
        pass

    def fake_info(self):
        f = Faker()
        self.name = ' '.join([str.capitalize(f.word()) for i in range(2)])
        self.tags = set([f.word() for i in range(Random().randint(1, 5))])
        return self

    def with_name(self, name: str):
        self.name = name
        return self

    def with_tags(self, tags: List):
        self.tags = tags
        return self

    def with_created_by(self, name: str):
        self.name = name
        return self

    def with_users(self, users: List):
        self.users.update(users)
        return self

    def __dict__(self):
        return {
            '_id': self._id,
            'name': self.name,
            'tags': list(self.tags),
            'creation_date': self.creation_date,
            'created_by': self.created_by,
            'users': list(self.users),
            'usergroups': list(self.usergroups)
        }

    def save(self):
        db.save(self.__dict__(), 'communities')


class Invite:

    def __init__(self, resource_id, resource_type):
        self._id = '{}'.format(uuid.uuid4())
        self.invite_for = resource_type     # 'community', 'usergroup' ...
        self.invite_for_resource_id = resource_id   # id of the community / usergroup / ..
        self.creation_date = datetime.utcnow().timestamp()
        self.status = 'pending'
        self.updated_on = datetime.utcnow().timestamp()
        self.invite_by = None
        self.invite_to = None
        pass

    def with_invite_by(self, invite_by: str):
        self.invite_by = invite_by
        return self

    def with_invite_to(self, invite_to: str):
        self.invite_to = invite_to
        return self

    def __dict__(self):
        return {
            '_id': self._id,
            'creation_date': self.creation_date,
            'invite_by': self.invite_by,
            'invite_to': self.invite_to,
            'invite_for': self.invite_for,
            'invite_for_resource_id': self.invite_for_resource_id,
            'status': self.status,
            'updated_on': self.updated_on
        }

    def save(self):
        db.save(self.__dict__(), 'invites')

    @staticmethod
    def get(filters):
        skip, limit = FlaskUtils.get_skip_limit()
        db.retrieve('invites', filters=filters, skip=skip, limit=limit)