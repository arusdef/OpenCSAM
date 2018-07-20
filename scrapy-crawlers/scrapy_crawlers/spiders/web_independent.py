""" [independent] Web Scraper """

import os
from dateutil import parser
from bs4 import BeautifulSoup
from .abstract_crawler import AbstractWebCrawler


class IndependentCrawler(AbstractWebCrawler):
    """ [independent] Web Scraper """

    # Spider Properties
    name = "web_independent"

    # Crawler Properties
    resource_link = 'https://www.independent.co.uk/topic/cyber-security'
    resource_label = 'independent'

    # TODO Move it to the super class
    custom_settings = {
        'ITEM_PIPELINES': {
            'scrapy_crawlers.pipelines.ElasticIndexPipeline': 500
        },
        'USER_AGENT': 'HTTPie/0.9.9'
    }

    links_to_articles_query = '#content > div.region.region-content > div > div > article > div > div.content > h1 > a::attr(href)'
    links_to_pages_query = None
    extract_title_query = 'h1.headline > span::text'
    extract_datetime_query = 'li.publish-date > amp-timeago::text'
    extract_content_query = 'div.body-content'
