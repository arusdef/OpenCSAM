""" [trendmicro] Web Scraper """

import os
from .abstract_crawler import AbstractWebCrawler


class TrendMicroCrawler(AbstractWebCrawler):
    """ [trendmicro] Web Scraper """

    # Spider Properties
    name = "web_trendmicro"

    # Crawler Properties
    resource_link = 'https://blog.trendmicro.com/trendlabs-security-intelligence/'
    resource_label = 'trendmicro'

    # TODO Move it to the super class
    custom_settings = {
        'ITEM_PIPELINES': {
            'scrapy_crawlers.pipelines.ElasticIndexPipeline': 500
        }
    }

    links_to_articles_query = '#pageContent div.post-text > a::attr(href)'
    links_to_pages_query = '#post-pagination > a::attr(href)'
    extract_title_query = '#pageContent div.post-head > div.post-title > h1::text'
    extract_datetime_query = 'meta[property="article:published_time"]::attr(content)'
    extract_content_query = '#pageContent div.post-text > p'
