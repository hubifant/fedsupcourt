import logging

import scrapy
from scrapy.loader import ItemLoader
from ..items import CategoryItem


class InternationalLawSpider(scrapy.Spider):
    name = 'rulings'
    start_urls = ["https://www.admin.ch/opc/de/classified-compilation/international.html"]
    scraped_links = []
    # allowed_domains =["relevancy.bger.ch"]
    counter = 0
    base_url = 'https://www.admin.ch'

    def parse(self, response):

        law_main_categories = response.xpath('//div[@id="content"]/table/tbody/tr')
        logging.info('%d law main categories will be extracted.\n'
                     '=============================================================================================\n\n'
                     % len(law_main_categories))

        for tr in law_main_categories:
            id = tr.xpath('td/text()').extract()
            url = self.base_url + tr.xpath('td/a/@href').extract()[0]
            name = tr.xpath('td/a/text()').extract()

            main_category_loader = ItemLoader(item=CategoryItem())
            main_category_loader.add_value('hierarchy_level', 0)
            main_category_loader.add_value('id', id)
            main_category_loader.add_value('name', name)
            main_category_loader.add_value('url', url)

            if url not in self.scraped_links and len(self.scraped_links) < 1:
                request = scrapy.Request(url, self.parse_main_category)
                request.meta['main_category'] = main_category_loader
                request.meta['parent_id'] = id
                self.scraped_links.append(url)
                yield request

    def parse_main_category(self, response):
        # first, complete the main_category item by adding the children.
        main_category_loader = response.meta['main_category']
        law_categories = response.xpath('//div[@id="content"]/table/tbody/tr/td[not(@style="padding-left: 23px") and not(a)]/text()').extract()
        main_category_loader.add_value('children', law_categories)
        yield main_category_loader.load_item()

        # then, extract the main_category's subcategories...
        for tr in response.xpath('//div[@id="content"]/table/tbody/tr[td[not(@style="padding-left: 23px") and not(a)]]'):

            id = tr.xpath('td[not(a)]/text()').extract_first()
            url = self.base_url + tr.xpath('td/a/@href').extract_first()
            name = tr.xpath('td/a/text()').extract()

            category_loader = ItemLoader(item=CategoryItem())
            category_loader.add_value('hierarchy_level', 1)
            category_loader.add_value('parent', response.meta['parent_id'])
            category_loader.add_value('id', id)
            category_loader.add_value('name', name)
            category_loader.add_value('url', url)

            if url not in self.scraped_links:
                request = scrapy.Request(url, self.parse_category)
                request.meta['category'] = category_loader
                request.meta['parent_id'] = id

                yield request

    def parse_category(self, response):
        # first, complete the category item by adding its children
        category_loader = response.meta['category']

        # the longer the ID, the lower is the subcat (e.g. '1.0' > '1.0.1')
        category_id = lambda tr: tr.xpath('td/h2/@id').extract_first(default='')
        category_relative_level = lambda tr: len(category_id(tr)) if category_id(tr) is not '' else None

        law_table = map(lambda tr: (category_id(tr), category_relative_level(tr), tr),
                        response.xpath('//div[@id="content"]/table/tbody/tr'))

        parent_absolute_level = 1

        children_ids, successor_items = self._generate_children(response.meta['parent_id'],
                                                                parent_absolute_level,
                                                                list(law_table),
                                                                response.url)
        print('=================================================================')
        print('')
        category_loader.add_value('children', children_ids)
        yield category_loader.load_item()
        yield from successor_items

    # recursive function returning list of children IDs
    def _generate_children(self, parent_id, parent_absolute_level, categories, main_cat_url):

        # the siblings are located one level higher than their parent
        sibling_abs_lvl = parent_absolute_level + 1

        # compute the relative sibling hierarchy levels (the longer the ID, the higher the level.)
        relative_levels = [c_lvl for c_id, c_lvl, c_tr in categories if c_lvl is not None]
        if relative_levels:
            sibling_rel_lvl = min(relative_levels)
        else:
            sibling_rel_lvl = 99

        sibling_ids = []
        item_hierarchy = []

        # find all elements on the current sibling level
        sibling_found = False
        for next_sibling, (next_id, next_lvl, next_tr) in enumerate(categories):

            if next_lvl is None and not sibling_found:
                law_id, law_item = self._generate_law_item(next_tr, parent_id, sibling_abs_lvl)
                sibling_ids.append(law_id)
                item_hierarchy.append(law_item)

            elif next_lvl == sibling_rel_lvl:
                if not sibling_found:
                    # first sibling detected...
                    curr_sibling = next_sibling
                    sibling_found = True

                else:
                    # another sibling detected...
                    curr_id, curr_lvl, curr_tr = categories[curr_sibling]

                    # generate the current sibling's children
                    children_ids, successor_items = self._generate_children(curr_id,
                                                                            sibling_abs_lvl,
                                                                            categories[curr_sibling + 1:next_sibling],
                                                                            main_cat_url)

                    # generate a category item for the current sibling
                    law_category_item = self._generate_law_category_item(curr_id,
                                                                         sibling_abs_lvl,
                                                                         curr_tr,
                                                                         parent_id,
                                                                         children_ids,
                                                                         main_cat_url)

                    # first, insert current item into hierarchy, then its successors
                    item_hierarchy.append(law_category_item)
                    item_hierarchy.extend(successor_items)

                    # add current item's ID to sibling list
                    sibling_ids.append(curr_id)

                    # update pointer
                    curr_sibling = next_sibling

        # the last sibling in the list...
        if sibling_found:
            curr_id, curr_lvl, curr_tr = categories[curr_sibling]

            # generate the last sibling's children
            children_ids, successor_items = self._generate_children(curr_id,
                                                                sibling_abs_lvl,
                                                                categories[curr_sibling + 1:],
                                                                main_cat_url)

            # generate a category item for the last sibling
            law_category_item = self._generate_law_category_item(curr_id,
                                                                 sibling_abs_lvl,
                                                                 curr_tr,
                                                                 parent_id,
                                                                 children_ids,
                                                                 main_cat_url)
            # first, insert current item into hierarchy, then its successors
            item_hierarchy.append(law_category_item)
            item_hierarchy.extend(successor_items)

            # add current item's ID to sibling list
            sibling_ids.append(curr_id)

        return sibling_ids, item_hierarchy

    def _generate_law_category_item(self, category_id, level, tr_tag, parent_id, children, main_cat_url):
        category_name = tr_tag.xpath('td/h2/text()').extract_first()
        url = main_cat_url + '#' + category_id
        print(('. ' * level) + category_id + ' ' + category_name + ' --> ' + str(children) + ' (lvl %d)' % level)

        category_loader = ItemLoader(item=CategoryItem())
        category_loader.add_value('hierarchy_level', level)
        category_loader.add_value('parent', parent_id)
        category_loader.add_value('id', category_id)
        category_loader.add_value('name', category_name)
        category_loader.add_value('children', children)
        category_loader.add_value('url', url)

        return category_loader.load_item()

    def _generate_law_item(self, tr_tag, parent_id, level):
        law_id = tr_tag.xpath('td/a[not(@href)]/@name').extract_first()
        name = tr_tag.xpath('td/a[@href]/text()').extract_first()
        url = self.base_url + tr_tag.xpath('td/a/@href').extract_first()
        print(('. ' * level) + '%-8s --> %-17s ¦ %-80s ¦ %s' % (parent_id, law_id, url, name))
        return law_id, None
