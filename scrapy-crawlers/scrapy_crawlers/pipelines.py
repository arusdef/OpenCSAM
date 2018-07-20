# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import hashlib
import logging
import os
from elasticsearch import Elasticsearch
from elasticsearch import exceptions


class ScrapyCrawlersPipeline(object):
    def process_item(self, item, spider):
        return item


class ElasticCreatePipeline(object):

    logger = logging.getLogger('elasticsearch')
    es_id = 'link'

    def __init__(self, es_url, es_index, es_type):
        self.es_url = es_url
        self.es_index = es_index
        self.es_type = es_type

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            es_url=crawler.settings.get('ES_URL', os.getenv('ES_URL', 'localhost:9200')),
            es_index=crawler.settings.get('ES_INDEX', os.getenv('ES_INDEX', 'content')),
            es_type=crawler.settings.get('ES_TYPE', os.getenv('ES_TYPE', 'article')),
        )

    def open_spider(self, spider):
        self.elastic = Elasticsearch(self.es_url)

    def process_item(self, item, spider):
        item_id = get_id(item, self.es_id)
        try:
            res = self.elastic.create(index=self.es_index, doc_type=self.es_type, id=item_id, body=item)
            self.logger.debug(res)
        except exceptions.ConflictError:
            self.logger.warn('version conflict, ' + item_id + ' document already exists')
        return item


class ElasticIndexPipeline(object):

    logger = logging.getLogger('elasticsearch')
    es_id = 'link'

    def __init__(self, es_url, es_index, es_type):
        self.es_url = es_url
        self.es_index = es_index
        self.es_type = es_type

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            es_url=crawler.settings.get('ES_URL', os.getenv('ES_URL', 'localhost:9200')),
            es_index=crawler.settings.get('ES_INDEX', os.getenv('ES_INDEX', 'content')),
            es_type=crawler.settings.get('ES_TYPE', os.getenv('ES_TYPE', 'article')),
        )

    def open_spider(self, spider):
        self.elastic = Elasticsearch(self.es_url)

    def process_item(self, item, spider):
        item_id = get_id(item, self.es_id)
        res = self.elastic.index(index=self.es_index, doc_type=self.es_type, id=item_id, body=item)
        self.logger.debug(res)
        return item


def get_id(item, es_id):
    item_unique_key = item[es_id]
    if isinstance(item_unique_key, list):
        item_unique_key = '-'.join(item_unique_key)

    unique_key = process_unique_key(item_unique_key)
    item_id = hashlib.sha1(unique_key).hexdigest()
    return item_id

def process_unique_key(unique_key):
    if isinstance(unique_key, list):
        unique_key = unique_key[0].encode('utf-8')
    elif isinstance(unique_key, ("".__class__, u"".__class__)):
        unique_key = unique_key.encode('utf-8')
    else:
        raise Exception('unique key must be str or unicode')

    return unique_key