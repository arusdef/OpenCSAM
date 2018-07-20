""" [Naked Security] Web Scraper """

import os
from .abstract_crawler import AbstractWebCrawler


class NakedSecurityCrawler(AbstractWebCrawler):
    """ [Naked Security] Web Scraper """

    # Spider Properties
    name = "web_nakedsecurity"

    # Crawler Properties
    resource_link = 'https://nakedsecurity.sophos.com/'
    resource_label = 'nakedsecurity'

    # TODO Move it to the super class
    custom_settings = {
        'ITEM_PIPELINES': {
            'scrapy_crawlers.pipelines.ElasticIndexPipeline': 500
        }
    }

    links_to_articles_query = 'div#page section.cards-panel div.container h3.card-title a::attr(href)'
    links_to_pages_query = 'div#page div.load-more div.container a::attr(href)'
    extract_title_query = 'div#page section.content-panel div.container main#main article header.entry-header h1::text'
    extract_datetime_query = 'div#page section.content-panel div.container main#main article header.entry-header time.published::attr(datetime)'
    extract_content_query = 'div#page section.content-panel div.container main#main article div.entry-content p'
