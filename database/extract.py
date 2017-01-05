import pymongo
from extraction import SRNumberExtractor, InternationalTreatyExtractor, InternationalCustomaryLawExtractor, \
    GeneralInternationalLawExtractor, MetadataExtractor
import logging
import time


ruling_chapters = ['core_issue', 'statement_of_affairs', 'paragraph']

def extract_and_save_sr_numbers(mongo_uri='mongodb://localhost:27017',
                                db_name='fedsupcourt',
                                int_law_collection_name='rulings'):

    start_time = time.clock()

    client = pymongo.MongoClient(mongo_uri)
    ruling_collection = client[db_name][int_law_collection_name]

    # ruling_cursor = ruling_collection.find({'ruling_id.bge_nb': 136}, modifiers={"$snapshot": True})
    ruling_cursor = ruling_collection.find({}, modifiers={"$snapshot": True})
    nb_rulings = ruling_cursor.count()
    print('Extracting SR numbers from %d rulings...' % nb_rulings)

    extractor = SRNumberExtractor()

    percentage_to_print = 0
    percentage_to_print_stepsize = 5

    for i, ruling in enumerate(ruling_cursor):
        if i/nb_rulings * 100 > percentage_to_print:
            print('%2d%% of the rulings processed. (%d/%d)' % (percentage_to_print, i, nb_rulings))
            percentage_to_print += percentage_to_print_stepsize

        extracted_laws = []
        extracted_categories = []
        for chapter in ruling_chapters:
            if chapter in ruling:
                laws, categories = extractor.extract_sr_numbers(ruling[chapter])

                for law in laws:
                    if law not in extracted_laws:
                        extracted_laws.append(law)
                for category in categories:
                    if category not in extracted_categories:
                        extracted_categories.append(category)

        if len(extracted_laws) > 0:
            ruling['extracted_laws'] = extracted_laws
        if len(extracted_categories) > 0:
            ruling['extracted_categories'] = extracted_categories

        ruling_collection.save(ruling)
        logging.info('Updated ruling %s.' % str(ruling['ruling_id']))

    end_time = time.clock()

    print('Running Time: %.3f' % (end_time - start_time))


def extract_and_save_keywords(mongo_uri='mongodb://localhost:27017',
                              db_name='fedsupcourt',
                              int_law_collection_name='rulings'):
    start_time = time.clock()

    client = pymongo.MongoClient(mongo_uri)
    ruling_collection = client[db_name][int_law_collection_name]

    # ruling_cursor = ruling_collection.find({'ruling_id.bge_nb': 136}, modifiers={"$snapshot": True})
    ruling_cursor = ruling_collection.find({}, modifiers={"$snapshot": True})
    nb_rulings = ruling_cursor.count()
    print('Extracting SR numbers from %d rulings...' % nb_rulings)

    int_treaty_extractor = InternationalTreatyExtractor()
    int_cust_law_extractor = InternationalCustomaryLawExtractor()
    int_law_in_gen_extractor = GeneralInternationalLawExtractor()

    percentage_to_print = 0
    percentage_to_print_stepsize = 5

    for i, ruling in enumerate(ruling_cursor):
        if i/nb_rulings * 100 > percentage_to_print:
            print('%2d%% of the rulings processed. (%d/%d)' % (percentage_to_print, i, nb_rulings))
            percentage_to_print += percentage_to_print_stepsize

        ruling = int_treaty_extractor.extract(ruling)
        ruling = int_cust_law_extractor.extract(ruling)
        ruling = int_law_in_gen_extractor.extract(ruling)

        ruling_collection.save(ruling)
        logging.info('Updated ruling %s.' % str(ruling['ruling_id']))

    end_time = time.clock()
    print('Running Time: %.3fs = %.2fm' % (end_time - start_time, (end_time - start_time)/60))


def extract_and_save_metadata(mongo_uri='mongodb://localhost:27017',
                              db_name='fedsupcourt',
                              int_law_collection_name='rulings'):
    start_time = time.clock()

    client = pymongo.MongoClient(mongo_uri)
    ruling_collection = client[db_name][int_law_collection_name]

    # ruling_cursor = ruling_collection.find({'ruling_id.bge_nb': 136}, modifiers={"$snapshot": True})
    ruling_cursor = ruling_collection.find({}, modifiers={"$snapshot": True})
    nb_rulings = ruling_cursor.count()
    print('Extracting SR numbers from %d rulings...' % nb_rulings)

    metadata_extractor = MetadataExtractor()

    percentage_to_print = 0
    percentage_to_print_stepsize = 5

    for i, ruling in enumerate(ruling_cursor):
        if i/nb_rulings * 100 > percentage_to_print:
            print('%2d%% of the rulings processed. (%d/%d)' % (percentage_to_print, i, nb_rulings))
            percentage_to_print += percentage_to_print_stepsize

        ruling = metadata_extractor.extract(ruling)

        ruling_collection.save(ruling)
        logging.info('Updated ruling %s.' % str(ruling['ruling_id']))

    end_time = time.clock()
    print('Running Time: %.3fs = %.2fm' % (end_time - start_time, (end_time - start_time)/60))