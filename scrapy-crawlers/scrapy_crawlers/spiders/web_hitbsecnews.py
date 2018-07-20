""" [HITBSecNews] Web Scraper """


from .abstract_crawler import AbstractWebCrawler


class HITBSecNewsCrawler(AbstractWebCrawler):
    """ [HITBSecNews] Web Scraper """

    # Spider Properties
    name = "web_hitbsecnews"

    # Crawler Properties
    resource_link = 'https://news.hitb.org/tags/security?q=tags/security&page=1'
    resource_label = 'hitbsecnews'

    # TODO Move it to the super class
    custom_settings = {
        'ITEM_PIPELINES': {
            'scrapy_crawlers.pipelines.ElasticIndexPipeline': 500
        }
    }

    links_to_articles_query = '#content > div.views-element-container > div > div.views-row > article > header > h2 > a::attr(href)'
    links_to_pages_query = '#content > div.views-element-container > div > nav > ul > li:nth-child(3) > a'
    extract_title_query = '#content > article > header > h1 > span::text'
    extract_datetime_query = '#content > article > header > div > div.date.text-right::text'
    extract_content_query = '#content > article > div.content > div > div'

    @classmethod
    def extract_datetime(self, response):
        """Extracts a date-time from the response"""
        query = self.extract_datetime_query
        datetime = response.css(query).extract()[1].strip()
        return parser.parse(datetime)
        
