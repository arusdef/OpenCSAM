""" [Infosecurity] Web Scraper """

import os
from .abstract_crawler import AbstractWebCrawler


class InfosecurityCrawler(AbstractWebCrawler):
    """ [Infosecurity] Web Scraper """

    # Spider Properties
    name = "web_infosecurity"

    # Crawler Properties
    resource_link = 'https://www.infosecurity-magazine.com/news/'
    resource_label = 'infosecurity'

    # TODO Move it to the super class
    custom_settings = {
        'ITEM_PIPELINES': {
            'scrapy_crawlers.pipelines.ElasticIndexPipeline': 500
        }
    }

    links_to_articles_query = 'div#pnlMainContent div.container div#webpages-list ' \
        'div.webpage-item a.webpage-link::attr(href)'
    links_to_pages_query = 'div#pnlMainContent div.container div.pagination a::attr(href)'
    extract_title_query = 'div#pnlMainContent div.container div.overlay h1::text'
    extract_datetime_query = 'div#pnlMainContent div.container div.overlay ' \
        'div.article-meta time::attr(datetime)'
    extract_content_query = 'div#pnlMainContent div.container div.article-body p'
