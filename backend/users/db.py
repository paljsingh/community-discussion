from pymongo import MongoClient
import logging

logger = logging.getLogger(__name__)


class Db:
    def __init__(self, db_uri=None, db_name=None):
        if db_uri is None or db_name is None:
            logger.error("db_uri or db_name not provided.")
            return

        client = MongoClient(db_uri)
        self.db_obj = client[db_name]

    def get_db(self):
        return self.db_obj

    def get_collection(self, collection_name):
        return self.db_obj.get_collection(collection_name)

    def save(self, document, collection_name=None):
        if collection_name is None:
            logger.error("no collection name provided.")
            return
        self.db_obj.get_collection(collection_name).insert(document)

    def retrieve(self, filters: dict, collection_name=None):
        if collection_name is None:
            logger.error("no collection name provided.")
            return

        return self.db_obj.get_collection(collection_name).find(filters)
