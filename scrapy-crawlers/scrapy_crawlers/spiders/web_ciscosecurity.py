""" [Naked Security] Web Scraper """

import os

from bs4 import BeautifulSoup
from .abstract_crawler import AbstractWebCrawler


class CiscoSecurityCrawler(AbstractWebCrawler):
    """ [Cisco Security] Web Scraper """

    # Spider Properties
    name = "web_ciscosecurity"

    # Crawler Properties
    resource_link = 'https://blogs.cisco.com/security'
    resource_label = 'ciscosecurity'

    # TODO Move it to the super class
    custom_settings = {
        'ELASTICSEARCH_SERVERS': os.getenv('ES_URL', 'localhost:9200'),
        'ELASTICSEARCH_INDEX': os.getenv('ES_INDEX', 'default'),
        'ELASTICSEARCH_TYPE': os.getenv('ES_TYPE', 'default'),
    }

    links_to_articles_query = 'div#sb-site div#main_content div#blog_content div#main_left article#category_content ' \
                              'ul.listings li.tab_posts h2 a::attr(href)'
    links_to_pages_query = 'div#sb-site div#main_content div#blog_content div#main_left article#category_content ' \
                           'div.pagination a::attr(href)'
    extract_title_query = 'div#sb-site div#main_content div#blog_content div#main_left article#article_post ' \
                          'div#post_info h1.kindle_title.title::text'
    extract_datetime_query = 'meta[property=article\:published_time]::attr(content)'
    extract_full_content_query = 'div#sb-site div#main_content div#blog_content div#main_left article#article_post ' \
                                 'div#content p'
    extract_short_content_query = 'div#sb-site div#main_content div#blog_content div#main_left article#article_post p'

    @classmethod
    def extract_content(self, response):
        """Extracts a content from the response"""
        body = ' '.join(response.css(self.extract_full_content_query).extract())
        if not body:
            # it seems to be short article leading to talos, reading just short description
            # TODO: Discuss whether jumping to subpage "read more" would be better than just reading short version here
            body = ' '.join(response.css(self.extract_short_content_query).extract()[1:])
        return BeautifulSoup(body, 'lxml').text.strip()
