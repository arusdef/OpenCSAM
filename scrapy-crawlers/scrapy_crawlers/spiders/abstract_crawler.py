""" [BleepingComputer] Web Scraper """

import abc
import logging
from dateutil import parser
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import scrapy


class AbstractWebCrawler(scrapy.Spider):
    """Abstract Web Scraper"""

    __metaclass__ = abc.ABCMeta

    def __init__(self):
        super().__init__()  # Calls __init__ method from base class
        self.start_urls = [self.resource_link]
        self.allowed_domains = [urlparse(self.resource_link).hostname]

    resource_type = 'web'

    @classmethod
    def parse(self, response):
        """ References Parser """

        logging.info('Parsing page on %s', response.url)

        # follow links to articles
        for href in self.links_to_articles(response):
            yield response.follow(href, self.parse_article)

        # follow pagination links
        for href in self.links_to_pages(response):
            yield response.follow(href, self.parse)

    # @classmethod TODO would be nice to extract it here
    # def follow_articles(self, response):
    #     """Follows links to articles"""
    #     for href in self.links_to_articles(response):
    #         yield response.follow(href, self.parse_article)

    # @classmethod TODO would be nice to extract it here
    # def follow_pages(self, response):
    #     """Follows links to pages"""
    #     for href in self.links_to_pages(response):
    #         yield response.follow(href, self.parse)

    @classmethod
    def parse_article(self, response):
        """ Articles Parser """

        logging.info('Scraping article on %s', response.url)

        yield {
            'title': self.extract_title(response),
            'link': response.url,
            'content': self.extract_content(response),
            'published': self.extract_datetime(response),
            'resource_type': self.resource_type,
            'resource_label': self.resource_label,
        }

    @abc.abstractproperty
    def resource_link(self):
        """A link to the web resource"""
        pass

    @abc.abstractproperty
    def resource_label(self):
        """A label for the web resource"""
        pass

    @abc.abstractproperty
    def links_to_articles_query(self):
        """Query: Extracts links to the articles"""
        pass

    @classmethod
    def links_to_articles(self, response):
        """Extracts links to the articles"""
        return response.css(self.links_to_articles_query).extract()

    @abc.abstractproperty
    def links_to_pages_query(self):
        """Query: Extracts links to the pages"""
        pass

    @classmethod
    def links_to_pages(self, response):
        """Extracts links to the pages"""
        return response.css(self.links_to_pages_query).extract()

    @abc.abstractproperty
    def extract_title_query(self):
        """Query: Extracts a title from the response"""
        pass

    @classmethod
    def extract_title(self, response):
        """Extracts a title from the response"""
        return response.css(self.extract_title_query).extract_first().strip()

    @abc.abstractproperty
    def extract_datetime_query(self):
        """Query: Extracts a date-time from the response"""
        pass

    @classmethod
    def extract_datetime(self, response):
        """Extracts a date-time from the response"""
        query = self.extract_datetime_query
        datetime = response.css(query).extract_first().strip()
        return parser.parse(datetime)

    @abc.abstractproperty
    def extract_content_query(self):
        """Extracts a content from the response"""
        pass

    @classmethod
    def extract_content(self, response):
        """Extracts a content from the response"""
        body = ' '.join(response.css(self.extract_content_query).extract())
        return BeautifulSoup(body, 'lxml').text.strip()
