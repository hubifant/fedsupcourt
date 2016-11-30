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
            extracted_date = self.metadata_extractor._extract_date(title_of_judgement, 'no url')

            self.assertEqual(extracted_date, case_metadata_extraction['date'][i],
                             'Could not extract date from\n"%s"' % title_of_judgement)

    def test_party_extraction(self):
        for i, title_of_judgement in enumerate(case_metadata_extraction['title_of_judgement']):
            extracted_parties = self.metadata_extractor._extract_involved_parties(title_of_judgement, 'no url')

            if case_metadata_extraction['parties'][i] is not None:
                try:
                    if 'claimant' in case_metadata_extraction['parties'][i]:
                        self.assertEqual(extracted_parties['claimant'], case_metadata_extraction['parties'][i]['claimant'],
                                         'Could not correctly extract claimant from\n"%s"' % title_of_judgement)

                    if 'defendant' in case_metadata_extraction['parties'][i]:
                        self.assertEqual(extracted_parties['defendant'], case_metadata_extraction['parties'][i]['defendant'],
                                         'Could not correctly extract defendant from\n"%s"' % title_of_judgement)
                except:
                    self.fail('Party extraction failed:\n"%s"' % title_of_judgement)
            else:
                if extracted_parties is not None:
                    self.fail('Extracted party even though this should not be possible from\n"%s"' % title_of_judgement)


if __name__ == '__main__':
    unittest.main()
