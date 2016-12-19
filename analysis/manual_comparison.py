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

print('\n\nReading manual results...')

with open(negative_samples_path, 'r') as csv_file:
    negative_reader = csv.reader(csv_file)
    for row in negative_reader:
        id = row[0].replace('BGE ', '').upper()
        if id not in negative_samples:
            negative_samples.append(id)
        else:
            print("\tDouble negative sample: " + row[0])

with open(positive_samples_path, 'r') as csv_file:
    positive_reader = csv.reader(csv_file)
    for row in positive_reader:
        id = row[0].replace('BGE ', '').upper()
        if id not in positive_samples:
            positive_samples.append(id)
        else:
            print("\tDouble positive sample: " + row[0])

print('\n')

nb_negative_samples = len(negative_samples)
nb_positive_samples = len(positive_samples)
print('Positive Samples: %3d' % nb_negative_samples)
print('Negative Samples: %3d' % nb_positive_samples)
print('---------------------------------')


true_positives = collection.find({
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
false_negatives = collection.find({
    '_id': {
        '$in': positive_samples
    },
    'international_treaties.clear': {'$exists': 0},
    'international_customary_law.clear': {'$exists': 0},
    'international_law_in_general.clear': {'$exists': 0},
    'extracted_laws': {'$exists': 0}
})
false_positives = collection.find({
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
true_negatives = collection.find({
    '_id': {
        '$in': negative_samples
    },
    'international_treaties.clear': {'$exists': 0},
    'international_customary_law.clear': {'$exists': 0},
    'international_law_in_general.clear': {'$exists': 0},
    'extracted_laws': {'$exists': 0}
})


true_positive_count = true_positives.count()
true_negative_count = true_negatives.count()
false_positive_count = false_positives.count()
false_negative_count = false_negatives.count()

true_positive_pcnt = (100 * true_positive_count / nb_positive_samples)
false_negative_pcnt = 100 - true_positive_pcnt
true_negative_pcnt = (100 * true_negative_count / nb_negative_samples)
false_positive_pcnt = 100 - true_negative_pcnt
print('%3d true positives:  %6.2f%%' % (true_positive_count, true_positive_pcnt))
print('%3d false positives: %6.2f%%' % (false_positive_count, false_positive_pcnt))
print('%3d true negatives:  %6.2f%%' % (true_negative_count, true_negative_pcnt))
print('%3d false negatives: %6.2f%%' % (false_negative_count, false_negative_pcnt))
print('=================================')


true_count = true_positive_count + true_negative_count
false_count = false_positive_count + false_negative_count
true_pcnt = 100 * true_count / (true_count + false_count)
false_pcnt = 100 * false_count / (true_count + false_count)
print('%3d correctly classified: %6.2f%%' % (true_count, true_pcnt))
print('%3d wrongly classified:   %6.2f%%' % (false_count, false_pcnt))


print('\nFalse Positives:')
for ruling in false_positives:
    print(" - " + ruling['_id'])

print('\nFalse Negatives:')
for ruling in false_negatives:
    print(" - " + ruling['_id'])
print('\n\n')


for id in negative_samples:
    result = collection.find_one({'_id': id})
    if result is None:
        print('Could not find negative sample %s in database.' % id)

for id in positive_samples:
    result = collection.find_one({'_id': id})
    if result is None:
        print('Could not find positive sample %s in database.' % id)
