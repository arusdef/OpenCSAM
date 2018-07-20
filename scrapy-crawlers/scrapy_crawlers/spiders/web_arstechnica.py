""" [ArsTechnica] Web Scraper """

import os
from .abstract_crawler import AbstractWebCrawler


class ArsTechnicaCrawler(AbstractWebCrawler):
    """ [ArsTechnica] Web Scraper """

    # Spider Properties
    name = "web_arstechnica"

    # Crawler Properties
    resource_link = 'https://arstechnica.com/tag/security/'
    resource_label = 'arstechnica'

    # TODO Move it to the super class
    custom_settings = {
        'ITEM_PIPELINES': {
            'scrapy_crawlers.pipelines.ElasticIndexPipeline': 500
        }
    }

    links_to_articles_query = 'article.article header h2 a::attr(href)'
    links_to_pages_query = 'div.prev-next-links a::attr(href)'
    extract_title_query = 'article header.article-header h1::text'
    extract_datetime_query = 'article header.article-header p.byline time.date::attr(datetime)'
    extract_content_query = 'article div.article-content p'
