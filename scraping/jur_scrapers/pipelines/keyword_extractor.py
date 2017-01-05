# -*- coding: utf-8 -*-

from extraction import InternationalTreatyExtractor, InternationalCustomaryLawExtractor, \
    GeneralInternationalLawExtractor


class KeywordExtractorPipeline:

    def __init__(self):
        """
        Pipeline for extracting all types of keywords from ruling items
        """

        self.int_treaty_extractor = InternationalTreatyExtractor()
        self.int_cust_law_extractor = InternationalCustomaryLawExtractor()
        self.gen_int_law_extractor = GeneralInternationalLawExtractor()

    def process_item(self, ruling, spider):
        ruling = self.int_treaty_extractor.extract(ruling)
        ruling = self.int_cust_law_extractor.extract(ruling)
        ruling = self.gen_int_law_extractor.extract(ruling)

        return ruling



