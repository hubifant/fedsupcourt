# -*- coding: utf-8 -*-

from collections import Counter
import re


class KeywordExtractorPipeline(object):

    patterns_international_treaties = {
        'de': [r'(?:international)\w*[\s\-]?(?:abkommen|p[aä]kt|\w*recht|übereinkommen|vertr[aä]g)\w*',
               r'(?:völkerrecht|staat)\w*[\s\-]?(?:abkommen|p[aä]kt|übereinkommen|vertr[aä]g)\w*',
               r'(?:[^\s\(\)\,\.]+ |[^\s\(\)\,\.]+)?(?:abkommen|übereinkommen|vertr[aä]g)\w*'],
        'fr': [r'(?:accord|contrat|convention|pacte|trait[ée])\w*[\s\-]internationa\w*',
               r'(?:accord|convention|pacte|traité)(?:s|es)?'
               '(?: (?:d\'|de la |de |des |sur (?:le|la|les) )[^\s\(\)\,\.]+| [^\s\(\)\,\.]+|(?=\W))'],
        'it': [r'(?:accord|convenzion|patt|trattat)\w*[\s\-](?:internazional|di stato)\w*',
               r'(?:convenzion[ei]|(?:accord|patt|trattat)[oi])'
               '(?: (?:d\'|di |(?:de|su)(?:lla|l|i|gli)? |per (?:il|la|gli|i) )[^\s\(\)\,\.]+| [^\s\(\)\,\.]+|(?=\W))']
    }

    def process_item(self, ruling, spider):
        # find out, if ruling mentions international law
        extracted_keywords = []
        contexts = []

        # ruling chapters from which keywords will be extracted:
        chapters = ['core_issue', 'statement_of_affairs', 'paragraph']

        for pattern_language, patterns in self.patterns_international_treaties.items():
            for pattern in patterns:
                for chapter in chapters:
                    if chapter in ruling:
                        extracted_keywords.extend(re.findall(pattern, ruling[chapter], re.IGNORECASE))

        # count each keyword's number of occurences
        # todo: counts can be wrong if same word is detected multiple times
        keywords_and_counts = dict(Counter(extracted_keywords))

        # if keywords have been found, extract the entire sentences in which they occur.
        if len(extracted_keywords) > 0:
            print('INTERNATIONAL TREATY DETECTED :-D')

            for keyword in keywords_and_counts.keys():
                # build regex
                # todo improve regex
                sentence_pattern = r'(?:^|(?<=\.|\n|\t))[^\.\n\t]*'  # start of a sentence
                sentence_pattern += re.escape(keyword)               # the keyword
                sentence_pattern += r'[^\.\n\t]*(?:\.|$|(?=\n|\t))'  # end of a sentence

                # find and save contexts
                for chapter in chapters:
                    if chapter in ruling:
                        sentences = re.findall(sentence_pattern, ruling[chapter], re.IGNORECASE)
                        contexts.extend([{'chapter': chapter, 'sentence': sentence} for sentence in sentences])

            print(keywords_and_counts)
            print(contexts)
            print('\n\n===================================================================================================')

            ruling['international_treaties'] = {
                'keywords': keywords_and_counts,
                'contexts': contexts
            }

        return ruling



