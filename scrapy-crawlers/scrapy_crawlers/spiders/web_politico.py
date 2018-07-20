""" [POLITICO] Web Scraper """

import os
from dateutil import parser
from bs4 import BeautifulSoup
from .abstract_crawler import AbstractWebCrawler


class PoliticoCrawler(AbstractWebCrawler):
    """ [POLITICO] Web Scraper """

    # Spider Properties
    name = "web_politico"

    # Crawler Properties
    resource_link = 'https://www.politico.com/cybersecurity'
    resource_label = 'politico'

    # TODO Move it to the super class
    custom_settings = {
        'ITEM_PIPELINES': {
            'scrapy_crawlers.pipelines.ElasticIndexPipeline': 500
        }
    }

    links_to_articles_query =   '#globalWrapper main section.content-groupset ' \
                                'div.content-group ul li article header h3 a::attr(href)'
    links_to_pages_query =      '#globalWrapper main div.content-nav div.pagination ' \
                                'ol li a::attr(href)'
    extract_title_query =       '#globalWrapper article div.summary header h1 span::text'
    extract_datetime_query =    '#globalWrapper article div.summary footer.meta p.timestamp time::attr(datetime)'
    extract_content_query =     '#globalWrapper article div.content div.story-text p'
