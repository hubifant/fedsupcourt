from analysis.keyword_statistics import save_result
from collections import OrderedDict
from datetime import datetime
import pymongo

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


no_language = collection.find(
    {
        'date': {'$lt': date_limit},
        'language': {'$exists': 0}
    },
    {
        '_id': 1,
        'title_of_judgement': 1
    }
)

print('Language could not be extracted from %d rulings.' % no_language.count())

key_mapping = OrderedDict()
key_mapping['_id'] = 'BGE'
key_mapping['title_of_judgement'] = 'Title of Judgement'
save_result(no_language, key_mapping, 'manual_language_determination')


referring_to_cust_int_law = collection.aggregate([
    {
        '$match': {
            'date': {'$lt': date_limit},
            'international_customary_law.clear': {'$exists': 1}
        }
    },
    {
        '$project': {
            '_id': '$_id',
            'url': '$url',
            'keywords': '$international_customary_law.clear.keywords.keyword'
        }
    }
])

key_mapping = OrderedDict()
key_mapping['_id'] = 'BGE'
key_mapping['keywords'] = 'Extracted Keywords referring to International Customary Law'
key_mapping['url'] = 'Link'

save_result(referring_to_cust_int_law, key_mapping, 'referring_to_customary_international_law')