import scrapy
from scrapy.loader import ItemLoader
from ..items import IndexItem, VolumeItem, RulingsItem


class RulingSpider(scrapy.Spider):
    name = 'rulings'
    start_urls = ["http://relevancy.bger.ch/cgi-bin/IndexCGI?lang=de"]
    allowed_domains =["relevancy.bger.ch"]

    def parse(self, response):
        l = ItemLoader(item=IndexItem(), response=response)
        # l.add_xpath('year', '//tr/td[@valign="top"]/text()')
        l.add_xpath('link', "//tr/td/a[text()[contains(., 'I')]]/@href")
        yield l.load_item()



