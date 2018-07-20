""" [welivesecurity] Web Scraper """

import os
from .abstract_crawler import AbstractWebCrawler


class WeLiveSecurityCrawler(AbstractWebCrawler):
    """ [welivesecurity] Web Scraper """

    # Spider Properties
    name = "web_welivesecurity"

    # Crawler Properties
    resource_link = 'https://www.welivesecurity.com/'
    resource_label = 'welivesecurity'

    # TODO Move it to the super class
    custom_settings = {
        'ITEM_PIPELINES': {
            'scrapy_crawlers.pipelines.ElasticIndexPipeline': 500
        }
    }

    links_to_articles_query = '#news-feed > article > div.text-wrapper > h2 > a::attr(href)'
    links_to_pages_query = '#news-feed > div.pagination-wrapper > div.wp-pagenavi > a::attr(href)'
    extract_title_query = '#article-detail div.container h1::text'
    extract_datetime_query = '#article-detail div.container div.post-meta time::attr(datetime)'
    extract_content_query = '#article-detail > div.content > div.container p'
