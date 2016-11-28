# pycharm testing tuto: https://confluence.jetbrains.com/display/PYH/Creating+and+running+a+Python+unit+test

import unittest
from scraping.rulings.pipelines import InternationalTreatyExtractor, InternationalCustomaryLawExtractor
from testing.dummy_data import case_incomplete, case_completeness_int_treaties, case_completeness_customary_int_law


class TestGeneralKeywordExtractor(unittest.TestCase):
    def test_incomplete_item(self):
        """
        Asserts that no exception is raised if the inputted item does not contain all chapters.
        """

        keyword_extractor = InternationalTreatyExtractor()

        try:
            keyword_extractor.process_item(case_incomplete['input_item'], None)

        except Exception:
            self.fail("Exception raised in test_incomplete_item")

    def test_simple_extraction(self):
        """
        Asserts that simple keyword is detected.
        """

        keyword_extractor = InternationalTreatyExtractor()
        computed_output = keyword_extractor.process_item(case_incomplete['input_item'], None)

        field_to_test = 'international_treaties'

        self.assertEqual(computed_output['keywords'][field_to_test]['keywords'],
                         case_incomplete['expected_output']['keywords'][field_to_test]['keywords'],
                         "Assertion failed in test_simple_extraction")
        self.assertEqual(computed_output['keywords'][field_to_test]['contexts'],
                         case_incomplete['expected_output']['keywords'][field_to_test]['contexts'],
                         "Assertion failed in test_simple_extraction")


class TestSpecificKeywordExtractorExtractors(unittest.TestCase):

    def test_completeness_international_treaties(self):
        """
        Asserts that all expected keywords related to international treaties are extracted
        """

        keyword_extractor = InternationalTreatyExtractor()
        computed_output = keyword_extractor.process_item(case_completeness_int_treaties['input_item'], None)
        computed_keywords = computed_output['keywords']['international_treaties']['keywords'].keys()

        for keyword in case_completeness_int_treaties['expected_output']:
            self.assertIn(keyword, computed_keywords, 'Keyword was not extracted.')

    def test_completeness_int_customary_law(self):
        """
        Asserts that all expected keywords related to customary international law are extracted
        """

        keyword_extractor = InternationalCustomaryLawExtractor()
        computed_output = keyword_extractor.process_item(case_completeness_customary_int_law['input_item'], None)
        computed_keywords = computed_output['keywords']['international_customary_law']['keywords'].keys()

        for keyword in case_completeness_customary_int_law['expected_output']:
            self.assertIn(keyword, computed_keywords, 'Keyword was not extracted.')


if __name__ == '__main__':
    unittest.main()
