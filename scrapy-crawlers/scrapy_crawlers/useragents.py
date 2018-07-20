""" User-Agent Middleware """

import logging
from fake_useragent import UserAgent

class RandomUserAgentMiddleware(object):
    """ Random User-Agent Middleware """

    default_user_agent = ('''Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) '''
    '''AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36''')

    user_agent = UserAgent(verify_ssl=False, fallback=default_user_agent)

    def process_request(self, request, spider):
        """ Process Request """

        random_user_agent = self.user_agent.random
        logging.debug(random_user_agent)

        request.headers.setdefault('User-Agent', random_user_agent)
        return None # continue processing this request