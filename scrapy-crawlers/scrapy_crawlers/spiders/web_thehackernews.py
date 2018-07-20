""" [TheHackerNews] Web Scraper """


from .abstract_crawler import AbstractWebCrawler


class TheHackerNewsCrawler(AbstractWebCrawler):
    """ [TheHackerNews] Web Scraper """

    # Spider Properties
    name = "web_thehackernews"

    # Crawler Properties
    resource_link = 'https://thehackernews.com/'
    resource_label = 'thehackernews'

    # TODO Move it to the super class
    custom_settings = {
        'ITEM_PIPELINES': {
            'scrapy_crawlers.pipelines.ElasticIndexPipeline': 500
        }
    }

    links_to_articles_query = '#Blog1 > div.blog-posts.clear > div > a::attr(href)'
    links_to_pages_query = '#Blog1_blog-pager-older-link::attr(href)'
    extract_title_query = 'body > main > div > h1.story-title > a::text'
    extract_datetime_query = '#Blog1 > div > div > div > div.clear.post-head > div > span:nth-child(2)::text'
    extract_content_query = '#articlebody'
