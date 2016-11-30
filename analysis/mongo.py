# -*- coding: utf-8 -*-

import pymongo
from pprint import pprint


mongo_uri = 'mongodb://localhost:27017'
database_name = 'fedsupcourt'
collection_name = 'rulings'

client = pymongo.MongoClient(mongo_uri)
db = client[database_name]
collection = db[collection_name]

print(collection.count())

result = collection.aggregate([
    {'$project': {'kw': '$international_treaties.keywords.keyword'}},
    {'$unwind': '$kw'},
    {'$group': {
        '_id': "$kw",
        'count': {'$sum': 1}}
    },
    {'$sort': {'_id': 1}}
])

international_treaties = []

for keyword in result:
    international_treaties.append(keyword)
    print('%-50s | %3d' % (keyword['_id'], keyword['count']))

print(len(international_treaties))


client.close()