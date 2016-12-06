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

        for tr in response.xpath('//div[@id="content"]/table/tbody/tr[td[not(@style="padding-left: 23px") and not(a)]]'):

            category_loader = ItemLoader(item=CategoryItem())
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

        _generate_children(response.meta['parent_id'], parent_absolute_level, list(law_table))
        print('=================================================================')
        print('')


# recursive function returning list of children IDs
def _generate_children(parent_id, parent_absolute_level, categories):

    # the siblings are located one level higher than their parent
    sibling_abs_lvl = parent_absolute_level + 1

    # compute the relative sibling hierarchy levels (the longer the ID, the higher the level.)
    relative_levels = [c_lvl for c_id, c_lvl, c_tr in categories if c_lvl is not None]
    if relative_levels:
        sibling_rel_lvl = min(relative_levels)
    else:
        sibling_rel_lvl = 99

    sibling_ids = []
    attached_laws = []

    # find all elements on the current sibling level
    sibling_found = False
    for next_sibling, (next_id, next_lvl, next_tr) in enumerate(categories):

        if next_lvl is None and not sibling_found:
            law_id = _generate_law_item(next_tr, parent_id, sibling_abs_lvl)
            attached_laws.append(law_id)

        elif next_lvl == sibling_rel_lvl:
            if not sibling_found:
                # first sibling detected...
                curr_sibling = next_sibling
                sibling_found = True

            else:
                # another sibling detected...
                curr_id, curr_lvl, curr_tr = categories[curr_sibling]
                sibling_ids.append(curr_id)

                # generate the current sibling's children
                children = _generate_children(curr_id,
                                              sibling_abs_lvl,
                                              categories[curr_sibling + 1:next_sibling])

                # generate a category item for the current sibling
                _generate_law_category_item(curr_id, sibling_abs_lvl, curr_tr, parent_id, children)
                curr_sibling = next_sibling

    # the last sibling in the list...
    if sibling_found:
        curr_id, curr_lvl, curr_tr = categories[curr_sibling]
        sibling_ids.append(curr_id)

        # generate the last sibling's children
        children = _generate_children(curr_id, sibling_abs_lvl, categories[curr_sibling + 1:])

        # generate a category item for the last sibling
        _generate_law_category_item(curr_id, sibling_abs_lvl, curr_tr, parent_id, children)

    sibling_ids.extend(attached_laws)

    return sibling_ids


def _generate_law_category_item(category_id, level, tr_tag, parent_id, children):
    print(('. ' * level) + category_id + ' --> ' + str(children) + ' (lvl %d)' % level)
    # todo don't forget url
    # yield


def _generate_law_item(tr_tag, parent_id, level):
    law_id = tr_tag.xpath('td/a[not(@href)]/@name').extract_first()
    name = tr_tag.xpath('td/a[@href]/text()').extract_first()
    url = tr_tag.xpath('td/a/@href').extract_first()
    print(('. ' * level) + '%-8s --> %-17s ¦ %-60s ¦ %s' % (parent_id, law_id, url, name))
    return law_id