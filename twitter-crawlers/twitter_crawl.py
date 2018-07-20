#!/usr/bin/env python3
"""Twitter Crawl Agent"""

import collections
import logging
import os
import sys

import tweepy
from dateutil import parser
from elasticsearch import Elasticsearch


class TwitterCrawlAgent():
    """Twitter Crawl Agent"""

    logging.basicConfig(level=logging.INFO)

    es_url = os.getenv('ES_URL', 'localhost:9200')
    es_index = os.getenv('ES_INDEX', 'twitter')
    es_type = os.getenv('ES_TYPE', 'tweet')
    es_id = 'id_str'

    tw_consumer_key = os.getenv('TW_CONSUMER_KEY')
    tw_consumer_secret = os.getenv('TW_CONSUMER_SECRET')
    tw_access_token_key = os.getenv('TW_ACCESS_TOKEN_KEY')
    tw_access_token_secret = os.getenv('TW_ACCESS_TOKEN_SECRET')
    tw_limit = int(os.getenv('TW_LIMIT', '50'))
    tw_lang = 'en'
    tw_ids = os.getenv('TW_IDS', 'kaspersky,paulsparrows')

    @classmethod
    def run(cls):
        """Runs the agent"""

        if not cls.tw_consumer_key:
            sys.exit('TW_CONSUMER_KEY is missing')
        if not cls.tw_consumer_secret:
            sys.exit('TW_CONSUMER_SECRET is missing')
        if not cls.tw_access_token_key:
            sys.exit('TW_ACCESS_TOKEN_KEY is missing')
        if not cls.tw_access_token_secret:
            sys.exit('TW_ACCESS_TOKEN_SECRET is missing')

        [cls.load(cls.extract(id.strip())) for id in cls.tw_ids.split(',')]

    @classmethod
    def extract(cls, account_id):
        """Pulls data from twitter"""
        auth = tweepy.OAuthHandler(cls.tw_consumer_key, cls.tw_consumer_secret)
        auth.set_access_token(cls.tw_access_token_key, cls.tw_access_token_secret)
        api = tweepy.API(auth)

        logging.info("Scraping last %s statuses from @%s account", cls.tw_limit, account_id)

        return tweepy.Cursor(api.user_timeline, id=account_id,
                             tweet_mode="extended").items(cls.tw_limit)

    @classmethod
    def load(cls, cursor):
        """Loads data into Elasticsearch"""
        elastic = Elasticsearch(cls.es_url)

        for status in cursor:
            doc = cls.transform(status._json)

            if doc['lang'] != cls.tw_lang:
                logging.warning('Skipping the message (unsupported lang) [id=%s, user=%s, lang=%s]',
                                doc['id_str'], doc['user']['screen_name'], doc['lang'])
            elif (doc['in_reply_to_status_id_str']) or (doc['in_reply_to_user_id_str']):
                logging.warning('Skipping the message (reply) [id=%s, user=%s, lang=%s]',
                                doc['id_str'], doc['user']['screen_name'], doc['lang'])
            else:
                cls.index(elastic, doc)

    @classmethod
    def transform(cls, doc):
        """Updates the document"""
        for key, val in doc.copy().items():
            if isinstance(val, collections.Mapping):
                doc[key] = cls.transform(doc.get(key, {}))
            elif key == 'created_at':
                doc[key] = parser.parse(doc[key])
            elif key == 'media':
                doc.pop(key, None)
            else:
                doc[key] = val
        return doc

    @classmethod
    def index(cls, elastic, doc):
        """Index the document"""
        res = elastic.index(index=cls.es_index, doc_type=cls.es_type, id=doc[cls.es_id], body=doc)
        logging.debug(res)

if __name__ == '__main__':
    TwitterCrawlAgent().run()
