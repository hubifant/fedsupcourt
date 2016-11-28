from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from scraping.rulings import RulingSpider
from scrapy.utils.project import get_project_settings


def scrape_rulings():

    # set the format of the logging messages and add pipeline(s)
    settings = get_project_settings()
    settings.set('LOG_FORMAT', '%(levelname)s | %(message)s')
    settings.set('ITEM_PIPELINES', {
        'rulings.pipelines.TextCleanerPipeline': '100,',
        'rulings.pipelines.MetadataExtractorPipeline': '200',
        'rulings.pipelines.InternationalTreatyExtractor': '300',
        'rulings.pipelines.InternationalCustomaryLawExtractor': '301',
        'rulings.pipelines.JsonWriterPipeline': '999'
    })
    settings.set('COOKIES_ENABLED', False)
    settings.set('DOWNLOAD_DELAY', 0.1)
    configure_logging()

    # start the crawler
    runner = CrawlerRunner(settings)
    d = runner.crawl(RulingSpider)

    # add callback that stops the reactor after RulingSpider has finished running
    d.addBoth(lambda _: reactor.stop())

    # the script will be blocked at the following line until the crawling is finished
    reactor.run()


scrape_rulings()
