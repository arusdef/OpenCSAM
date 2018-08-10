""" [BBC] Web Scraper """

import os
from .abstract_crawler import AbstractWebCrawler


class BBCCrawler(AbstractWebCrawler):
    """ [BBC] Web Scraper """

    # Spider Properties
    name = "web_bbc"

    # Crawler Properties
    resource_link = 'http://www.bbc.com/news/topics/cz4pr2gd85qt/cyber-security'
    resource_label = 'bbc'

    # TODO Move it to the super class
    custom_settings = {
        'ITEM_PIPELINES': {
            'scrapy_crawlers.pipelines.ElasticIndexPipeline': 500
        }
    }

    links_to_articles_query = 'article > header > div > h3 > a::attr(href)'
    links_to_pages_query = 'dummy' # dynamic ajax pagination
    extract_title_query = '#page > div:nth-child(1) > div.container > div > div.column--primary > div.story-body > h1::text'
    extract_datetime_query = '#page > div:nth-child(1) > div.container > div > div.column--primary > div.story-body > div.with-extracted-share-icons > div > div.story-body__mini-info-list-and-share-row > div.mini-info-list-wrap > ul > li > div::text'
    extract_content_query = '#page > div:nth-child(1) > div.container > div > div.column--primary > div.story-body > div.story-body__inner'
