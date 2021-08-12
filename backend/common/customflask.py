from flask_cors import CORS
from flask import Flask

from common.config import Config
from common.db import Db


class CustomFlask(Flask):
    def __init__(self, name):
        super().__init__(name)
        self.conf = Config.load()
        self.secret_key = self.conf.get('secret_key')
        CORS(self)
        self.db = Db()

    # override process_response to suppress default response headers.
    def process_response(self, response):
        # hide server info.
        response.headers['server'] = "Custom Web Server"
        super(CustomFlask, self).process_response(response)
        return response

