""" [CSOOnline] Web Scraper """

import os
from .abstract_crawler import AbstractWebCrawler


class CSOOnlineCrawler(AbstractWebCrawler):
    """ [CSOOnline] Web Scraper """

    # Spider Properties
    name = "web_csoonline"

    # Crawler Properties
    resource_link = 'https://www.csoonline.com/news/'
    resource_label = 'csoonline'

    # TODO Move it to the super class
    custom_settings = {
        'ITEM_PIPELINES': {
            'scrapy_crawlers.pipelines.ElasticIndexPipeline': 500
        }
    }

    links_to_articles_query = 'div#page-wrapper section.bodee div.main-col ' \
        'div.article div.post-cont h3 a::attr(href)'
    links_to_pages_query = 'div#page-wrapper section.bodee div.main-col a#load-more-index'
    extract_title_query = 'div#page-wrapper section article header.cat h1::text'
    extract_datetime_query = 'div#page-wrapper section article header.cat span.pub-date::attr(content)'
    extract_content_query = 'div#page-wrapper section article div#drr-container p'
