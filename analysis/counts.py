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

def save_result(result, mongo_csv_key_mapping, result_name, path='.', verbose=False):
    file_path = path + '/' + result_name + '.csv'

    with open(file_path, 'w') as csv_file:
        keyword_writer = csv.DictWriter(csv_file,
                                        quoting=csv.QUOTE_ALL,
                                        fieldnames=mongo_csv_key_mapping.values())
        keyword_writer.writeheader()

        for mongo_row in result:

            # first, build csv row from mongo row
            csv_row = {}
            for mongo_key, csv_key in mongo_csv_key_mapping.items():
                if csv_key is 'Year':
                    csv_row[csv_key] = int(mongo_row[mongo_key])
                else:
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
                                    {'$add': ['$ruling_id.bge_nb', first_year]},
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

save_result(per_year, key_mapping, 'counts_per_year')



per_year_and_sr_nb = collection.aggregate([
    {
        '$match': {
            'date': {'$lt': date_limit}
        }
    },
    {
        '$unwind': {
            'path': '$extracted_laws'
        }
    },
    {
        '$group': {
            '_id': {
                'year': {
                    '$multiply': [
                        {
                            '$floor': {
                                '$divide': [
                                    {'$add': ['$ruling_id.bge_nb', first_year]},
                                    year_group_size
                                ]
                            }
                        },
                        year_group_size
                    ],
                },
                'sr_number': '$extracted_laws.law'
            },
            'count': {
                '$sum': 1
            }
        }
    },
    {
        '$project': {
            'year': '$_id.year',
            'sr_number': '$_id.sr_number',
            'count': '$count'
        }
    },
    {
        '$sort': {
            '_id.year': 1,
            '_id.sr_number': 1
        }
    }
])
key_mapping_yr_sr = OrderedDict()
key_mapping_yr_sr['year'] = 'Year'
key_mapping_yr_sr['sr_number'] = 'Law (SR-Number)'
key_mapping_yr_sr['count'] = 'Count'
save_result(per_year_and_sr_nb, key_mapping_yr_sr, 'counts_per_year_and_sr_number')


