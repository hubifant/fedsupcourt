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
            category_loader.add_value('hierarchy_level', 1)
            id = tr.xpath('td[not(a)]/text()').extract_first()
            url = self.base_url + tr.xpath('td/a/@href').extract_first()
            name = tr.xpath('td/a/text()').extract()

            category_loader = ItemLoader(item=CategoryItem())
            category_loader.add_value('hierarchy_level', 0)
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
        # subcat_titles = response.xpath('//div[@id="content"]//h2')

        # do this in item class?
        # extract_title = lambda s: re.search(r'(?<= - ).*?(?=\r|\n|$)', s).group()
        category_id = lambda tr: tr.xpath('td/h2/@id').extract_first(default='')
        category_level = lambda tr: len(category_id(tr)) if category_id(tr) is not '' else None

        # the more dots in the ID, the lower is the subcat (e.g. '1.0' > '1.0.1')
        # subcats_id_name_lvl = map(lambda h2: (h2.xpath('@id').extract()[0],
        #                                       extract_title(h2.xpath('text()').extract()[0]),
        #                                       h2.xpath('@id').extract()[0].count('.')), subcat_titles)

        law_table = map(lambda tr: (category_id(tr), category_level(tr), tr),
                        response.xpath('//div[@id="content"]/table/tbody/tr'))

        # for c_id, lvl, tr in law_table:
        #     print((c_id, lvl, tr))
        print('-----------------------------------------------------------------')
        _generate_children(response.meta['parent_id'], list(law_table))
        print('=================================================================')
        print('')


# recursive function returning list of children IDs
def _generate_children(parent_id, categories):
    print(parent_id)
    # compute the sibling level (the current level in the category-hierarchy)
    parent_lvl = len(parent_id)
    levels = [c_lvl for c_id, c_lvl, c_tr in categories if c_lvl is not None]
    print(levels)
    if levels:
        sibling_lvl = min(levels)
    else:
        sibling_lvl = 99

    sibling_ids = []
    attached_law_ids = []

    # find all siblings who are direct successors of parent_id
    sibling_found = False
    for next_sibling, (next_id, next_lvl, next_tr) in enumerate(categories):
        # if sibling_found:
        #     print('curr: %d; next: %d' % (curr_sibling, next_sibling))
        # else:
        #     print('next: %d' % next_sibling)

        if next_lvl is None and not sibling_found:
            pass
            # law_id = _generate_law_item(next_tr, parent_id)
            # attached_law_ids.append(law_id)

        elif next_lvl == sibling_lvl:
            if not sibling_found:
                curr_sibling = next_sibling
                sibling_found = True
                print('First sibling found! [%d]' % curr_sibling)

            else:
                print('Next sibling found! [%d]' % next_sibling)
                curr_id, curr_lvl, curr_tr = categories[curr_sibling]
                sibling_ids.append(curr_id)

                # generate the current category's successors
                children = _generate_children(curr_id, categories[curr_sibling + 1:next_sibling])

                # generate a category item from the collected info
                # _generate_law_category_item(curr_id, sibling_lvl, curr_tr, parent_id, children)
                curr_sibling = next_sibling

        elif next_lvl is not None and next_lvl < sibling_lvl and not sibling_found:
            raise Exception('Incest! Child %s is a predecessor.' % next_id)

    # the last sibling in the list...
    if sibling_found:
        print('Ended loop.')
        curr_id, curr_lvl, curr_tr = categories[curr_sibling]
        sibling_ids.append(curr_id)

        # generate the last sibling's successors
        children = _generate_children(curr_id, categories[curr_sibling + 1:])

        # generate a category item from the collected info
        # _generate_law_category_item(curr_id, sibling_lvl, curr_tr, parent_id, children)

    return sibling_ids


def _generate_law_category_item(category_id, level, tr_tag, parent_id, children):
    # todo don't forget url
    yield None


def _generate_law_item(tr_tag, parent_id):
    law_id = tr_tag.xpath('td/a[not(@href)]/@name').extract_first()
    name = tr_tag.xpath('td/a[@href]/text()').extract_first()
    url = tr_tag.xpath('td/a/@href').extract_first()
    print('\tLaw %-8s --> %-17s ¦ %-60s ¦ %s' % (parent_id, law_id, url, name))
    return 'ID'