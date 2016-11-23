# -*- coding: utf-8 -*-

from collections import Counter
import re


class KeywordExtractorPipeline(object):

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
            keywords.extend(re.findall(pattern, item['statement_of_affairs'], re.IGNORECASE))
            keywords.extend(re.findall(pattern, item['paragraph'], re.IGNORECASE))

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
                sentences_in_soa = re.findall(sentence_pattern, item['statement_of_affairs'], re.IGNORECASE)
                sentences_in_p = re.findall(sentence_pattern, item['paragraph'], re.IGNORECASE)

                # save entire context
                contexts.extend([{'chapter': 'Core Issue', 'sentence': sentence} for sentence in sentences_in_ci])
                contexts.extend([{'chapter': 'Statement of Affairs', 'sentence': sentence} for sentence in sentences_in_soa])
                contexts.extend([{'chapter': 'Paragraph', 'sentence': sentence} for sentence in sentences_in_p])

            print(keywords_and_counts)
            print(contexts)
            print('\n\n===================================================================================================')

            item['international_law'] = {
                'keywords': keywords_and_counts,
                'contexts': contexts
            }

        return item