per_year_dep_and_sr_nb = collection.aggregate([
    {
        '$match': {
            'date': {'$lt': date_limit}
        }
    },
    {
        '$unwind': {
            'path': '$extracted_laws'
        }
    },
    {
        '$project': {
            'extracted_laws': '$extracted_laws',
            'year': {
                    '$multiply': [
                        {
                            '$floor': {
                                '$divide': [
                                    {'$add': ['$ruling_id.bge_nb', first_year]},
                                    year_group_size
                                ]
                            }
                        },
                        year_group_size
                    ],
                },
            'department': {
                '$cond': {
                    'if': {'$lt': ['$_id.year', 1995]},
                    'then': {
                        '$cond': {
                            'if': {
                                '$or': [
                                    {'$eq': ['$ruling_id.volume', 'I']},
                                    {'$eq': ['$ruling_id.volume', 'IA']},
                                    {'$eq': ['$ruling_id.volume', 'IB']},
                                ]

                            },
                            'then': 'Constitutional, Administrative and International Public Law',
                            'else': {
                                '$cond': {
                                    'if': {
                                        '$or': [
                                            {'$eq': ['$ruling_id.volume', 'II']},
                                            {'$eq': ['$ruling_id.volume', 'III']}
                                        ]
                                    },
                                    'then': 'Private Law (including Debt Recovery and Bankruptcy)',
                                    'else': {
                                        '$cond': {
                                            'if': {'$eq': ['$ruling_id.volume', 'IV']},
                                            'then': 'Criminal  Law  and  Criminal  Enforcement Law',
                                            'else': 'Social Insurance Law'
                                        }
                                    }
                                }
                            }
                        }
                    },
                    'else': {
                        '$cond': {
                            'if': {
                                '$or': [
                                    {'$eq': ['$ruling_id.volume', 'I']},
                                    {'$eq': ['$ruling_id.volume', 'II']}
                                ]
                            },
                            'then': 'Constitutional, Administrative and International Public Law',
                            'else': {
                                '$cond': {
                                    'if': {'$eq': ['$ruling_id.volume', 'III']},
                                    'then': 'Private Law (including Debt Recovery and Bankruptcy)',
                                    'else': {
                                        '$cond': {
                                            'if': {'$eq': ['$ruling_id.volume', 'IV']},
                                            'then': 'Criminal  Law  and  Criminal  Enforcement Law',
                                            'else': 'Social Insurance Law'
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    },
    {
        '$group': {
            '_id': {
                'year': '$year',
                'sr_number': '$extracted_laws.law',
                'department': '$department'
            },
            'count': {
                '$sum': 1
            }
        }
    },
    {
        '$project': {
            'year': '$_id.year',
            'sr_number': '$_id.sr_number',
            'count': '$count',
            'department': '$_id.department'
        }
    },
    {
        '$sort': {
            'year': 1,
            'department': 1,
            '_id.sr_number': 1
        }
    }
])
key_mapping_yr_dep_sr = OrderedDict()
key_mapping_yr_dep_sr['year'] = 'Year'
key_mapping_yr_dep_sr['department'] = 'Department'
key_mapping_yr_dep_sr['sr_number'] = 'Law (SR-Number)'
key_mapping_yr_dep_sr['count'] = 'Count'
save_result(per_year_dep_and_sr_nb, key_mapping_yr_dep_sr, 'counts_per_year_dep_and_sr_number')


per_year_and_department = collection.aggregate([
    {
        '$match': {
            'date': {'$lt': date_limit}
        }
    },
    {
        '$project': {
            'international_treaties.clear': '$international_treaties.clear',
            'international_customary_law.clear': '$international_customary_law.clear',
            'international_law_in_general.clear': '$international_law_in_general.clear',
            'extracted_laws': '$extracted_laws',
            'year': {
                    '$multiply': [
                        {
                            '$floor': {
                                '$divide': [
                                    {'$add': ['$ruling_id.bge_nb', first_year]},
                                    year_group_size
                                ]
                            }
                        },
                        year_group_size
                    ],
                },
            'department': {
                '$cond': {
                    'if': {'$lt': ['$_id.year', 1995]},
                    'then': {
                        '$cond': {
                            'if': {
                                '$or': [
                                    {'$eq': ['$ruling_id.volume', 'I']},
                                    {'$eq': ['$ruling_id.volume', 'IA']},
                                    {'$eq': ['$ruling_id.volume', 'IB']},
                                ]

                            },
                            'then': 'Constitutional, Administrative and International Public Law',
                            'else': {
                                '$cond': {
                                    'if': {
                                        '$or': [
                                            {'$eq': ['$ruling_id.volume', 'II']},
                                            {'$eq': ['$ruling_id.volume', 'III']}
                                        ]
                                    },
                                    'then': 'Private Law (including Debt Recovery and Bankruptcy)',
                                    'else': {
                                        '$cond': {
                                            'if': {'$eq': ['$ruling_id.volume', 'IV']},
                                            'then': 'Criminal  Law  and  Criminal  Enforcement Law',
                                            'else': 'Social Insurance Law'
                                        }
                                    }
                                }
                            }
                        }
                    },
                    'else': {
                        '$cond': {
                            'if': {
                                '$or': [
                                    {'$eq': ['$ruling_id.volume', 'I']},
                                    {'$eq': ['$ruling_id.volume', 'II']}
                                ]
                            },
                            'then': 'Constitutional, Administrative and International Public Law',
                            'else': {
                                '$cond': {
                                    'if': {'$eq': ['$ruling_id.volume', 'III']},
                                    'then': 'Private Law (including Debt Recovery and Bankruptcy)',
                                    'else': {
                                        '$cond': {
                                            'if': {'$eq': ['$ruling_id.volume', 'IV']},
                                            'then': 'Criminal  Law  and  Criminal  Enforcement Law',
                                            'else': 'Social Insurance Law'
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    },
    {
        '$group': {
            '_id': {
                'year': '$year',
                'department': '$department'
            },
            'total': {
                '$sum': 1
            },
            'international_law': {
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
            }
        }
    },
    {
        '$project': {
            'year': '$_id.year',
            'department': '$_id.department',
            'total': '$total',
            'international_law': '$international_law',
            'relevant_pcnt': {'$divide': ['$international_law', '$total']},
            'int_treaty_extracted': '$int_treaty_extracted',
            'int_cust_law_extracted': '$int_cust_law_extracted'
        }
    },
    {
        '$sort': {
            'year': 1,
            'relevant_pcnt': -1
        }
    }
])
key_mapping_dep = OrderedDict()
key_mapping_dep['year'] = 'Year'
key_mapping_dep['department'] = 'Department'
key_mapping_dep['total'] = 'Total Number of Decisions'
key_mapping_dep['international_law'] = 'Number of Decisions referring to International Law'
key_mapping_dep['relevant_pcnt'] = 'Share of Decisions referring to International Law'
key_mapping_dep['int_treaty_extracted'] = 'Rulings referring to International Treaties'
key_mapping_dep['int_cust_law_extracted'] = 'Rulings referring to International Customary Law'
save_result(per_year_and_department, key_mapping_dep, 'counts_per_year_and_department')
