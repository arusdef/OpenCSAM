""" [Symantec] Web Scraper """

import json
import logging
import os
import re
from urllib.parse import urlparse
from dateutil import parser
from bs4 import BeautifulSoup
from scrapy import Request
from .abstract_crawler import AbstractWebCrawler


class SymantecCrawler(AbstractWebCrawler):
    """ [Symantec] Web Scraper """

    # Spider Properties
    name = "web_symantec"

    # Crawler Properties
    resource_link = 'https://www.symantec.com/blogs/threat-intelligence'
    resource_label = 'symantec'

    # TODO Move it to the super class
    custom_settings = {
        'ITEM_PIPELINES': {
            'scrapy_crawlers.pipelines.ElasticIndexPipeline': 500
        }
    }

    # Sets all css selectors to none
    links_to_articles_query = None
    links_to_pages_query = None
    extract_title_query = None
    extract_datetime_query = None
    extract_content_query = None

    api_url = 'https://content.connect.symantec.com/api/v1/blogs/search?_format=json&blog=221&sort=&sortDirection=&rows=10&page='
    api_page = 1
    link_prefix = 'https://www.symantec.com/blogs'

    def __init__(self):
        super().__init__()  # Calls __init__ method from base class
        self.start_urls = [self.api_url + str(self.api_page)]
        self.allowed_domains = [urlparse(self.api_url).hostname]

    @classmethod
    def parse(self, response):
        """ References Parser """

        logging.info('Parsing page on %s', response.url)

        jsonresponse = json.loads(response.body_as_unicode())

        # follow links to articles
        for item in jsonresponse['results']:
            raw_content = ''.join(e['content'] for e in item['paragraphs'] if 'content' in e)
            content = BeautifulSoup(raw_content, 'lxml').text.strip()
            yield {
                'title': str(item['title']),
                'link': self.link_prefix + str(item['urlAlias']),
                'content': content,
                'published': parser.parse(item['createdDate']),
                'resource_type': self.resource_type,
                'resource_label': self.resource_label,
            }

        # logging.info('>>> ' + str('results' not in jsonresponse))
        # logging.info('>>> ' + str(not jsonresponse['results']))

        # break scraping if results is empty
        if ('results' not in jsonresponse) or (not jsonresponse['results']):
            return

        # follow pages
        self.api_page = self.api_page + 1
        yield Request(self.api_url + str(self.api_page), callback=self.parse)
