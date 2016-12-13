import csv
import pymongo
from datetime import datetime
from collections import OrderedDict


mongo_uri = 'mongodb://localhost:27017'
database_name = 'fedsupcourt'
collection_name = 'rulings'

date_limit = datetime.strptime('1.10.2016', '%d.%m.%Y')

client = pymongo.MongoClient(mongo_uri)
db = client[database_name]
collection = db[collection_name]

# SETTINGS:
year_group_size = 10

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



per_year = collection.aggregate([
    {
        '$match': {
            'date': {'$lt': date_limit}
        }
    },
    {
        '$group': {
            '_id': {
                '$multiply': [
                    {
                        '$floor': {
                            '$divide': [
                                {'$year': '$date'},
                                year_group_size
                            ]
                        }
                    },
                    year_group_size
                ]
            },
            'total_number_of_decisions': {
                '$sum': 1
            },
            'sr_nb_extracted': {
                '$sum': {
                    '$cond': [{"$ifNull": ["$extracted_laws", False]}, 1, 0]
                }
            },
            'int_treaty_extracted': {
                '$sum': {
                    '$cond': [{"$ifNull": ["$international_treaties.clear", False]}, 1, 0]
                }
            },
            'int_cust_law_extracted': {
                '$sum': {
                    '$cond': [{"$ifNull": ["$international_customary_law.clear", False]}, 1, 0]
                }
            },
            'int_law_in_gen_extracted': {
                '$sum': {
                    '$cond': [{"$ifNull": ["$international_law_in_general.clear", False]}, 1, 0]
                }
            },
            'relevant_rulings_only_kws': {
                '$sum': {
                    '$cond': [
                        {
                            "$or": [
                                {"$ifNull": ["$international_treaties.clear", False]},
                                {"$ifNull": ["$international_customary_law.clear", False]},
                                {"$ifNull": ["$international_law_in_general.clear", False]}
                            ]
                        }, 1, 0
                    ]
                }
            },
            'relevant_rulings': {
                '$sum': {
                    '$cond': [
                        {
                            "$or": [
                                {"$ifNull": ["$international_treaties.clear", False]},
                                {"$ifNull": ["$international_customary_law.clear", False]},
                                {"$ifNull": ["$international_law_in_general.clear", False]},
                                {"$ifNull": ["$extracted_laws", False]}
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


key_mapping = OrderedDict()
key_mapping['_id'] = 'Year'
key_mapping['total_number_of_decisions'] = 'Total Number of Decisions'
key_mapping['int_treaty_extracted'] = 'Rulings referring to International Treaties'
key_mapping['int_cust_law_extracted'] = 'Rulings referring to International Customary Law'
key_mapping['int_law_in_gen_extracted'] = 'Rulings referring to International Law in General'
key_mapping['sr_nb_extracted'] = 'SR-Number extracted'
key_mapping['relevant_rulings_only_kws'] = 'Total Number of Rulings referring to International Law'
key_mapping['relevant_rulings'] = 'Total Number of Rulings referring to International Law (incl. SR-Numbers)'

save_result(per_year, key_mapping, 'yearwise')