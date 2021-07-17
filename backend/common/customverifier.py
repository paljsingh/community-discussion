import json
from functools import wraps
from typing import Callable

from flask import request
from okta_jwt_verifier import JWTVerifier
from werkzeug.exceptions import BadRequest, Unauthorized

from common.config import Config


class CustomJWTVerifier:

    config = Config.load()

    @classmethod
    def verify_jwt_token(cls, func: Callable):
        @wraps(func)
        async def inner(*args, **kwargs):
            def raiser(ex, *args, **kwargs):
                print("Exception! {}".format(str(ex)))
                # raise ex
                return CustomJWTVerifier.handle_error(ex)

            if request.headers.get('Authorization') and ' ' in request.headers.get('Authorization'):
                jwt_token = request.headers.get('Authorization').split(' ')[1]
                try:
                    jwt_verifier = JWTVerifier(
                        cls.config.get('issuer'), cls.config.get('client_id'), cls.config.get('audience'))
                    await jwt_verifier.verify_access_token(jwt_token)
                    print("jwt token verified!")
                    return func(*args, **kwargs)
                except Exception:
                    return raiser(BadRequest)
            else:
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


