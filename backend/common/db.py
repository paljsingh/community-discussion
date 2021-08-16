from pymodm.connection import connect
from common.config import Config
from common.utils import FlaskUtils
from typing import Dict, List


class Db:

    def __init__(self):
        self.conf = Config.load()
        self.db = connect(self.conf.get('db_uri'), alias="my-app")

    def retrieve(self, collection, filters: Dict = None, select_columns: List = None, to_son=True, pagination=True):    # noqa
        (skip, limit) = FlaskUtils.get_skip_limit()
        (page, per_page) = FlaskUtils.get_url_args('page', 'perPage')

        query = collection.objects
        if select_columns:
            query = query.only(*select_columns)

        if filters:
            query = query.raw(filters)

        items = [x.to_son() if to_son else x for x in query.skip(skip).limit(limit)]
        total_items = collection.objects.count()

        if pagination:
            return {
                'data': items,
                'pagination': {
                    'total': total_items,
                    'page': page,
                    'perPage': per_page
                }
            }
        else:
            return items

    def get(self, collection, id_val=None, filters=None, select_columns=None, to_son=True):     # noqa
        if id_val is None and filters is None:
            print("either id_val or filters must be specified.")
            return
        query = collection.objects

        if select_columns:
            query = query.only(*select_columns)

        try:
            if id_val:
                item = query.get({'_id': id_val})
            else:
                item = query.get(filters)
            if to_son:
                return item.to_son()
            else:
                return item
        except collection.DoesNotExist as ex:
            # no item found
            return
