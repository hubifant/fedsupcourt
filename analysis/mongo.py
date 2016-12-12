# -*- coding: utf-8 -*-

import csv
import pymongo


mongo_uri = 'mongodb://localhost:27017'
database_name = 'fedsupcourt'
collection_name = 'rulings'

client = pymongo.MongoClient(mongo_uri)
db = client[database_name]
collection = db[collection_name]


def save_keyword_list(keyword_type, path='.', verbose=False):
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

            if verbose:
                print('%-50s | %3d' % (row['_id'], row['occurrences']))

    return keyword_list

international_treaties_c = save_keyword_list('international_treaties.clear')
international_treaties_b = save_keyword_list('international_treaties.broad')
save_keyword_list('international_law_in_general.broad')
save_keyword_list('international_law_in_general.clear')
save_keyword_list('international_customary_law.broad')
save_keyword_list('international_customary_law.clear')
# print(len(international_treaties))


count_containing_field = lambda keyword_type: collection.find({keyword_type: {'$exists': 1}}).count()
count_language = lambda language: collection.find({'language': language}).count()

print('Keyword Counts: ')
print('Total Number of Rulings:              %5d' % collection.count())
print('International Treaties (clear):       %5d' % count_containing_field('international_treaties.clear'))
print('International Treaties (broad):       %5d' % count_containing_field('international_treaties.broad'))
print('International Customary Law (clear):  %5d' % count_containing_field('international_customary_law.clear'))
print('International Customary Law (broad):  %5d' % count_containing_field('international_customary_law.broad'))
print('International Law in General (clear): %5d' % count_containing_field('international_law_in_general.clear'))
print('International Law in General (broad): %5d' % count_containing_field('international_law_in_general.broad'))
print('===================================')

print('Language:')
print('Total Number of Rulings:                   %5d' % collection.count())
print('Number of Rulings with extracted Language: %5d' % count_containing_field('language'))
print('German:                                    %5d' % count_language('de'))
print('French:                                    %5d' % count_language('fr'))
print('Italian:                                   %5d' % count_language('it'))
print('Rhaeto-Romance:                            %5d' % count_language('rr'))
print('================================================')



def save_departments(path='.', verbose=False):
    departments = collection.aggregate([
        {'$group': {
            '_id': "$department",
            'count': {'$sum': 1}}
        },
        {'$sort': {'_id': 1}}
    ])

    department_list = []

    with open(path + '/departments.csv', 'w') as csv_file:
        department_writer = csv.DictWriter(csv_file,
                                           quoting=csv.QUOTE_NONNUMERIC,
                                           fieldnames=["Department", "Occurrences"])
        department_writer.writeheader()

        if verbose:
            print('Department                                                                       | Count')
            print('---------------------------------------------------------------------------------+------')

        for dep in departments:
            if dep['_id'] is None:
                dep['_id'] = 'Department not extractable'
            department_writer.writerow({'Department': dep['_id'], 'Occurrences': dep['count']})
            department_list.append(dep)
            if verbose:
                print('%-80s | %5d' % (dep['_id'], dep['count']))

    return department_list

# save_departments()


def count_by_year(keyword_type, path='.', verbose=False):
    file_path = path + '/' + keyword_type + '_by_year' + '.csv'
    count_variable = 'rulings_applying_' + keyword_type
    result = collection.aggregate([
        {'$match': {keyword_type: {'$exists': 1}}},
        {
            '$group': {
                '_id': '$ruling_id.bge_nb',
                count_variable: {
                    '$sum': 1
                }
            }
        },
        {'$sort': {'_id': 1}}
    ])

    year_list = []
    with open(file_path, 'w') as csv_file:
        keyword_writer = csv.DictWriter(csv_file, quoting=csv.QUOTE_NONNUMERIC, fieldnames=["Keyword", count_variable])
        keyword_writer.writeheader()

        for row in result:
            year_list.append(row)
            keyword_writer.writerow({"Keyword": row['_id'], count_variable: row[count_variable]})

            if verbose:
                print('%-50s | %3d' % (row['_id'], row[count_variable]))

    return year_list

count_by_year('international_customary_law')
count_by_year('international_law_in_general')
count_by_year('extracted_laws')



# result = collection.find({'ruling_id.bge_nb': 95, 'ruling_id.volume': 'III', 'ruling_id.ruling_nb': 76},
#                          {'title_of_judgement': 1, 'date': 1, 'type_of_proceeding': 1, 'language': 1, 'department': 1,
#                           'dossier_number': 1, 'involved_parties': 1, 'url': 1})
# print(result.count())
# for i, r in enumerate(result):
#     pprint(r, width=300)
#     if i > 1:
#         break




client.close()