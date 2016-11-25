# pycharm testing tuto: https://confluence.jetbrains.com/display/PYH/Creating+and+running+a+Python+unit+test

import unittest
from scraping.rulings.pipelines import KeywordExtractorPipeline
from testing.dummy_data import case_incomplete


class TestKeywordExtractorPipeline(unittest.TestCase):
    def test_incomplete_item(self):
        """
        Asserts that no exception is raised if the inputted item does not contain all chapters.
        """

        keyword_extractor = KeywordExtractorPipeline()

        try:
            keyword_extractor.process_item(case_incomplete['input_item'], None)

        except Exception:
            self.fail("Exception raised in test_incomplete_item")

    def test_simple_extraction(self):
        """
        Asserts that simple keyword is detected.
        """

        keyword_extractor = KeywordExtractorPipeline()
        computed_output = keyword_extractor.process_item(case_incomplete['input_item'], None)

        field_to_test = 'international_treaties'

        self.assertEqual(computed_output[field_to_test]['keywords'],
                         case_incomplete['expected_output'][field_to_test]['keywords'],
                         "Assertion failed in test_simple_extraction")
        self.assertEqual(computed_output[field_to_test]['contexts'],
                         case_incomplete['expected_output'][field_to_test]['contexts'],
                         "Assertion failed in test_simple_extraction")


if __name__ == '__main__':
    unittest.main()
