""" [Reuters] Web Scraper """

import os
from dateutil import parser
from bs4 import BeautifulSoup
from .abstract_crawler import AbstractWebCrawler


class ReutersCrawler(AbstractWebCrawler):
    """ [Reuters] Web Scraper """

    # Spider Properties
    name = "web_reuters"

    # Crawler Properties
    resource_link = 'https://www.reuters.com/news/archive/cybersecurity'
    resource_label = 'reuters'

    # TODO Move it to the super class
    custom_settings = {
        'ITEM_PIPELINES': {
            'scrapy_crawlers.pipelines.ElasticIndexPipeline': 500
        }
    }

    links_to_articles_query = 'article.story div.story-content a::attr(href)'
    links_to_pages_query = 'div.control-nav a.control-nav-next::attr(href)'
    extract_title_query = 'meta[name="analyticsAttributes.title"]::attr(content)'
    extract_datetime_query = 'meta[name="analyticsAttributes.articleDate"]::attr(content)'
    extract_content_query = 'p'
