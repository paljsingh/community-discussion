from urllib.parse import urlparse, parse_qs, ParseResult, urlencode
from flask import request

from common.config import Config


class FlaskUtils:

    conf = Config.load()
    query_params = {
        'perPage': {
            'type': int,
            'default': conf.get('default_per_page', 10)
        },
        'page': {
            'type': int,
            'default': 1
        },
        'name': {
            'type': str,
            'default': ''
        },
    }

    @staticmethod
    def update_url(key: str, value):
        """
        Create a new url with page index updated.
        :param key:
        :param value:
        :return:
        """
        u = urlparse(request.url)
        params = parse_qs(u.query)
        params[key] = value
        res = ParseResult(scheme=u.scheme, netloc=u.hostname, path=u.path, params=u.params, query=urlencode(params),
                          fragment=u.fragment, typename="")  # https://youtrack.jetbrains.com/issue/PY-22102
        return res.geturl()

    @staticmethod
    def get_url_args(*arg_keys):
        return tuple(FlaskUtils.query_params[k]['type'](request.args.get(k))
                     if request.args.get(k) else FlaskUtils.query_params[k]['default'] for k in arg_keys)

    @staticmethod
    def get_skip_limit():
        per_page, current_page = FlaskUtils.get_url_args('perPage', 'page')
        per_page = min(per_page, FlaskUtils.conf.get('max_per_page'))
        print("perPage: {}, page: {}".format(per_page, current_page))
        skip = (current_page - 1) * per_page
        limit = per_page
        return skip, limit
