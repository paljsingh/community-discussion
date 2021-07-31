import json
from functools import wraps
from typing import Callable

from flask import request
from okta_jwt_verifier import JWTVerifier
from werkzeug.exceptions import BadRequest, Unauthorized
import jwt

from common.config import Config


class CustomJWTVerifier:

    config = Config.load()

    @classmethod
    def get_token(cls):
        return request.headers.get('Authorization').split(' ')[1]

    @classmethod
    def get_userid(cls, token):
        print("get_userid", jwt.decode(token,  options={"verify_signature": False}).get('sub'))
        return jwt.decode(token,  options={"verify_signature": False}).get('sub')

    @classmethod
    def verify_jwt_token(cls, func: Callable):
        @wraps(func)
        async def inner(*args, **kwargs):
            def raiser(ex, *args, **kwargs):
                print("Exception! {}".format(str(ex)))
                return CustomJWTVerifier.handle_error(ex)

            if request.headers.get('Authorization') and ' ' in request.headers.get('Authorization'):
                jwt_token = request.headers.get('Authorization').split(' ')[1]

                decoded_token = False
                is_admin = False

                # try to verify as a dummy user
                try:
                    decoded_token = jwt.decode(jwt_token, cls.config.get('secret_key'), cls.config.get('algo'))
                    is_admin = False
                    print("authenticated as dummy user")
                except Exception as ex:
                    print("failed to verify as dummy user - {}".format(ex))

                if not decoded_token:
                    # try to verify as okta user
                    try:
                        jwt_verifier = JWTVerifier(
                            cls.config.get('issuer'), cls.config.get('client_id'), cls.config.get('audience'))
                        await jwt_verifier.verify_access_token(jwt_token)
                        # no exception - all is well
                        decoded_token = True
                        is_admin = True
                        print("authenticated as okta user")
                    except Exception as ex:
                        print("failed to verify as okta user - {}".format(ex))

                if decoded_token:
                    return func(is_admin=is_admin)

                # raise exception.
                return raiser(BadRequest)
            else:
                print("no authorization header found: {}".format(request.headers))
                return raiser(Unauthorized)
        return inner

    @classmethod
    def handle_error(cls, error):
        if hasattr(error, '__name__'):
            name = error.__name__
        else:
            name = error.__class__.__name__
        code = error.code
        return json.dumps({"error": name, "code": code}), code, {'Content-Type': 'application/json'}


