""" [fireeye] Web Scraper """

import os
from dateutil import parser
from bs4 import BeautifulSoup
from .abstract_crawler import AbstractWebCrawler


class FireEyeCrawler(AbstractWebCrawler):
    """ [fireeye] Web Scraper """

    # Spider Properties
    name = "web_fireeye"

    # Crawler Properties
    resource_link = 'https://www.fireeye.com/blog/threat-research.html'
    resource_label = 'fireeye'

    # TODO Move it to the super class
    custom_settings = {
        'ITEM_PIPELINES': {
            'scrapy_crawlers.pipelines.ElasticIndexPipeline': 500
        }
    }

    links_to_articles_query = 'main div.blog.main div.entries div.blogentry h2 > a::attr(href)'
    links_to_pages_query = 'main div.blog.main div.pagination > ul > li > a::attr(href)'
    extract_title_query = 'main div.blog.main div.title.entrytitle h1::text'
    extract_datetime_query = 'main div.blog.main div.title.entrytitle time.entry-date::attr(content)'
    extract_content_query = 'main div.blog.main div.entrytext.section p'
