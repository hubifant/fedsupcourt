import csv
import pymongo
from datetime import datetime


mongo_uri = 'mongodb://localhost:27017'
database_name = 'fedsupcourt'
collection_name = 'rulings'

date_limit = datetime.strptime('1.10.2016', '%d.%m.%Y')

client = pymongo.MongoClient(mongo_uri)
db = client[database_name]
collection = db[collection_name]


def save_result(result, mongo_csv_key_mapping, result_name, path='.', verbose=False):
    file_path = path + '/' + result_name + '.csv'

    with open(file_path, 'w') as csv_file:
        keyword_writer = csv.DictWriter(csv_file,
                                        quoting=csv.QUOTE_NONNUMERIC,
                                        fieldnames=mongo_csv_key_mapping.values())
        keyword_writer.writeheader()

        for mongo_row in result:

            # first, build csv row from mongo row
            csv_row = {}
            for mongo_key, csv_key in mongo_csv_key_mapping.items():
                csv_row[csv_key] = mongo_row[mongo_key]

            keyword_writer.writerow(csv_row)

            # if verbose:
            #     print('%-50s | %3d' % (mongo_row['_id'], mongo_row['occurrences']))

test = collection.find_one({'date': {'$lt': date_limit}}, {'date': 1})
print(test)

per_year = collection.aggregate([
    {
        '$match': {
            'date': {'$lt': date_limit}
        }
    },
    {
        '$group': {
            '_id': {
                '$year': '$date'
            },
            'total_number_of_decisions': {
                '$sum': 1
            },
            'relevant_rulings': {
                '$sum': {
                    '$cond': [
                        {
                            "$or": [
                                {"$ifNull": ["$international_treaties.clear", False]},
                                {"$ifNull": ["$international_customary_law.clear", False]},
                                {"$ifNull": ["$international_law_in_general.clear", False]},
                                {"$ifNull": ["$extracted_laws", False]},
                            ]
                        }, 1, 0
                    ]
                }
            }
        }
    },
    {
        '$sort': {
            '_id': 1
        }
    }
])

per_year_1 = collection.aggregate([
    {
        '$match': {
            'date': {'$lt': date_limit},
            '$or': [
                {'international_treaties.clear': {'$exists': 1}},
                {'international_customary_law.clear': {'$exists': 1}},
                {'international_law_in_general.clear': {'$exists': 1}},
                {'extracted_laws': {'$exists': 1}}
            ]
        }
    },
    {
        '$group': {
            '_id': {
                '$year': '$date'
            },
            'relevant_rulings': {
                '$sum': 1
            }
        }
    },
    {
        '$sort': {
            '_id': 1
        }
    }
])


save_result(per_year, {'_id': 'Year', 'relevant_rulings': 'Relevant Rulings'}, 'yearwise')
save_result(per_year_1, {'_id': 'Year', 'relevant_rulings': 'Relevant Rulings'}, 'yearwise_comparison')