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

    sentence_pattern = r'(?:^|(?<=\. )(?=[A-Z])|(?<=\n|\t))'   # Go to the beginning of a sentence
    sentence_pattern += r'(?:.(?!\. [A-Z]))*'                  # anyrything that is not followed by beginning of a sentence
    sentence_pattern += r'%s'                                  # place holder for keyword
    sentence_pattern += r'.*?(?:\.(?= [A-Z])|$|(?=\n|\t))'     # end of a sentence

    def process_item(self, ruling, spider):

        # find keywords associated to international treaties
        extracted_keywords = []
        keywords_with_counts = {}
        contexts = []

        # ruling chapters from which keywords will be extracted:
        ruling_chapters = ['core_issue', 'statement_of_affairs', 'paragraph']

        # go through all ruling chapters and extract keywords
        for chapter in ruling_chapters:
            if chapter in ruling:
                for pattern_language, patterns in self.patterns_international_treaties.items():
                    for pattern in patterns:
                        extracted_keywords.extend(re.findall(pattern, ruling[chapter], re.IGNORECASE))

        # if keywords have been found, extract the entire sentences in which they occur
        if len(extracted_keywords) > 0:
            for keyword in set(extracted_keywords):

                # pattern matches sentences containing the keyword
                keyword_context_pattern = self.sentence_pattern % re.escape(keyword)

                # find and save contexts in each chapter
                for chapter in ruling_chapters:
                    if chapter in ruling:
                        sentences = re.findall(keyword_context_pattern, ruling[chapter])  # don't IGNORECASE here!

                        # update contexts list with each extracted sentence
                        contexts.extend(
                            [{'keyword': keyword, 'chapter': chapter, 'sentence': sentence} for sentence in sentences]
                        )

                        # update keyword count (difficult to do this nicer before)
                        keywords_with_counts[keyword] = keywords_with_counts.get(keyword, 0) + len(sentences)

            ruling['international_treaties'] = {
                'keywords': keywords_with_counts,
                'contexts': contexts
            }

        return ruling



