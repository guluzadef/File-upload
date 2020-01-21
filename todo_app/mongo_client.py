from kombu.utils import json
from pymongo import MongoClient
from bson.json_util import loads as bson_loads, dumps as bson_dumps
from bson.objectid import ObjectId


class Repo(object):
    def __init__(self):
        self.client = MongoClient('mongodb://localhost:27017/api_test')
        self.db = self.client.api_test

    @staticmethod
    def find(collection, o_id):
        cls = Repo()
        return cls.db[collection].find_one({'_id': ObjectId(o_id)})

    @staticmethod
    def search(collection, params):
        cls = Repo()
        return json.loads(bson_dumps(cls.db[collection].find(params)))

    @staticmethod
    def find_all(collection):
        cls = Repo()
        return bson_dumps(cls.db[collection].find({}))

    @staticmethod
    def delete(collection):
        cls = Repo()
        cls.db[collection].remove({})
        return True

    @staticmethod
    def put(collection, query, data):
        cls = Repo()
        return cls.db[collection].update_one(query, data)


    @staticmethod
    def save(collection, data):
        cls = Repo()
        obj_id = cls.db[collection].insert_one(data).inserted_id
        obj = Repo.find(collection, obj_id)
        return json.loads(bson_dumps(obj))
