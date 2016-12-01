# -*- coding: utf-8 -*-

import csv
import pymongo
from pprint import pprint


mongo_uri = 'mongodb://localhost:27017'
database_name = 'fedsupcourt'
collection_name = 'rulings'

client = pymongo.MongoClient(mongo_uri)
db = client[database_name]
collection = db[collection_name]

print(collection.count())


def save_keyword_list(keyword_type, path='.'):
    file_path = path + '/' + keyword_type + '.csv'
    result = collection.aggregate([
        {'$project': {'kw': '$' + keyword_type + '.keywords.keyword'}},
        {'$unwind': '$kw'},
        {
            '$group': {
                '_id': {
                    '$toLower': "$kw"
                },
                'occurrences': {
                    '$sum': 1
                }
            }
        },
        {'$sort': {'_id': 1}}
    ])

    keyword_list = []
    with open(file_path, 'w') as csv_file:
        keyword_writer = csv.DictWriter(csv_file, quoting=csv.QUOTE_NONNUMERIC, fieldnames=["Keyword", "Occurrences"])
        keyword_writer.writeheader()

        for row in result:
            keyword_list.append(row)
            keyword_writer.writerow({"Keyword": row['_id'], "Occurrences": row["occurrences"]})
            print('%-50s | %3d' % (row['_id'], row['occurrences']))

    return keyword_list

international_treaties = save_keyword_list('international_treaties')
save_keyword_list('international_law_in_general')
save_keyword_list('international_customary_law')
print(len(international_treaties))


count_containing_field = lambda keyword_type: collection.find({keyword_type: {'$exists': 1}}).count()
count_language = lambda language: collection.find({'language': language}).count()

print(count_containing_field('international_treaties'))
print(count_containing_field('international_customary_law'))
print(count_containing_field('international_law_in_general'))
print('===============================================')

print('Language:')
print(count_containing_field('language'))
print(count_language('de'))
print(count_language('fr'))
print(count_language('it'))
print(count_language('rr'))
print('===============================================')

print('Department                                                                       | Count')
print('---------------------------------------------------------------------------------+------')
result = collection.aggregate([
    {'$group': {
        '_id': "$department",
        'count': {'$sum': 1}}
    },
    {'$sort': {'_id': 1}}
])

for keyword in result:
    international_treaties.append(keyword)
    print('%-80s | %5d' % (keyword['_id'], keyword['count']))


result = collection.find({'ruling_id.bge_nb': 95, 'ruling_id.volume': 'III', 'ruling_id.ruling_nb': 76},
                         {'title_of_judgement': 1, 'date': 1, 'type_of_proceeding': 1, 'language': 1, 'department': 1,
                          'dossier_number': 1, 'involved_parties': 1, 'url': 1})
print(result.count())
for i, r in enumerate(result):
    pprint(r, width=300)
    if i > 1:
        break
client.close()