# -*- coding: utf-8 -*-

import pymongo


mongo_uri = 'mongodb://localhost:27017'
database_name = 'fedsupcourt'
collection_name = 'rulings'

client = pymongo.MongoClient(mongo_uri)
db = client[database_name]
collection = db[collection_name]

print(collection.count())

client.close()