# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json


class RulingsPipeline(object):

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

