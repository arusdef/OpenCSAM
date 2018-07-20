""" [secureworks] Web Scraper """

import os
from .abstract_crawler import AbstractWebCrawler


class SecureworksCrawler(AbstractWebCrawler):
    """ [secureworks] Web Scraper """

    # Spider Properties
    name = "web_secureworks"

    # Crawler Properties
    resource_link = 'https://www.secureworks.com/research?page=300'
    resource_label = 'secureworks'

    # TODO Move it to the super class
    custom_settings = {
        'ITEM_PIPELINES': {
            'scrapy_crawlers.pipelines.ElasticIndexPipeline': 500
        }
    }

    @classmethod
    def links_to_pages(self, response):
        return []

    links_to_articles_query = '#divPostListContainer > article > div.description > h3 > a::attr(href)'
    extract_title_query = '#content div.text-wrap div.text-holder h1::text'
    extract_datetime_query = '#content div.text-wrap div.text-holder time::attr(datetime)'
    extract_content_query = '#content div.text-wrap div.text-holder div.dashed p'
