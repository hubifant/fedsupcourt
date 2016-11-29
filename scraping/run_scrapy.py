from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from scraping.rulings import RulingSpider
from scrapy.utils.project import get_project_settings


def scrape_rulings():

    # don't show too many messages
    #  --> log levels: CRITICAL > ERROR > WARNING > INFO > DEBUG
    configure_logging({
        'LOG_LEVEL': 'INFO',
        'LOG_FORMAT': '%(levelname)s \t| %(asctime)s \t| %(message)s',
        # 'LOG_FILE': 'crawler.log'
    })

    # set the format of the logging messages and add pipeline(s)
    settings = get_project_settings()

    settings.set('ITEM_PIPELINES', {
        'rulings.pipelines.TextCleanerPipeline': 100,
        'rulings.pipelines.MetadataExtractorPipeline': 200,
        'rulings.pipelines.InternationalTreatyExtractor': 300,
        'rulings.pipelines.InternationalCustomaryLawExtractor': 301,
        'rulings.pipelines.GeneralInternationalLawExtractor': 302,
        'rulings.pipelines.JsonWriterPipeline': 999
    })

    # Turn off the built-in UserAgentMiddleware and add RandomUserAgentMiddleware.
    #  --> https://github.com/alecxe/scrapy-fake-useragent
    settings.set('DOWNLOADER_MIDDLEWARES', {
        'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
        'scrapy_fake_useragent.middleware.RandomUserAgentMiddleware': 400,  # todo: don't forget to install!
    })

    # turn off cookies
    settings.set('COOKIES_ENABLED', False)

    # set a download delay of 0.2sec (2sec is recommended)
    settings.set('DOWNLOAD_DELAY', 0.2)

    runner = CrawlerRunner(settings)

    # start the crawler
    d = runner.crawl(RulingSpider)

    # add callback that stops the reactor after RulingSpider has finished running
    d.addBoth(lambda _: reactor.stop())

    # the script will be blocked at the following line until the crawling is finished
    reactor.run()


scrape_rulings()
