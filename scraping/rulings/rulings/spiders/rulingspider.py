import scrapy
from scrapy.loader import ItemLoader
from ..items import RulingItem


class RulingSpider(scrapy.Spider):
    name = 'rulings'
    start_urls = ["http://relevancy.bger.ch/cgi-bin/IndexCGI?lang=de"]
    scraped_links = []
    allowed_domains =["relevancy.bger.ch"]

    def parse(self, response):

        volume_links = response.xpath("//tr/td/a[text()[contains(., 'I')]]/@href").extract()
        for link in volume_links:
            url = 'http://relevancy.bger.ch/' + link
            if url not in self.scraped_links and len(self.scraped_links) < 2:
                self.scraped_links.append(url)
                print('\n\n\n'+url+'\n\n\n')
                yield scrapy.Request(url, self.parse)

        ruling_links = response.xpath('//li/a/@href').extract()
        for link in ruling_links:
            url = 'http://relevancy.bger.ch/' + link
            if url not in self.scraped_links and len(self.scraped_links) < 4:
                self.scraped_links.append(url)
                print('\n\n\n'+url+'\n\n\n')
                yield scrapy.Request(url, self.parse)

        l = ItemLoader(item=RulingItem(), response=response)
        # l.add_xpath('year', '//tr/td[@valign="top"]/text()')
        l.add_xpath('regeste', '//div[@id="regeste"]//text()')
        yield l.load_item()



