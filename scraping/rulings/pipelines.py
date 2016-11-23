# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from collections import Counter
import json
import re


class KeywordsExtractorPipeline(object):

    patterns_international_treaties = {
        'de': r'(?:international|völkerrecht)\w*[\s\-]?(?:abkommen|p[aä]kt|\w*recht|übereinkommen|vertr)\w*',
        'fr': r'(?:accord|contrat|convention|pacte|trait[eé])\w*[\s\-]internationa\w*',
        'it': r'(?:accord|convenzion|patt|trattat)\w*[\s\-]internazional\w*'
    }

    def process_item(self, item, spider):
        # find out, if ruling mentions international law
        keywords = []
        contexts = []

        for pattern_language, pattern in self.patterns_international_treaties.items():
            keywords.extend(re.findall(pattern, item['core_issue'], re.IGNORECASE))
            keywords.extend(re.findall(pattern, item['paragraph'], re.IGNORECASE))
            keywords.extend(re.findall(pattern, item['consideration'], re.IGNORECASE))

        # count each keyword's number of occurences
        keywords_and_counts = dict(Counter(keywords))

        # if keywords have been found, extract the entire sentences in which they occur.
        if len(keywords) > 0:
            print('INTERNATIONAL TREATY DETECTED :-D')

            for kw in set(keywords):
                # build regex
                sentence_pattern = r'(?:^|(?<=\.|\n|\t))[^\.\n\t]*'  # start of a sentence
                sentence_pattern += re.escape(kw)                    # the keyword
                sentence_pattern += r'[^\.\n\t]*(?:\.|$|(?=\n|\t))'  # end of a sentence

                # find sentences
                sentences_in_ci = re.findall(sentence_pattern, item['core_issue'], re.IGNORECASE)
                sentences_in_p = re.findall(sentence_pattern, item['paragraph'], re.IGNORECASE)
                sentences_in_c = re.findall(sentence_pattern, item['consideration'], re.IGNORECASE)

                # save entire context
                contexts.extend([{'chapter': 'Core Issue', 'sentence': sentence} for sentence in sentences_in_ci])
                contexts.extend([{'chapter': 'Paragraph', 'sentence': sentence} for sentence in sentences_in_p])
                contexts.extend([{'chapter': 'Consideration', 'sentence': sentence} for sentence in sentences_in_c])

            print(keywords_and_counts)
            print(contexts)
            print('\n\n===================================================================================================')

            item['international_law'] = {
                'keywords': keywords_and_counts,
                'contexts': contexts
            }

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

