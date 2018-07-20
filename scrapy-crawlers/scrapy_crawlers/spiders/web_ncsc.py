""" [ncsc] Web Scraper """

import os
from .abstract_crawler import AbstractWebCrawler


class NationalCyberSecurityCentreCrawler(AbstractWebCrawler):
    """ [ncsc] Web Scraper """

    # Spider Properties
    name = "web_ncsc"

    # Crawler Properties
    resource_link = 'https://www.ncsc.gov.uk/index/news'
    resource_label = 'ncsc'

    # TODO Move it to the super class
    custom_settings = {
        'ITEM_PIPELINES': {
            'scrapy_crawlers.pipelines.ElasticIndexPipeline': 500
        }
    }

    links_to_articles_query = 'body > div.page-wrap div.container > div.row ul ' \
        '> li > div.result-item-wrapper > h4.field-title a::attr(href)'

    links_to_pages_query = 'body > div.page-wrap div.container div.search-results-list ' \
        'ul li div.result-item-wrapper h4.field-title a::attr(href)'

    extract_title_query = 'body div.page-wrap div.container > div.row h1::text'
    
    extract_datetime_query = 'body div.page-wrap div.container div.row div.field-date-created ' \
        'span.date-display-single::attr(content)'
    
    extract_content_query = '#quicktabs-news_tabs1 > div.tab-contents p'
