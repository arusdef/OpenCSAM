""" [wired] Web Scraper """

import os
from .abstract_crawler import AbstractWebCrawler


class WiredCrawler(AbstractWebCrawler):
    """ [wired] Web Scraper """

    # Spider Properties
    name = "web_wired"

    # Crawler Properties
    resource_link = 'https://www.wired.com/category/security/page/1/'
    resource_label = 'wired'

    # TODO Move it to the super class
    custom_settings = {
        'ITEM_PIPELINES': {
            'scrapy_crawlers.pipelines.ElasticIndexPipeline': 500
        }
    }

    links_to_articles_query = '#app-root div.page-loader-component div.archive-listing-main-component \
        div.archive-listing-component div.archive-list-component ul li a.archive-item-component__link::attr(href)'
    links_to_pages_query = '#app-root div.page-loader-component div.archive-listing-main-component \
        div.archive-listing-component > nav.pagination-component > ul > span > li > a::attr(href)'
    extract_title_query = '#articleTitleFull::text'
    extract_datetime_query = 'meta[name=parsely-pub-date]::attr(content)'
    extract_content_query = '#app-root main > article p'
