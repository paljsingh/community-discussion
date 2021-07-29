
from flask import Flask


class CustomFlask(Flask):
    def __init__(self, name):
        super().__init__(name)

    # override process_response to suppress default response headers.
    def process_response(self, response):
        # hide server info.
        response.headers['server'] = "Custom Web Server"
        super(CustomFlask, self).process_response(response)
        return response

