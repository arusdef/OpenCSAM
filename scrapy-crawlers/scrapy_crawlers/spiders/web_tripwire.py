""" [Tripwire] Web Scraper """

import os
from .abstract_crawler import AbstractWebCrawler


class TripwireCrawler(AbstractWebCrawler):
    """ [Tripwire] Web Scraper """

    # Spider Properties
    name = "web_tripwire"

    # Crawler Properties
    resource_link = 'https://www.tripwire.com/state-of-security/news/'
    resource_label = 'tripwire'

    # TODO Move it to the super class
    custom_settings = {
        'ITEM_PIPELINES': {
            'scrapy_crawlers.pipelines.ElasticIndexPipeline': 500
        }
    }

    links_to_articles_query = 'section#page section#content section.container ' \
        'div.body-content article header.entry-header h5.title.entry-title a::attr(href)'
    links_to_pages_query = 'section#page section#content section.container ' \
        'div.body-content nav.pagination ul.pagination li a.page-numbers::attr(href)'
    extract_title_query = 'section#page section#content section.container article ' \
        'header.page-header.single-header h1.title.single::text'
    extract_datetime_query = 'meta[property="article:published_time"]::attr(content)'
    extract_content_query = 'section#page section#content section.container article ' \
        'section.body-content span.entry-content.post-content p'
