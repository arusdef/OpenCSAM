""" [Securelist] Web Scraper """

import os
from dateutil import parser
from bs4 import BeautifulSoup
from .abstract_crawler import AbstractWebCrawler


class SecurelistCrawler(AbstractWebCrawler):
    """ [Securelist] Web Scraper """

    # Spider Properties
    name = "web_securelist"

    # Crawler Properties
    resource_link = 'https://securelist.com/all/'
    resource_label = 'securelist'

    # TODO Move it to the super class
    custom_settings = {
        'ITEM_PIPELINES': {
            'scrapy_crawlers.pipelines.ElasticIndexPipeline': 500
        }
    }

    links_to_articles_query = '#content article div.entry-content a.read-more::attr(href)'
    links_to_pages_query = '#content > nav > div > div.nav-link.nav-previous > a::attr(href)'
    extract_title_query = '#primary > header > div.title-wrap > h1::text'
    extract_datetime_query = '#primary > header > div.entry-meta time::attr(datetime)'
    extract_content_query = '#primary > div.entry-content > p'
