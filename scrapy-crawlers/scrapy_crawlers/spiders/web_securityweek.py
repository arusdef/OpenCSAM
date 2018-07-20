""" [securityweek] Web Scraper """

import os
from dateutil import parser
from .abstract_crawler import AbstractWebCrawler


class SecurityWeekCrawler(AbstractWebCrawler):
    """ [securityweek] Web Scraper """

    # Spider Properties
    name = "web_securityweek"

    # Crawler Properties
    resource_link = 'https://www.securityweek.com/'
    resource_label = 'securityweek'

    # TODO Move it to the super class
    custom_settings = {
        'ITEM_PIPELINES': {
            'scrapy_crawlers.pipelines.ElasticIndexPipeline': 500
        }
    }

    links_to_articles_query = '#front-page > div.center-wrapper > div.panel-col-last.panel-panel ' \
        'div.view-content > div.views-row > div.views-field-view-node > span > a::attr(href)'
    links_to_pages_query = '#front-page > div.center-wrapper > div.panel-col-last.panel-panel ' \
        'div.item-list > ul > li.pager-next.last > a::attr(href)'
    extract_title_query = '#center > h2::text'
    extract_datetime_query = 'div.meta > div > div:nth-child(1)::text'
    extract_content_query = 'div.content.clear-block > p'

    @classmethod
    def extract_datetime(self, response):
        """Extracts a date-time from the response"""
        query = self.extract_datetime_query
        extracted = response.css(query).extract()[1]
        return parser.parse(extracted)
