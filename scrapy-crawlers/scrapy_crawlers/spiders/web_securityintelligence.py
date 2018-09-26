""" [SecurityIntelligence] Web Scraper """

import logging
import os
import scrapy
from scrapy import FormRequest
from .abstract_crawler import AbstractWebCrawler


class SecurityIntelligenceCrawler(AbstractWebCrawler):
    """ [SecurityIntelligence] Web Scraper """

    # Spider Properties
    name = "web_securityintelligence"

    # Crawler Properties
    resource_link = 'https://securityintelligence.com/category/topics/'
    resource_label = 'securityintelligence'

    # TODO Move it to the super class
    custom_settings = {
        'ITEM_PIPELINES': {
            'scrapy_crawlers.pipelines.ElasticIndexPipeline': 500
        }
    }

    form_url = 'https://securityintelligence.com/wp-admin/admin-ajax.php'
    form_offset = 0
    form_count = 8

    @classmethod
    def parse(self, response):
        """ References Parser """

        logging.info('Parsing page on %s', response.url)

        # follow links to articles
        for href in self.links_to_articles(response):
            yield response.follow(href, self.parse_article)

        # break scraping if page size is 0
        if len(response.body) == 0:
            return

        # pagination ajax request (8 is a default value on the website)
        yield FormRequest(self.form_url, formdata=self.form_data_and_inc(), callback=self.parse)

    @classmethod
    def form_data_and_inc(self):
        """ Creates form data and increments the offset """
        formdata = {'catid': '310', 'action': 'ajax_load_more',
                    'count': str(self.form_count), 'offset': str(self.form_offset)}
        self.form_offset = self.form_offset + self.form_count
        logging.info('Generated Form Data %s', str(formdata))
        return formdata

    links_to_articles_query = 'article div.row div.content h4 a::attr(href)'
    links_to_pages_query = None
    extract_title_query = '#content > div > div.single.col-lg-12.col-md-12.col-sm-12.col-xs-12 > div > div.post-single.col-lg-6.col-md-6.col-sm-10.col-xs-12 > div > h1::text'
    extract_datetime_query = 'meta[property="article:published_time"]::attr(content)'
    extract_content_query = 'div#content div.row div.single article div.content-wrapper div.body p'
