""" [SCMagazine] Web Scraper """

from .abstract_crawler import AbstractWebCrawler


class SCMagazineCrawler(AbstractWebCrawler):
    """ [SCMagazine] Web Scraper """

    # Spider Properties
    name = "web_scmagazine"

    # Crawler Properties
    resource_link = 'https://www.scmagazine.com/archive/23903/44/1/'
    resource_label = 'scmagazine'

    # TODO Move it to the super class
    custom_settings = {
        'ITEM_PIPELINES': {
            'scrapy_crawlers.pipelines.ElasticIndexPipeline': 500
        },
        'ROBOTSTXT_OBEY': False
    }

    links_to_articles_query = '#main-section > div > div > div.col-9 > h2 > a::attr(href)'
    links_to_pages_query = None
    extract_title_query = '#main-section > article > h1::text'
    extract_datetime_query = '#main-section > article > time::text'
    extract_content_query = '#main-section > article > div.article-body'
