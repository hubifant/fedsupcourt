# pycharm testing tuto: https://confluence.jetbrains.com/display/PYH/Creating+and+running+a+Python+unit+test

import unittest
from scraping.rulings.pipelines import InternationalTreatyExtractor, InternationalCustomaryLawExtractor, \
    GeneralInternationalLawExtractor
from testing.dummy_data import case_incomplete, case_completeness_int_treaties, case_completeness_customary_int_law, \
    case_completeness_int_law_in_general


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
        Asserts that simple 'broad' keyword is detected.
        """

        keyword_extractor = InternationalTreatyExtractor()
        computed_output = keyword_extractor.process_item(case_incomplete['input_item'], None)

        field_to_test = 'international_treaties'
        keyword_type = 'broad'

        self.assertEqual(computed_output[field_to_test][keyword_type]['keywords'],
                         case_incomplete['expected_output'][field_to_test][keyword_type]['keywords'],
                         "Assertion failed in test_simple_extraction")
        self.assertEqual(computed_output[field_to_test][keyword_type]['contexts'],
                         case_incomplete['expected_output'][field_to_test][keyword_type]['contexts'],
                         "Assertion failed in test_simple_extraction")


class TestSpecificKeywordExtractorExtractors(unittest.TestCase):
    def _test_completeness(self, keyword_type, keyword_extractor, test_data):
        """
        Asserts that all expected keywords are extracted
        :param keyword_type: specifies the keyword type
        :type keyword_type: string
        :param keyword_extractor: KeywordExtractorPipeline object
        :type keyword_extractor: KeywordExtractorPipeline
        :type test_data: dict
        """
        computed_output = keyword_extractor.process_item(test_data['input_item'], None)

        # for 'clear' and 'broad' keywords...
        for type in ['clear', 'broad']:
            self.assertEqual(type in computed_output[keyword_type], type in test_data['expected_output'],
                             'Something with keywords of type "%s" did not work as expected.' % type)

            if type in computed_output[keyword_type]:
                computed_keywords_and_counts = computed_output[keyword_type][type]['keywords']
                computed_keywords = [kw_c['keyword'] for kw_c in computed_keywords_and_counts]

                # sort both lists (for nicer prints)
                computed_keywords.sort()
                test_data['expected_output'][type].sort()

                self.assertLessEqual(
                    len(computed_keywords),
                    len(test_data['expected_output'][type]),
                    'Too many keywords have been extracted!\n'
                    ' --> Extracted: %s\n'
                    ' --> Should-be: %s' % (str(computed_keywords),
                                            str(test_data['expected_output'][type])))

                for keyword in test_data['expected_output'][type]:
                    self.assertIn(keyword, computed_keywords, 'Keyword was not extracted.')

    def test_completeness_international_treaties(self):
        """
        Asserts that all expected keywords related to international treaties are extracted
        """

        keyword_extractor = InternationalTreatyExtractor()
        self._test_completeness('international_treaties', keyword_extractor, case_completeness_int_treaties)

    def test_completeness_int_customary_law(self):
        """
        Asserts that all expected keywords related to customary international law are extracted
        """

        keyword_extractor = InternationalCustomaryLawExtractor()
        self._test_completeness('international_customary_law', keyword_extractor, case_completeness_customary_int_law)

    def test_completeness_int_law_in_general(self):
        """
        Asserts that all expected keywords related to international law in general are extracted
        """

        keyword_extractor = GeneralInternationalLawExtractor()
        self._test_completeness('international_law_in_general', keyword_extractor, case_completeness_int_law_in_general)


if __name__ == '__main__':
    unittest.main()
