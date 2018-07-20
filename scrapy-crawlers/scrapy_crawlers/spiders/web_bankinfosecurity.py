""" [BankInfoSecurity] Web Scraper """

import os
from dateutil import parser
from bs4 import BeautifulSoup
from .abstract_crawler import AbstractWebCrawler


class BankInfoSecurityCrawler(AbstractWebCrawler):
    """ [BankInfoSecurity] Web Scraper """

    # Spider Properties
    name = "web_bankinfosecurity"

    # Crawler Properties
    resource_link = 'https://www.bankinfosecurity.com/latest-news'
    resource_label = 'bankinfosecurity'

    # TODO Move it to the super class
    custom_settings = {
        'ITEM_PIPELINES': {
            'scrapy_crawlers.pipelines.ElasticIndexPipeline': 500
        }
    }

    links_to_articles_query = '#main #content section#latest-news-page article h2.title a::attr(href)'
    links_to_pages_query = '#main #content #paginator ul.pagination li a::attr(href)'
    extract_title_query = '#main #content article .article-title::text'
    extract_datetime_query = '#main #content article span.article-byline span.text-nowrap::text'
    extract_content_query = '#main #content article p:not(.text-muted)'
