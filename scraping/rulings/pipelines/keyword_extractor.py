# -*- coding: utf-8 -*-

import re


class _KeywordExtractorPipeline:

    # ruling chapters from which keywords will be extracted:
    ruling_chapters = ['core_issue', 'statement_of_affairs', 'paragraph']

    # regex for extracting a keyword's context
    sentence_pattern = r'(?:^|(?<=\. )(?=[A-Z])|(?<=\n|\t))'  # beginning of a sentence
    sentence_pattern += r'(?:.(?!\. [A-Z]))*'  # anything NOT followed by beginning of sentence
    sentence_pattern += r'%s'  # keyword
    sentence_pattern += r'.*?(?:\.(?= [A-Z])|$|(?=\n|\t))'  # anything until end of sentence

    # keyword suffix french: used for matching word(s) following the actual keyword.
    pattern_suffix_fr = r'(?: (?:d|(?:à|aux?|avec|dans|des?|pour|sur)(?: ce(?:tte|s)?| la| les?)?(?: double| libre)?'
    pattern_suffix_fr += r'|dont|du|en|es?t'
    pattern_suffix_fr += r'|entre(?:\s\w+){1,4}'
    pattern_suffix_fr += r')[\'\s][^\s\(\)\,\.]*\w'
    pattern_suffix_fr += r'| (?=n\'|ne )'  # next word is a verb -> does not make sense to match it.
    pattern_suffix_fr += r'| (?=qu[ei\'])'  # indicates start of subclause -> does not make sense to match next word
    pattern_suffix_fr += r'| (?=l(?:\'|e |eurs? |a |es ))'
    pattern_suffix_fr += r'| [^\s\(\)\,\.]+\w'  # todo: just leave this case?
    pattern_suffix_fr += r'|(?=\W))'

    # keyword suffix italian
    pattern_suffix_it = r'(?: (?:all[ao]?|d|di'
    pattern_suffix_it += r'|(?:de|da|ne|su)(?:lla|lle|ll|l|i|gli)?'
    pattern_suffix_it += r'|per (?:il|la|gli|i)'
    pattern_suffix_it += r'|[ft]ra(?:\s\w+){1,4}'
    pattern_suffix_it += r')(?: doppia)?[\'\s][^\s\(\)\,\.]*\w'
    pattern_suffix_it += r'| [^\s\(\)\,\.]*\w|(?=\W))'

    pattern_publication_omission = r'(?! \d+| [ivx]+\b| vol\b)'


    def __init__(self, keyword_type, keyword_patterns):
        """
        :param keyword_patterns: dict of format {'<LANGUAGE>': [r'<PATTERN_1>', r'<PATTERN_2>']}
        :type keyword_patterns: dict
        """
        self.keyword_patterns = keyword_patterns
        self.keyword_type = keyword_type

    def process_item(self, ruling, spider):

        # find keywords associated to international treaties
        extracted_keywords = {
            'clear': [],
            'broad': []
        }

        # go through all ruling chapters and extract keywords
        for chapter in self.ruling_chapters:
            if chapter in ruling:
                for pattern_language, patterns in self.keyword_patterns.items():
                    if 'clear' in patterns:
                        extracted_keywords['clear'].extend(re.findall(patterns['clear'], ruling[chapter], re.IGNORECASE))

                    if 'broad' in patterns:
                        # only save a 'broad' keyword if it is not detected by the 'clear' pattern
                        extracted_broad = re.findall(patterns['broad'], ruling[chapter], re.IGNORECASE)

                        for broad_keyword in extracted_broad:
                            if 'clear' in patterns:
                                if not re.search(patterns['clear'], broad_keyword, re.IGNORECASE):
                                    extracted_keywords['broad'].append(broad_keyword)
                            else:
                                extracted_keywords['broad'].append(broad_keyword)

        keywords_and_contexts = {}

        # context extraction for 'clear' and 'broad' keywords
        for pattern_type in ['clear', 'broad']:
            keyword_counts = {}
            contexts = []

            # if keywords have been found, extract the entire sentences in which they occur
            if len(extracted_keywords[pattern_type]) > 0:

                # iterate through all unique keywords
                for keyword in set(extracted_keywords[pattern_type]):

                    # create the pattern matching sentences containing the keyword
                    keyword_context_pattern = self.sentence_pattern % re.escape(keyword)

                    # find and save contexts in each chapter
                    for chapter in self.ruling_chapters:
                        if chapter in ruling:
                            sentences = re.findall(keyword_context_pattern, ruling[chapter])  # don't IGNORECASE here!

                            # update contexts list with each extracted sentence
                            contexts.extend(
                                [{'keyword': keyword, 'chapter': chapter, 'sentence': sentence} for sentence in sentences]
                            )

                            # update keyword count (difficult to do this more elegantly above)
                            keyword_counts[keyword] = keyword_counts.get(keyword, 0) + len(sentences)

                # keywords and counts are saved in a format that is easier to access in mongodb
                keywords_and_contexts[pattern_type] = {
                    'keywords': [{'keyword': kw, 'count': cnt} for kw, cnt in keyword_counts.items()],
                    'contexts': contexts
                }

        if len(keywords_and_contexts) > 0:
            ruling[self.keyword_type] = keywords_and_contexts

        return ruling


