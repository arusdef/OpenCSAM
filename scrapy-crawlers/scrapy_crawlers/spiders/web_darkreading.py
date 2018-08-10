""" [Darkreading] Web Scraper """

import os
import logging
from scrapy import Request
from scrapy.exceptions import CloseSpider
from dateutil import parser
from .abstract_crawler import AbstractWebCrawler


class DarkreadingCrawler(AbstractWebCrawler):
    """ [Darkreading] Web Scraper """

    # Spider Properties
    name = "web_darkreading"

    # Crawler Properties
    resource_link = 'https://www.darkreading.com/archives.asp?tag_id=644'
    resource_label = 'darkreading'

    # TODO Move it to the super class
    custom_settings = {
        'ITEM_PIPELINES': {
            'scrapy_crawlers.pipelines.ElasticIndexPipeline': 500
        }
    }

    # Sets all css selectors to none
    links_to_articles_query = 'div.listdocitem > span.blue.strong.medium > a::attr(href)'
    links_to_months_query = '#menu_box_archives > div:nth-child(1) > ul > li > a::attr(href)'
    links_to_pages_query = 'span.blue.strong.allcaps:nth-child(1) > a:nth-child(1)::attr(href)'
    extract_title_query = 'div#article-main > header > h1.larger.blue::text'
    extract_datetime_query = '#aside-inner > div:nth-child(1) > span::text'
    extract_content_query = 'div#article-main'

    @classmethod
    def parse(self, response):
        """Parse the months only once delegating to parse_month to parse the articles and follow the pagination."""
        for href in self.links_to_months(response):
            yield response.follow(href, self.parse_month)

    @classmethod
    def parse_month(self, response):
        """ References Parser """

        logging.info('Parsing page on %s', response.url)

        # follow links to articles
        for href in self.links_to_articles(response):
            yield response.follow(href, self.parse_article)

        # follow pagination links
        for href in self.links_to_pages(response):
            yield response.follow(href, self.parse_month)

    @classmethod
    def parse_article(self, response):
        if "Looks like you've hit your article limit." in response.body_as_unicode():
            raise CloseSpider('Reading quota limit exceeded')
        else:
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

    @classmethod
    def links_to_months(self, response):
        """Extracts the list of links per month from the response"""
        query = self.links_to_months_query
        return response.css(query).extract()

    @classmethod
    def extract_datetime(self, response):
        """Extracts a date-time from the response"""
        query = self.extract_datetime_query
        datetime = ' '.join(response.css(query).extract())
        return parser.parse(datetime)
