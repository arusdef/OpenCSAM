#!/usr/bin/env python3
"""This script retrieves the credentials to access Elasticsearch from a configuration file
and provides function to read data into a pandas dataframe.
"""

from elasticsearch import Elasticsearch, helpers
from configparser import ConfigParser
from pathlib import Path
import progressbar
import pandas as pd
import os


#CHUNK_SIZE = 10000

parser = ConfigParser()
parser.read(str(Path(Path(__file__).parent / 'elastic.cfg')))
#parser.read('elastic.cfg')

# Get credentials from environment variables.
# Otherwise, retrieve it from the configuration file.
url = os.getenv('ES_URL', parser.get('Elasticsearch', 'url'))
username = os.getenv('ES_USERNAME', parser.get('Elasticsearch', 'username'))
password = os.getenv('ES_PASSWORD', parser.get('Elasticsearch', 'password'))
port = os.getenv('ES_PORT', parser.get('Elasticsearch', 'port'))

es = Elasticsearch(url, port=port, http_auth=(username, password))

def elastic_to_df(index, from_date=''):
    # Get the number of entries in the index.
    count = es.count(index).get('count')
    print("Total number of entries in the index (without the date selection):", count)

#    # Read all entries from Elasticsearch in chunks.
#    size = min(CHUNK_SIZE, count)
#    print("Reading {} entries from start.".format(size))
#    hits = es.search(index=index, body={}, size=size)['hits']['hits']
#    df = pd.DataFrame(hits)
#
#    for i in range((count - CHUNK_SIZE) // CHUNK_SIZE):
#        offset = (i + 1) * CHUNK_SIZE
#        size = min(CHUNK_SIZE, count - offset)
#        print("Reading {} entries from position {}.".format(size, offset))
#        hits = es.search(index=index, body={}, size=size, from_=offset)['hits']['hits']
#        df.append(pd.DataFrame(hits), ignore_index=True)

    query = None
    if from_date:
        query = {
            "query": {
                "range": {
                    "published": {
                        "gte": "{}".format(from_date)
                    }
                }
            }
        }
    res = helpers.scan(client=es, index=index, query=query)
    idx = 0
    df = pd.DataFrame(columns = ['_id', '_score', '_source'])
    bar = progressbar.ProgressBar(maxval=count,
                                  widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
    bar.start()
    for i in res:
        df.loc[idx] = [i['_id'], i['_score'], i['_source']]
        idx += 1
        bar.update(idx)
    bar.finish()
    print("Total number of retrieved entries:", len(df))

    # Turn the _source items into columns.
    def to_columns(x):
        for k, v in x['_source'].items():
            x[k] = v
        return x

    print("Turning the _source items into columns.")
    return df.apply(to_columns, axis=1).drop(columns=['_source']).sort_values(by=['_id'])


def get_articles(index, from_date):
    """Get the text of the news articles as pandas series.
    The text is taken either from the content filed, which is populated by web scrapers.
    In case this field is empty, the description field, populated by RSS feeds, is taken.

    Args:
        index: Index to use (either websites or rssfeeds).
        from_date: Date to select the recent articles only.

    Returns:
        Pandas series with the text of the news articles.
    """

    def get_text(row):
        return row['content'] # if row['content'] == '' else row['description']

    df = elastic_to_df(index, from_date)
    return df.apply(get_text, axis=1)


def save_topics(index, topics, date):
    """Upload the topics into the database.
    The topics index is used for this.
    The keywords are saved in separate fields for individual clusters.

    Args:
        index: Index to store the topics.
        topics: List of lists of keywords for individual clusters.
        date: Timestamp.

    Returns:
        Result of the uploading.
    """

    doc = {}
    doc["date"] = date
    for i in range(len(topics)):
        doc["cluster{}".format(i)] = topics[i]
    res = es.index(index=index, doc_type='topics', body=doc)
    return res['result']