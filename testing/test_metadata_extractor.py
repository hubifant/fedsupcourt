# pycharm testing tuto: https://confluence.jetbrains.com/display/PYH/Creating+and+running+a+Python+unit+test

import unittest
from scraping.rulings.pipelines import MetadataExtractorPipeline
from testing.dummy_data import case_metadata_extraction


class TestMetadataExtractor(unittest.TestCase):
    metadata_extractor = MetadataExtractorPipeline()

    def test_date_extraction(self):
        """
        Asserts that simple keyword is detected.
        """
        for i, title_of_judgement in enumerate(case_metadata_extraction['title_of_judgement']):
            extracted_date = self.metadata_extractor._extract_date(title_of_judgement)
            print(extracted_date + ": \n" + title_of_judgement)
            self.assertEqual(extracted_date, case_metadata_extraction['date'][i])


if __name__ == '__main__':
    unittest.main()
