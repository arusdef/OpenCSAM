""" [BleepingComputer] Web Scraper """

import os
from dateutil import parser
from bs4 import BeautifulSoup
from .abstract_crawler import AbstractWebCrawler


class BleepingComputerCrawler(AbstractWebCrawler):
    """ [BleepingComputer] Web Scraper """

    # Spider Properties
    name = "web_bleepingcomputer"

    # Crawler Properties
    resource_link = 'https://bleepingcomputer.com'
    resource_label = 'bleepingcomputer'

    # TODO Move it to the super class
    custom_settings = {
        'ITEM_PIPELINES': {
            'scrapy_crawlers.pipelines.ElasticIndexPipeline': 500
        }
    }

    links_to_articles_query = 'div.bc_latest_news_text h4 a::attr(href)'
    links_to_pages_query = 'ul.cz-pagination li a::attr(href)'
    extract_title_query = 'section.bc_main_content h2::text'
    extract_datetime_query = None
    extract_content_query = 'section.bc_main_content div.articleBody p'

    @classmethod
    def extract_datetime(self, response):
        date_query = 'section.bc_main_content li.cz-news-date::text'
        date = response.css(date_query).extract_first().strip()
        time_query = 'section.bc_main_content li.cz-news-time::text'
        time = response.css(time_query).extract_first().strip()
        return parser.parse(date + ' ' + time)
