# -*- coding: utf-8 -*-

import re


class _KeywordExtractorPipeline:
    def __init__(self, keyword_type, keyword_patterns):
        """
        :param keyword_patterns: dict of format {'<LANGUAGE>': [r'<PATTERN_1>', r'<PATTERN_2>']}
        :type keyword_patterns: dict
        """

        self.keyword_patterns = keyword_patterns
        self.keyword_type = keyword_type

        # regex for extracting a keyword's context
        self.sentence_pattern = r'(?:^|(?<=\. )(?=[A-Z])|(?<=\n|\t))'  # beginning of a sentence
        self.sentence_pattern += r'(?:.(?!\. [A-Z]))*'  # anything NOT followed by beginning of sentence
        self.sentence_pattern += r'%s'  # keyword
        self.sentence_pattern += r'.*?(?:\.(?= [A-Z])|$|(?=\n|\t))'  # anything until end of sentence

        # ruling chapters from which keywords will be extracted:
        self.ruling_chapters = ['core_issue', 'statement_of_affairs', 'paragraph']

    def process_item(self, ruling, spider):

        # find keywords associated to international treaties
        extracted_keywords = []
        keywords_with_counts = {}
        contexts = []

        # go through all ruling chapters and extract keywords
        for chapter in self.ruling_chapters:
            if chapter in ruling:
                for pattern_language, patterns in self.keyword_patterns.items():
                    for pattern in patterns:
                        extracted_keywords.extend(re.findall(pattern, ruling[chapter], re.IGNORECASE))

        # if keywords have been found, extract the entire sentences in which they occur
        if len(extracted_keywords) > 0:
            for keyword in set(extracted_keywords):

                # pattern matches sentences containing the keyword
                keyword_context_pattern = self.sentence_pattern % re.escape(keyword)

                # find and save contexts in each chapter
                for chapter in self.ruling_chapters:
                    if chapter in ruling:
                        sentences = re.findall(keyword_context_pattern, ruling[chapter])  # don't IGNORECASE here!

                        # update contexts list with each extracted sentence
                        contexts.extend(
                            [{'keyword': keyword, 'chapter': chapter, 'sentence': sentence} for sentence in sentences]
                        )

                        # update keyword count (difficult to do this nicer before)
                        keywords_with_counts[keyword] = keywords_with_counts.get(keyword, 0) + len(sentences)

            ruling['keywords'] = {
                self.keyword_type: {
                    'keywords': keywords_with_counts,
                    'contexts': contexts
                }
            }

        return ruling


class InternationalTreatyExtractor(_KeywordExtractorPipeline):
    """
    Implements KeywordExtractorPipeline for keywords indicating the use of international treaties.
    """

    def __init__(self):
        patterns_international_treaties = {
            'de': [r'(?:international)\w*[\s\-]?(?:abkommen|p[aä]kt|\w*recht|übereinkommen|vertr[aä]g)\w*',
                   r'(?:völkerrecht|staat)\w*[\s\-]?(?:abkommen|p[aä]kt|übereinkommen|vertr[aä]g)\w*',
                   r'(?:[^\s\(\)\,\.]+ |[^\s\(\)\,\.]+)?(?:abkommen|pakt|übereinkommen|vertr[aä]g)\w*'],
            'fr': [r'(?:accord|contrat|convention|pacte|trait[ée])\w*[\s\-]internationa\w*',
                   r'(?:accord|convention|pacte|traité)(?:s|es)?'
                   '(?: (?:d\'|de la |de |des |sur (?:le|la|les) )[^\s\(\)\,\.]+| [^\s\(\)\,\.]+|(?=\W))'],
            'it': [r'(?:accord|convenzion|patt|trattat)\w*[\s\-](?:internazional|di stato)\w*',
                   r'(?:convenzion[ei]|(?:accord|patt|trattat)[oi])'
                   '(?: (?:d\'|di |(?:de|su)(?:lla|l|i|gli)? |per (?:il|la|gli|i) )[^\s\(\)\,\.]+| [^\s\(\)\,\.]+|(?=\W))']
        }

        super(InternationalTreatyExtractor, self).__init__('international_treaties', patterns_international_treaties)


class InternationalCustomaryLawExtractor(_KeywordExtractorPipeline):
    """
    Implements KeywordExtractorPipeline for keywords indicating the use of international customary law.
    """

    def __init__(self):
        patterns_international_customary_law = {
            'de': [r'(?:(?:internationale\w?|völker(?:rechtliche)?\w?) ?gewohnheitsrecht\w?)',
                   r'(?:gewohnheitsrechtlich\w*(?: völkerrecht\w*)?)'],
            'fr': [r'(?:(?:droit )?(?:des gens|international coutumier|coutumi?er?(?: internationale?)?))'],
            'it': [r'(?:(?:diritto )?(?:consuetudin(?:e|ario)(?: internazionale)?|internazionale consuetudinario))'],
            'lat': [r'(?:ius gentium|opinio [ij]uris)']
        }

        super(InternationalCustomaryLawExtractor, self).__init__('international_customary_law',
                                                                 patterns_international_customary_law)
