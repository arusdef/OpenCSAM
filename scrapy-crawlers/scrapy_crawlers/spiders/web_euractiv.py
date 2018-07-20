""" [Euractive Cybersecurity] Web Scraper """

from .abstract_crawler import AbstractWebCrawler


class EuractivCrawler(AbstractWebCrawler):
    """ [Euractiv Cybersecurity] Web Scraper """

    # Spider Properties
    name = "web_euractiv"

    # Crawler Properties
    resource_link = 'https://www.euractiv.com/sections/cybersecurity/'
    resource_label = 'euractiv'

    # TODO Move it to the super class
    custom_settings = {
        'ITEM_PIPELINES': {
            'scrapy_crawlers.pipelines.ElasticIndexPipeline': 500
        }
    }

    links_to_articles_query_first_page = 'div#main_container section.ea-archive-body.row ' \
                                         'div.ea-archive.col-xs-12.col-sm-12.col-md-8.col-lg-9 ' \
                                         'div.ea-cards.row div.ea-card.col-xs-12.col-sm-6.col-md-6.col-lg-4 ' \
                                         'div.thumbnail div.caption h3 a::attr(href)'
    links_to_articles_query_next_page = 'div#main_container section.ea-archive-body.row ' \
                                        'div.ea-archive.col-xs-12.col-sm-12.col-md-8.col-lg-9 ' \
                                        'ul.ea-card-listing li.ea-card-listing.row ' \
                                        'div.caption h3 a::attr(href)'

    links_to_pages_query = 'div#main_container section.ea-archive-body.row ' \
                           'div.ea-archive.col-xs-12.col-sm-12.col-md-8.col-lg-9 div.col-xs-12.a ' \
                           'span.pagination-link a::attr(href)'

    extract_title_query = 'div#main_container section.ea-post-title h1::text'
    extract_datetime_query = 'meta[property=article\:published_time]::attr(content)'
    extract_content_query = 'div#main_container section.row article.ea-article.col-xs-12.col-sm-12.col-md-8.col-lg-8 ' \
                            'div.ea-article-body div.ea-article-body-content p'

    @classmethod
    def links_to_articles(cls, response):
        """Extracts links to the articles"""
        links = response.css(cls.links_to_articles_query_next_page).extract()
        if not links:
            links = response.css(cls.links_to_articles_query_first_page).extract()
        return links

