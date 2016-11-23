# -*- coding: utf-8 -*-

import json


class JsonWriterPipeline(object):

    def open_spider(self, spider):
        # open data file when spider is started (make sure that encoding is correct)
        self.file = open('../data/rulings.json', 'w+', encoding='utf-8')

    def close_spider(self, spider):
        # close data file when spider is done
        self.file.close()

    def process_item(self, item, spider):
        # write item to datafile
        line = json.dumps(dict(item), ensure_ascii=False) + "\n"
        self.file.write(line)
        return item
