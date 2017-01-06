import pymongo
from extraction import SRNumberExtractor, CombinedKeywordExtractor, MetadataExtractor
import logging
import time


def map_rulings(map_function,
                mongo_uri='mongodb://localhost:27017',
                db_name='fedsupcourt',
                ruling_collection_name='rulings'):
    """
    Iterates over ruling database and applies map_function to each ruling. The processed ruling is then saved in the
    database.
    """
    start_time = time.clock()

    client = pymongo.MongoClient(mongo_uri)
    ruling_collection = client[db_name][ruling_collection_name]

    # ruling_cursor = ruling_collection.find({'ruling_id.bge_nb': 136}, modifiers={"$snapshot": True})
    ruling_cursor = ruling_collection.find({}, modifiers={"$snapshot": True})
    nb_rulings = ruling_cursor.count()
    print('%d rulings will be processed...' % nb_rulings)

    percentage_to_print = 0
    percentage_to_print_stepsize = 5

    for i, ruling in enumerate(ruling_cursor):
        if i / nb_rulings * 100 > percentage_to_print:
            print('\t%2d%% of the rulings processed. (%d/%d)' % (percentage_to_print, i, nb_rulings))
            percentage_to_print += percentage_to_print_stepsize

        ruling = map_function(ruling)

        ruling_collection.save(ruling)
        logging.info('Updated ruling %s.' % str(ruling['ruling_id']))

    end_time = time.clock()
    print('Running Time: %.3fs = %.2fm' % (end_time - start_time, (end_time - start_time) / 60))


def extract_and_save_sr_numbers():
    """
    Extracts SR numbers from each ruling and saves them in the database
    """
    extractor = SRNumberExtractor()
    ruling_chapters = ['core_issue', 'statement_of_affairs', 'paragraph']

    def extract_sr_numbers(ruling):
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

        return ruling

    map_rulings(extract_sr_numbers)


def extract_and_save_keywords():
    """
    Extracts keywords from each ruling and saves them in the database
    """
    kw_extractor = CombinedKeywordExtractor()
    map_rulings(kw_extractor.extract)


def extract_and_save_metadata():
    """
    Extracts metadata from each ruling and saves it in the database
    """
    metadata_extractor = MetadataExtractor()
    map_rulings(metadata_extractor.extract)