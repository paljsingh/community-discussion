from pymongo import MongoClient
import logging
from common.config import Config


class Db(MongoClient):
    conf = Config.load()

    def __init__(self, **kwargs):
        super().__init__(self.conf.get('db_uri'), **kwargs)
        self.logger = logging.getLogger(__name__)
        self.db = self.get_database(self.conf.get('db_name'))

    def save(self, document, collection_name):
        self.db.get_collection(collection_name).insert(document)

    def retrieve(self, collection_name, filters: dict = None, select_columns: dict = None, skip=0, limit=None):
        if not filters:
            filters = {}

        cols_filter = None
        if select_columns:
            cols_filter = {x: 1 for x in select_columns}

        default_per_page = self.conf.get('default_per_page', 10)
        if not limit:
            # no limit specified, revert to default.
            limit = default_per_page
        else:
            # restrict to a max limit, do not let users specify an arbitrarily high limit.
            limit = min(limit, self.conf.get('max_per_page', 100))

        return {
            'data': [x for x in self.db.get_collection(collection_name).find(filters, cols_filter,
                                                                             skip=skip, limit=limit)],
            'pagination': {
                'total': self.db.get_collection(collection_name).count(),
                'perPage': limit,
                'currentPage': skip // limit
            }
        }
