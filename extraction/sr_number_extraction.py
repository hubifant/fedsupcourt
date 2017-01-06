import re
import pymongo
import logging


class SRNumberExtractor:

    def __init__(self, mongo_uri='mongodb://localhost:27017', db_name='fedsupcourt',
                 int_law_collection_name='international_laws'):
        """Queries all international laws from database."""
        self.client = pymongo.MongoClient(mongo_uri)
        self.int_laws = self.client[db_name][int_law_collection_name]

        self.laws = self._get_international_laws()
        print('Queried %d laws from the database.' % len(self.laws))

        self.sr_pattern = r'(?:(?:(?<=sr |rs )|'        # SR-number is preceded by 'sr ', 'rs '
        self.sr_pattern += r'(?<=\(|\[| ))'             # or by '(', '[', ' '
        self.sr_pattern += r'0(?:\.\d{3})*\.\d{1,3}'    # SR number format: e.g. '0.xxx.xxx.xx'

        # Exception: it is allowed to cite ECHR (European Convention for
        # the Protection of Human Rights and Fundamental Freedoms) by
        # its name instead of its number (which is SR 0.101)
        self.echr_pattern = r'\b(?:EMRK|europäische\w menschenrechtskonvention'
        self.echr_pattern += r'|konvention zum schutz der menschenrechte und grundfreiheiten'
        self.echr_pattern += r'|CEDH|convention européenne des droits de l\'homme'
        self.echr_pattern += r'|convention de sauvegarde des droits de l’homme et des libertés fondamentales'
        self.echr_pattern += r'|CEDU|convenzione europea dei diritti dell\'uomo'
        self.echr_pattern += r'|convenzione per la salvaguardia dei diritti dell\'uomo e delle libertà fondamentali)\b'

        # include special ECHR cases in the SR pattern
        self.sr_pattern += r'|' + self.echr_pattern + r')'

    def extract_sr_numbers(self, text):
        extracted_laws = []
        extracted_categories = []

        for potential_sr_nb in re.findall(self.sr_pattern, text, re.IGNORECASE):

            # if the ECHR-law was extracted, translate it into its sr-number.
            # if potential_sr_nb.upper() in ['EMRK', 'CEDH', 'CEDU']:
            if re.match(self.echr_pattern, potential_sr_nb):
                potential_sr_nb = '0.101'

            # if the matched pattern is a key in self.int_laws, it IS an existing SR number
            if potential_sr_nb in self.laws:
                law_info = self.laws[potential_sr_nb]
                extracted_laws.append({'law': potential_sr_nb, 'hierarchy_level': law_info['hierarchy_level']})
                for category in law_info['categories']:
                    if category not in extracted_categories:
                        extracted_categories.append(category)

        return extracted_laws, extracted_categories

    def _get_international_laws(self):
        """Returns all international laws with the categories they are assigned to."""
        level_0_categories = self.int_laws.find({'hierarchy_level': 0})
        return self._get_laws_with_categories(level_0_categories)

    def _get_laws_with_categories(self, parent_categories, ancestor_categories=list()):
        """Recursive breadth-first traversal of the law hierarchy, returning a list containing all laws in the
        categories specified in parent_categories with all the categories they are assigned to (i.e. the category-path
        to the law)"""

        laws_with_categories = {}

        for law_hierarchy_item in parent_categories:

            # if law_hierarchy_item is a law category that contains subcategories and/or laws
            if 'children' in law_hierarchy_item:
                new_ancestor_categories = ancestor_categories.copy()
                new_ancestor_categories.append({'category': law_hierarchy_item['_id'],
                                                'hierarchy_level': law_hierarchy_item['hierarchy_level']})
                children = self.int_laws.find({'parent': law_hierarchy_item['_id']})
                laws_with_categories.update(self._get_laws_with_categories(children, new_ancestor_categories))

            # law_hierarchy_item is a leaf
            else:
                # if it is actually a law, return it together with the categories it is assigned to
                if law_hierarchy_item['is_law']:
                    laws_with_categories[law_hierarchy_item['_id']] = {
                            'hierarchy_level': law_hierarchy_item['hierarchy_level'],
                            'categories': ancestor_categories
                    }

        return laws_with_categories
