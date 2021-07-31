from datetime import datetime
from werkzeug.exceptions import HTTPException, BadRequest
from faker import Faker
from flask import request
import uuid

from common.pagination import Pagination
from common.customflask import CustomFlask
from common.customverifier import CustomJWTVerifier

app = CustomFlask(__name__)
conf = app.conf
db = app.db

for cls in HTTPException.__subclasses__():
    app.register_error_handler(cls, CustomJWTVerifier.handle_error)


@app.route("/api/v1/usergroups/new", methods=['POST'])
@CustomJWTVerifier.verify_jwt_token
def create_usergroup(is_admin=False):
    # create a new usergroup - use uuid for unique identifier.
    usergroup_id = '{}'.format(uuid.uuid4())
    f = Faker()
    usergroup_name = '{}-{}'.format(f.word(), f.word())

    user_id = CustomJWTVerifier.get_userid(CustomJWTVerifier.get_token())

    user_ids = set()
    if not is_admin:
        user_ids.add(user_id)

    try:
        if request.get_json() and request.get_json().get('user_ids'):
            user_ids.update(request.get_json().get('user_ids'))
    except BadRequest as ex:
        print("expected json data: {}".format(ex))

    if user_ids:
        usergroup_users = db.get_collection('users').find({"_id": {"$in": user_ids}})
    else:
        usergroup_users = []

    usergroup_info = {
        "_id": usergroup_id,
        "name": usergroup_name,
        "created_by": user_id,
        "created_on": datetime.utcnow().timestamp(),
        "users": usergroup_users,
    }
    db.save(usergroup_info, 'usergroups')

    # send response
    return app.make_response(usergroup_info)


@app.route("/api/v1/usergroups", methods=['GET'])
@CustomJWTVerifier.verify_jwt_token
def get_all_usergroups(is_admin=False):
    if is_admin:
        usergroups = Pagination.get_paginated_records("usergroups")
    else:
        usergroups = Pagination.get_paginated_records("usergroups", ["_id", "name", "users"])
        for ug in usergroups:
            for user in ug.get('users'):
                filtered_user = {"_id": user.get("_id"), "name": user.get("name")}
                ug['users'] = filtered_user
    # send response
    return app.make_response(usergroups)
