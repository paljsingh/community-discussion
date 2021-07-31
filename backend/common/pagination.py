from typing import List
from urllib.parse import urlparse, parse_qs, ParseResult, urlencode

from flask import request

from common.config import Config
from common.db import Db

conf = Config.load()
db = Db(conf.get('db_uri'), conf.get('db_name'))


class Pagination:

    @classmethod
    def _per_page_with_limit(cls):
        """
        If query parameter exist, return number of items specified in query parameter, subject to a max
        configurable limit (or hardcoded number 100)
        :return:
        """
        items_per_page = int(request.args.get("itemsPerPage", conf.get("default_per_page", 10)))
        return min(items_per_page, conf.get('max_per_page', 100))

    @classmethod
    def _pagination_info(cls, collection_name: str):
        total_records = db.get_collection(collection_name).count()
        items_per_page = cls._per_page_with_limit()
        current_page = int(request.args.get("page", 1))
        return {
            "total": total_records,
            "itemsPerPage": items_per_page,
            "page": current_page,
        }

    @classmethod
    def get_paginated_records(cls, collection_name: str, include_columns: List = None):
        pinfo = cls._pagination_info(collection_name)
        skip_records = (pinfo['page'] - 1) * pinfo['itemsPerPage']
        if include_columns:
            cols_dict = {x: 1 for x in include_columns}
            data = [name for name in db.get_collection(collection_name).find(
                {}, cols_dict, skip=skip_records, limit=pinfo['itemsPerPage'])]
        else:
            data = [name for name in
                    db.get_collection(collection_name).find(skip=skip_records, limit=pinfo['itemsPerPage'])]

        return {
            "pagination": pinfo,
            "data": data
        }

    @classmethod
    def get_page_url(cls, current_page: int):
        """
        Create a new url with page index updated.
        :param current_page:
        :return:
        """
        u = urlparse(request.url)
        params = parse_qs(u.query)
        params['page'] = current_page     # noqa
        res = ParseResult(scheme=u.scheme, netloc=u.hostname, path=u.path, params=u.params, query=urlencode(params),
                          fragment=u.fragment)  # noqa  - https://youtrack.jetbrains.com/issue/PY-22102
        return res.geturl()

