# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import re


class KeywordsExtractorPipeline(object):

    patterns_international_treaties = {
        'de': r'(?:international|völkerrecht)\w*[\s\-]?(?:abkommen|p[aä]kt|übereinkommen|vertr)\w*',
        'fr': r'(?:accord|contrat|convention|pacte|trait[eé])\w*[\s\-]internationa\w*',
        'it': r'(?:accord|convenzion|patt|trattat)\w*[\s\-]internazional\w*'
    }

    def process_item(self, item, spider):
        # find out, if ruling mentions international law
        matches = []
        occurences = []

        for pattern_language, pattern in self.patterns_international_treaties.items():
            matches.extend(re.findall(pattern, item['core_issue'], re.IGNORECASE))
            matches.extend(re.findall(pattern, item['statement_of_affairs'], re.IGNORECASE))
            matches.extend(re.findall(pattern, item['consideration'], re.IGNORECASE))

            # if matches have been found, extract the entire sentence in which the match occurs.
            if len(matches) > 0:
                sentence_pattern = r'(^|(?<=\.|\n|\t))[^\.\n\t]*'    # start of a sentence
                sentence_pattern += pattern                          # the keyword
                sentence_pattern += r'[^\.\n\t]*(?:\.|$|(?=\n|\t))'  # end of a sentence
                occurences.extend(re.findall(sentence_pattern, item['core_issue'], re.IGNORECASE))
                occurences.extend(re.findall(sentence_pattern, item['statement_of_affairs'], re.IGNORECASE))
                occurences.extend(re.findall(sentence_pattern, item['consideration'], re.IGNORECASE))

                print('WOOHOOOOOOOOOOOOOOOOO :-D')
                print(matches)
                print(occurences)
                print('\n\n===================================================================================================')
        return item


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

