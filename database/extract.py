import pymongo
from extraction import SRNumberExtractor
import logging
import time


ruling_chapters = ['core_issue', 'statement_of_affairs', 'paragraph']

def extract_and_save_sr_numbers(mongo_uri='mongodb://localhost:27017',
                                db_name='fedsupcourt',
                                int_law_collection_name='rulings'):

    start_time = time.clock()

    client = pymongo.MongoClient(mongo_uri)
    ruling_collection = client[db_name][int_law_collection_name]

    # ruling_cursor = ruling_collection.find({'_id.bge_nb': 136}, modifiers={"$snapshot": True})
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

        # update the processed ruling
        ruling_to_update = {'_id': ruling['_id']}
        update_result = ruling_collection.replace_one(ruling_to_update, ruling)

        # raise error if the ruling was not updated.
        if update_result.matched_count == 0 or update_result.modified_count == 0:
            raise Exception('Could not update ruling ' + str(ruling['_id']) + '!')

        if i > nb_rulings:
            print('Updated ruling %s.' % str(ruling['_id']))

    end_time = time.clock()

    print('Running Time: %.3f' % (end_time - start_time))
