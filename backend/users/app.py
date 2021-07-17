#!/usr/bin/env python3
import logging.config

from flask_cors import CORS

from werkzeug.exceptions import HTTPException

from common.config import Config
from common.customflask import CustomFlask
from common.customverifier import CustomJWTVerifier

logging.config.fileConfig('./logging.conf')
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = CustomFlask(__name__)
CORS(app)

config = Config.load()
for cls in HTTPException.__subclasses__():
    app.register_error_handler(cls, CustomJWTVerifier.handle_error)


@app.route("/api/v1/users/new", methods=['POST'])
@CustomJWTVerifier.verify_jwt_token
def create_new_user():
    return app.create_new_user()


@app.route("/api/v1/users", methods=['GET'])
@CustomJWTVerifier.verify_jwt_token
def get_all_users():
    return app.get_all_users()
