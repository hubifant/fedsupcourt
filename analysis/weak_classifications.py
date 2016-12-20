# this script is for querying those rulings from which only few keywords were extracted


import pymongo
from datetime import datetime
from analysis.counts import save_result
from collections import OrderedDict


mongo_uri = 'mongodb://localhost:27017'
database_name = 'fedsupcourt'
collection_name = 'rulings'

date_limit = datetime.strptime('1.7.2016', '%d.%m.%Y')

client = pymongo.MongoClient(mongo_uri)
db = client[database_name]
collection = db[collection_name]

# SETTINGS:
first_year = 1874
year_group_size = 1

weak_classifications = collection.aggregate([
    {
        '$match': {
            'date': {'$lt': date_limit},
            'extracted_laws': {'$exists': 0}
        }
    },
    {
        '$project': {
            'international_treaties.clear': '$international_treaties.clear',
            'international_customary_law.clear': '$international_customary_law.clear',
            'international_law_in_general.clear': '$international_law_in_general.clear',
            'nb_kw_international_treaties': {
                '$size': {"$ifNull": ['$international_treaties.clear.keywords', []]}
            },
            'nb_kw_international_customary_law': {
                '$size': {"$ifNull": ['$international_customary_law.clear.keywords', []]}
            },
            'nb_kw_international_law_in_general': {
                '$size': {"$ifNull": ['$international_law_in_general.clear.keywords', []]}
            }
        }
    },
    {
        '$project': {
            'extracted_keyword_and_context': {
                '$ifNull': [
                    '$international_treaties.clear',
                    {
                        '$ifNull': [
                            '$international_customary_law.clear',
                            '$international_law_in_general.clear',
                        ]
                    }
                ]
            },
            'nb_distinct_keywords': {
                '$add': [
                    '$nb_kw_international_treaties',
                    '$nb_kw_international_customary_law',
                    '$nb_kw_international_law_in_general'
                ]
            }
        }
    },
    {
        '$match': {
            'nb_distinct_keywords': 1
        }
    },
    {
        '$project': {
            'extracted_keyword': {'$arrayElemAt': ['$extracted_keyword_and_context.keywords.keyword', 0]},
            'count': {'$arrayElemAt': ['$extracted_keyword_and_context.keywords.count', 0]},
            'extracted_keyword_count': '$extracted_keyword_and_context.keyword.count',
            'contexts': '$extracted_keyword_and_context.contexts.sentence'
        }
    },
    {
        '$sort':
            {'_id': 1}
    }
])


key_mapping = OrderedDict()
key_mapping['_id'] = 'Ruling'
key_mapping['extracted_keyword'] = 'Extracted Keyword'
key_mapping['count'] = 'Number Occurrences'
key_mapping['contexts'] = 'Contexts'

save_result(weak_classifications, key_mapping, 'weak_classifications')