class InternationalTreatyExtractor(_KeywordExtractorPipeline):
    """
    Implements KeywordExtractorPipeline for keywords indicating the use of international treaties.
    """

    def __init__(self):
        patterns_international_treaties = {
            'de': {
                'clear': r'(?:international|völkerrecht|staat)\w*[\s\-]?(?:abkommen|p[aä]kt|übereinkommen|vertr[aä]g)\w*',
                'broad': r'(?:\w[^\s\(\)\,\.]+\s?)?(?:abkommen|pakt|übereinkommen)\w*'
            },
            'fr': {
                'clear': r'(?:accord|contrat|convention|pacte|trait[ée])\w*[\s\-]internationa\w*',
                'broad': r'(?:accord|convention|pacte|traité)(?:s|es)?' + self.pattern_suffix_fr
            },
            'it': {
                'clear': r'(?:accord[oi]|convenzion|patt|trattat)\w*[\s\-](?:internazional|di stato)\w*',
                'broad': r'(?:convenzion[ei]|(?:accord|patt|trattat)[oi])' + self.pattern_suffix_it
            }
        }

        super(InternationalTreatyExtractor, self).__init__('international_treaties', patterns_international_treaties)


class InternationalCustomaryLawExtractor(_KeywordExtractorPipeline):
    """
    Implements KeywordExtractorPipeline for keywords indicating the use of international customary law.
    """

    def __init__(self):
        patterns_international_customary_law = {
            'de': {
                'clear': r'(?:(?:internationale\w?|völker(?:rechtliche)?\w?) ?gewohnheitsrecht\w*|'
                         r'(?:gewohnheitsrechtlich\w*(?: völkerrecht\w*)))'
                         + self.pattern_publication_omission,
                'broad': r'(?:gewohnheitsrechtlich\w*(?:\s\w+)?)'
            },
            'fr': {
                'clear': r'(?:(?:droit )?(?:international coutumier|coutumi?er?(?: internationale?)))'
                         + self.pattern_publication_omission,
                'broad': r'(?:(?:droit )?(?:coutumi?er?(?: \w+)?))'
                         + self.pattern_publication_omission
                         + self.pattern_suffix_fr
            },
            'it': {
                'clear': r'(?:(?:diritto )?(?:consuetudin(?:e|ario)(?: internazionale)|internazionale consuetudinario))'
                         + self.pattern_publication_omission,
                'broad': r'(?:(?:diritto )?(?:consuetudin(?:e|ario)))'
                         + self.pattern_publication_omission
                         + self.pattern_suffix_it
            },
            'lat': {
                'clear': r'(?:opinio [ij]uris)'
            }
        }

        super(InternationalCustomaryLawExtractor, self).__init__('international_customary_law',
                                                                 patterns_international_customary_law)


class GeneralInternationalLawExtractor(_KeywordExtractorPipeline):
    """
    Implements KeywordExtractorPipeline for keywords indicating the use of international law in general.
    """

    def __init__(self):
        patterns_international_law_in_general = {
            'de': {
                'clear': r'(?:(?:international|völker)\w*[\s\-]?\w*recht\w*)' + self.pattern_publication_omission
            },
            'fr': {
                'clear': r'(?:droits? (?:privé |public )?internationa(?:l|ux)'
                         + self.pattern_publication_omission
                         + r'(?: privé| public)?)'
                         + self.pattern_suffix_fr,
                'broad': r'droit des gens'
            },
            'it': {
                'clear': r'(?:diritt[oi] (?:(?:pubblico|privato) )?internazional[ei]'
                         + self.pattern_publication_omission + r')'
                         + self.pattern_suffix_it
            },
            'lat': {
                'broad': r'(?:ius gentium)'
            }
        }

        super(GeneralInternationalLawExtractor, self).__init__('international_law_in_general',
                                                               patterns_international_law_in_general)
