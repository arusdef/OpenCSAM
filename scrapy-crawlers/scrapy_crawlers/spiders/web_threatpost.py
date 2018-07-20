""" [ThreatPost] Web Scraper """

import os
from dateutil import parser
from bs4 import BeautifulSoup
from .abstract_crawler import AbstractWebCrawler


class ThreatPostCrawler(AbstractWebCrawler):
    """ [ThreatPost] Web Scraper """

    # Spider Properties
    name = "web_threatpost"

    # Crawler Properties
    resource_link = 'https://threatpost.com/blog/'
    resource_label = 'threatpost'

    # TODO Move it to the super class
    custom_settings = {
        'ITEM_PIPELINES': {
            'scrapy_crawlers.pipelines.ElasticIndexPipeline': 500
        }
    }

    links_to_articles_query = '#content #latest-posts article h3.entry-title a::attr(href)'
    links_to_pages_query = '#content div.navigation p a::attr(href)'
    extract_title_query = '#main #content article.post header.entry-header h1.entry-title::text'
    extract_datetime_query = '#main #content article.post header.entry-header div.post-info span.date time::text'
    extract_content_query = '#main #content article.post div.entry-content p'
