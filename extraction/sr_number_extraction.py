import re
import pymongo


class SRNumberExtractor:

    def __init__(self, mongo_uri='mongodb://localhost:27017', db_name='fedsupcourt',
                 int_law_collection_name='international_laws'):
        """Queries all international laws from database."""
        self.client = pymongo.MongoClient(mongo_uri)
        self.int_laws = self.client[db_name][int_law_collection_name]

        self.laws = self._get_international_laws()

        for l in self.laws:
            print('%20s ¦ %2d ¦ %s' % (l['law'], l['hierarchy_level'], str(l['categories'])))

    def extract_sr_numbers(self):

        return None



    def _get_international_laws(self):
        """Returns all international laws with the categories they are assigned to."""
        level_0_categories = self.int_laws.find({'hierarchy_level': 0})
        return self._get_laws_with_categories(level_0_categories)

    def _get_laws_with_categories(self, parent_categories, ancestor_categories=list()):
        """Recursive breadth-first traversal of the law hierarchy, returning a list containing all laws in the
        categories specified in parent_categories with all the categories they are assigned to (i.e. the category-path
        to the law)"""

        laws_with_categories = []

        for law_hierarchy_item in parent_categories:

            # if law_hierarchy_item is a law category that contains subcategories and/or laws
            if 'children' in law_hierarchy_item:
                new_ancestor_categories = ancestor_categories.copy()
                new_ancestor_categories.append({'category': law_hierarchy_item['_id'],
                                                'hierarchy_level': law_hierarchy_item['hierarchy_level']})
                children = self.int_laws.find({'parent': law_hierarchy_item['_id']})
                laws_with_categories.extend(self._get_laws_with_categories(children, new_ancestor_categories))

            # law_hierarchy_item is a leaf
            else:
                # if it is actually a law, return it together with the categories it is assigned to
                if law_hierarchy_item['is_law']:
                    laws_with_categories.append({'law': law_hierarchy_item['_id'],
                                                 'hierarchy_level': law_hierarchy_item['hierarchy_level'],
                                                 'categories': ancestor_categories})

        return laws_with_categories


