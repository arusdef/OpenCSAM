""" [SecurityAffairs] Web Scraper """

import os
from dateutil import parser
from bs4 import BeautifulSoup
from .abstract_crawler import AbstractWebCrawler


class SecurityAffairsCrawler(AbstractWebCrawler):
    """ [SecurityAffairs] Web Scraper """

    # Spider Properties
    name = "web_securityaffairs"

    # Crawler Properties
    resource_link = 'https://securityaffairs.co/wordpress/'
    resource_label = 'securityaffairs'

    # TODO Move it to the super class
    custom_settings = {
        'ITEM_PIPELINES': {
            'scrapy_crawlers.pipelines.ElasticIndexPipeline': 500
        }
    }

    links_to_articles_query = 'div#content_wrapper div.sidebar_content div.post_header_wrapper h3 a::attr(href)'
    links_to_pages_query = '#content_wrapper div.sidebar_content div.pagination a::attr(href)'
    extract_title_query = '#content_wrapper div.sidebar_content div.post_header_wrapper h1.post_title::text'
    extract_datetime_query = 'meta[property="article:published_time"]::attr(content)'
    extract_content_query = '#content_wrapper div.sidebar_content div.post_wrapper div.post_inner_wrapper h2,p'
