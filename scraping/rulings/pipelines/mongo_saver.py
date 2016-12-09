# -*- coding: utf-8 -*-
# from: https://doc.scrapy.org/en/latest/topics/item-pipeline.html#write-items-to-mongodb

import pymongo


class MongoSaverPipeline(object):

    def __init__(self, mongo_uri, mongo_db, collection_name, indexes):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.collection_name = collection_name
        self.indexes = indexes

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'fedsupcourt'),
            indexes=crawler.settings.get('MONGO_INDEXES', []),
            collection_name=crawler.settings.get('MONGO_COLLECTION')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

        # set up index
        if self.indexes:
            create_index_model = lambda idx: pymongo.IndexModel([(idx['field'], 1)],
                                                                name=idx['idx_name'],
                                                                unique=idx.get('unique', False))
            index_generator = map(create_index_model, self.indexes)
            self.db[self.collection_name].create_indexes(list(index_generator))  # indices need to be passed in a list

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        self.db[self.collection_name].insert(dict(item))
        return item
