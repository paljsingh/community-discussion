from datetime import datetime
from http import HTTPStatus

from werkzeug.exceptions import HTTPException, BadRequest, abort
from faker import Faker
from flask import request
import uuid

from common.customflask import CustomFlask
from common.customverifier import CustomJWTVerifier
from common.utils import FlaskUtils
from users.app import User

app = CustomFlask(__name__)
conf = app.conf
db = app.db

for cls in HTTPException.__subclasses__():
    app.register_error_handler(cls, CustomJWTVerifier.handle_error)


@app.route("/api/v1/communities/<community_id>/usergroups/new", methods=['POST'])
@CustomJWTVerifier.verify_jwt_token
def create_usergroup(community_id, my_id, is_admin=False):
    user_ids = None
    try:
        json_content = request.get_json()
        if not (json_content and json_content.get('user_ids')):
            abort(HTTPStatus.BAD_REQUEST, 'must provide user id(s)')
        user_ids = json_content.get('user_ids')
    except BadRequest as ex:
        print("expected json data: {}".format(ex))

    usergroup_users = set()
    usergroup_users.update(User.get(my_id))
    for user_id in user_ids:
        usergroup_users.update(User.get(user_id))

    # create a new usergroup - use uuid for unique identifier.
    usergroup_id = '{}'.format(uuid.uuid4())
    f = Faker()
    usergroup_name = '{}-{}'.format(f.word(), f.word())

    print("cug: usergroup_users: {}".format(usergroup_users))
    usergroup_info = {
        "_id": usergroup_id,
        "name": usergroup_name,
        "created_by": my_id,
        "created_on": datetime.utcnow().timestamp(),
        "users": usergroup_users,
    }
    print("cug: usergroup_info: {}".format(usergroup_info))
    db.save(usergroup_info, 'usergroups')

    # update community for list of usergroups
    community = db.retrieve('communities', filters={'_id': community_id}, limit=1)
    community['usergroups'].update(usergroup_id)
    db.save(community, 'communities')

    return app.make_response(usergroup_info)


@app.route("/api/v1/usergroups", methods=['GET'])
@CustomJWTVerifier.verify_jwt_token
def get_usergroups(my_id, is_admin=False):
    """
    :param is_admin: if admin, return all data for the user groups.
    for non-admins, return only the public data.
    :return:
    """
    filters = None
    if request.args.get('q'):
        filters = request.args.get('q')

    skip, limit = FlaskUtils.get_skip_limit()
    if is_admin:
        usergroups = db.retrieve("usergroups", filters=filters, skip=skip, limit=limit)
    else:
        usergroups = db.retrieve("usergroups", select_columns=["_id", "name", "users"], filters=filters,
                                 skip=skip, limit=limit)
        for ug in usergroups:
            for user in ug.get('users'):
                filtered_user = {"_id": user.get("_id"), "name": user.get("name")}
                ug['users'] = filtered_user
    # send response
    return app.make_response(usergroups)


