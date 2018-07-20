""" [TechCrunch] Web Scraper """

import json
import logging
import os
import re
from dateutil import parser
from bs4 import BeautifulSoup
from scrapy import Request
from .abstract_crawler import AbstractWebCrawler


class TechCrunchCrawler(AbstractWebCrawler):
    """ [TechCrunch] Web Scraper """

    # Spider Properties
    name = "web_techcrunch"

    # Crawler Properties
    resource_link = 'https://techcrunch.com/tag/cybersecurity/'
    resource_label = 'techcrunch'

    # TODO Move it to the super class
    custom_settings = {
        'ITEM_PIPELINES': {
            'scrapy_crawlers.pipelines.ElasticIndexPipeline': 500
        }
    }

    links_to_articles_query = None
    links_to_pages_query = None
    extract_title_query = None
    extract_datetime_query = None
    extract_content_query = None

    api_url = 'https://techcrunch.com/wp-json/tc/v1/magazine?_embed=true&_envelope=true&tags=965824&page='
    api_page = 0

    def __init__(self):
        super().__init__()  # Calls __init__ method from base class
        self.start_urls = [self.api_url + str(self.api_page)]

    @classmethod
    def parse(self, response):
        """ References Parser """

        logging.info('Parsing page on %s', response.url)

        jsonresponse = json.loads(response.body_as_unicode())

        # follow links to articles
        for item in jsonresponse['body']:
            content = BeautifulSoup(item['content']['rendered'], 'lxml').text.strip()
            yield {
                'title': item['title']['rendered'],
                'link': item['link'],
                'content': content,
                'published': parser.parse(item['date_gmt']),
                'resource_type': self.resource_type,
                'resource_label': self.resource_label,
            }

        # break scraping if body is empty
        if ('body' not in jsonresponse) or (not jsonresponse['body']):
            return

        # follow pages
        self.api_page = self.api_page + 1
        yield Request(self.api_url + str(self.api_page), callback=self.parse)
