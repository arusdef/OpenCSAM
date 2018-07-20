import logging
import os
from scrapy.commands.crawl import Command
from scrapy.exceptions import UsageError

class GuardCrawl(Command):

    def run(self, args, opts):
        if len(args) < 1:
            raise UsageError()
        elif len(args) > 1:
            raise UsageError("running 'scrapy crawl' with more than one spider is no longer supported")
        spname = args[0]

        self.crawler_process.crawl(spname, **opts.spargs)
        crawler = list(self.crawler_process.crawlers)[0]
        self.crawler_process.start()

        logging.info(crawler.stats.get_stats())

        error_limit = int(crawler.settings.get('ERROR_LIMIT', os.getenv('ERROR_LIMIT', 0)))
        error_count = int(crawler.stats.get_value('log_count/ERROR', 0))

        if error_count > error_limit:
            self.exitcode = 1