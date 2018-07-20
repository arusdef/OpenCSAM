""" [itsecurityguru] Web Scraper """

import os
from .abstract_crawler import AbstractWebCrawler


class ITSecurityGuruCrawler(AbstractWebCrawler):
    """ [itsecurityguru] Web Scraper """

    # Spider Properties
    name = "web_itsecurityguru"

    # Crawler Properties
    resource_link = 'http://www.itsecurityguru.org/category/news/'
    resource_label = 'itsecurityguru'

    # TODO Move it to the super class
    custom_settings = {
        'ITEM_PIPELINES': {
            'scrapy_crawlers.pipelines.ElasticIndexPipeline': 500
        }
    }

    links_to_articles_query = '#main-content div.content div.post-listing article h2 a::attr(href)'
    links_to_pages_query = '#main-content div.content div.pagination a::attr(href)'
    extract_title_query = '#main-content > div.content > article > div.post-inner > h1 > span::text'
    extract_datetime_query = 'meta[property=article\:published_time]::attr(content)'
    extract_content_query = '#main-content > div.content > article > div.post-inner > div.entry p'
