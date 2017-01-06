# -*- coding: utf-8 -*-

from extraction import CombinedKeywordExtractor


class KeywordExtractorPipeline:

    def __init__(self):
        """
        Pipeline for extracting all types of keywords from ruling items
        """

        self.keyword_extractor = CombinedKeywordExtractor()

    def process_item(self, ruling, spider):
        ruling = self.keyword_extractor.extract(ruling)

        return ruling



