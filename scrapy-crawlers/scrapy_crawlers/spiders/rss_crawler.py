""" RSS Feed Crawler """

import os
import logging
from datetime import datetime
from email.utils import parsedate_tz
from email.utils import mktime_tz
from bs4 import BeautifulSoup
from scrapy import Spider

class RSSCrawler(Spider):
    """ RSS Feed Crawler """

    # Current Attributes
    rss_link = os.getenv('RSS_LINK', 'http://feeds.arstechnica.com/arstechnica/security')
    rss_label = os.getenv('RSS_LABEL', 'arstechnica')

    # Crawler Attributes
    name = "rss_crawler"
    start_urls = [rss_link]

    custom_settings = {
        'ITEM_PIPELINES': {
            'scrapy_crawlers.pipelines.ElasticCreatePipeline': 500
        }
    }

    @classmethod
    def parse(cls, response):
        """ Channel Parser """

        for node in response.xpath('//channel/item'):
            yield cls.parse_node(node)

    @classmethod
    def parse_node(cls, node):
        """ Node Parser """

        body = cls.extract_text(node, 'description/text()') # mandatory field
        text = BeautifulSoup(body, 'lxml').text.strip()

        item = {
            'title': cls.extract_text(node, 'title/text()'), # mandatory field
            'link': cls.extract_text(node, 'link/text()'), # mandatory field
            'content': text,
            'published': cls.extract_date(node, 'pubDate/text()'),
            'resource_type': 'rss',
            'resource_label': cls.rss_label,
        }

        return item

    @classmethod
    def extract_text(cls, node, xpath):
        """ Extracts text with XPath """
        return node.xpath(xpath).extract_first(default='').strip()

    @classmethod
    def extract_date(cls, node, xpath):
        """ Extracts date with XPath """
        return cls.rfc822(cls.extract_text(node, xpath))

    @classmethod
    def extract_array(cls, node, xpath):
        """ Extracts array with XPath """
        return node.xpath(xpath).extract()

    @classmethod
    def rfc822(cls, timestamp):
        """ Converts RFC822 timestamp string to datetime object """
        try:
            return datetime.fromtimestamp(mktime_tz(parsedate_tz(timestamp)))
        except:
            logging.warn("Unable to extract date from [" + timestamp + "]")
            return None
