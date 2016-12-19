# this script is for comparing a manual ruling evaluations with the automatic evaluations

import csv
import pymongo
from datetime import datetime
from collections import OrderedDict
from analysis.court_department_categories import department_mapping


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


negative_samples_path = '../data/manual_coding_negative_samples.csv'
negative_samples = []

positive_samples_path = '../data/manual_coding_positive_samples.csv'
positive_samples = []

with open(negative_samples_path, 'r') as csv_file:
    negative_reader = csv.reader(csv_file)
    for row in negative_reader:
        negative_samples.append(row[0].replace('BGE ', ''))

with open(positive_samples_path, 'r') as csv_file:
    positive_reader = csv.reader(csv_file)
    for row in positive_reader:
        positive_samples.append(row[0].replace('BGE ', ''))

print(negative_samples)
print(positive_samples)


true_positives_list = collection.find({
    '_id': {
        '$in': positive_samples
    },
    '$or': [
        {'international_treaties.clear': {'$exists': 1}},
        {'international_customary_law.clear': {'$exists': 1}},
        {'international_law_in_general.clear': {'$exists': 1}},
        {'extracted_laws': {'$exists': 1}},
    ]
})

true_positive_count = true_positives_list.count()
print(true_positive_count)

false_negatives_list = collection.find({
    '_id': {
        '$in': positive_samples
    },
    'international_treaties.clear': {'$exists': 0},
    'international_customary_law.clear': {'$exists': 0},
    'international_law_in_general.clear': {'$exists': 0},
    'extracted_laws': {'$exists': 0}
})

false_negative_count = false_negatives_list.count()
print(false_negative_count)

false_negative_pcnt = (100 * false_negative_count / (false_negative_count + true_positive_count))
true_positive_pcnt = 100 - false_negative_pcnt
print(false_negative_pcnt)


false_positives_list = collection.find({
    '_id': {
        '$in': negative_samples
    },
    '$or': [
        {'international_treaties.clear': {'$exists': 1}},
        {'international_customary_law.clear': {'$exists': 1}},
        {'international_law_in_general.clear': {'$exists': 1}},
        {'extracted_laws': {'$exists': 1}},
    ]
})

false_positive_count = false_positives_list.count()
print(false_positive_count)

true_negatives_list = collection.find({
    '_id': {
        '$in': negative_samples
    },
    'international_treaties.clear': {'$exists': 0},
    'international_customary_law.clear': {'$exists': 0},
    'international_law_in_general.clear': {'$exists': 0},
    'extracted_laws': {'$exists': 0}
})

true_negative_count = true_negatives_list.count()
print(true_negative_count)

true_negative_pcnt = (100 * true_negative_count / (true_negative_count + true_positive_count))
false_positive_pcnt = 100 - true_negative_pcnt
print(false_positive_pcnt)

