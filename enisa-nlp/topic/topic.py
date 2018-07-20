#!/usr/bin/env python3
"""Topic modelling."""

from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.decomposition import NMF
import os
import logging
import sys
from time import time
from datetime import datetime, timedelta

from enisa_elastic.elastic import get_articles, save_topics
from pdf_documents.utils import preproc, tokenizer


# Default number of days in the past that specifies the age of the news articles
# taken into account for the topic modelling.
DEFAULT_DAYS_FROM_TODAY = 7

# Default parameters for vectorizers.
MAX_DF = 0.1
MIN_DF = 0.001
MAX_FEATURES = 1000


def get_lda_pipeline(num_clusters, max_df, min_df, max_features):
    """Return pipeline with count vectorizer and Latent Dirichlet Allocation."""
    cv = CountVectorizer(lowercase=True, stop_words='english', preprocessor=preproc,
                         tokenizer=tokenizer, max_df=max_df, min_df=min_df, max_features=max_features)
    lda = LatentDirichletAllocation(n_components=num_clusters, max_iter=100,
                                    learning_method='online',
                                    random_state=42)
    return Pipeline([
        ("cv", cv),
        ("lda", lda)
    ])


def get_nmf_pipeline(num_clusters, max_df, min_df, max_features):
    """Return pipeline with TF-IDF vectorizer and Non-negative Matrix Factorization."""
    tv = TfidfVectorizer(lowercase=True, stop_words='english', preprocessor=preproc,
                         tokenizer=tokenizer, max_df=max_df, min_df=min_df, max_features=max_features)
    nmf = NMF(n_components=num_clusters, random_state=42,
              beta_loss='kullback-leibler', solver='mu', max_iter=1000, alpha=.1,
              l1_ratio=.5)
    return Pipeline([
        ("tv", tv),
        ("nmf", nmf)
    ])


def get_topics(pipeline, num_keywords):
    """Return topics, i.e. keywords per cluster.

    This function extracts the feature names (actual words) from the fitted vectorizer
    and uses this to return keywords for individual topics from the fitted model.
    """

    vectorizer = pipeline.steps[0][1]
    feature_names = vectorizer.get_feature_names()

    model = pipeline.steps[1][1]
    topics = []
    for component in model.components_:
        topics.append([feature_names[i]
                       for i in component.argsort()[:-num_keywords - 1:-1]])
    return topics


def main():
    # Create logger
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    # Create handler
    handler = logging.StreamHandler(stream=sys.stdout)
    handler.setLevel(logging.DEBUG)

    # Specify the logging format
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    # Add the handler to the logger
    logger.addHandler(handler)

    # Read parameters from the environment variables.
    num_clusters = int(os.getenv('NUM_CLUSTERS', '5'))
    logger.info("NUM_CLUSTERS: {}".format(num_clusters))
    num_keywords = int(os.getenv('NUM_KEYWORDS', '5'))
    logger.info("NUM_KEYWORDS: {}".format(num_keywords))
    model = os.getenv('MODEL', 'NMF')
    logger.info("MODEL: {}".format(model))
    index_news = os.getenv('INDEX_NEWS', 'content')
    logger.info("INDEX_NEWS: {}".format(index_news))
    days_from_today = os.getenv('DAYS_FROM_TODAY', DEFAULT_DAYS_FROM_TODAY)
    date_from = "{:%Y-%m-%d}".format(datetime.today() - timedelta(days_from_today))
    logger.info("DATE_FROM: {}".format(date_from))
    index_topics = os.getenv('INDEX_TOPICS', 'topics')
    logger.info("INDEX_TOPICS: {}".format(index_topics))
    max_df = os.getenv('MAX_DF', MAX_DF)
    logger.info("MAX_DF: {}".format(max_df))
    min_df = os.getenv('MIN_DF', MIN_DF)
    logger.info("MIN_DF: {}".format(min_df))
    max_features = os.getenv('MAX_FEATURES', MAX_FEATURES)
    logger.info("MAX_FEATURES: {}".format(max_features))

    # Select the pipeline.
    get_pipeline = {"LDA": get_lda_pipeline, "NMF": get_nmf_pipeline}
    pipeline = get_pipeline[model](num_clusters, max_df, min_df, max_features)

    # Get recent news articles
    X = get_articles(index_news, date_from)
    logger.info("Number of news articles: {}".format(len(X)))

    # Fit the pipeline for the topic modelling.
    logger.info("Start fitting pipeline.")
    t0 = time()
    pipeline.fit(X)
    logger.info("Done fitting pipeline in %0.3fs." % (time() - t0))
    logger.debug("Vector representation length: {}".format(pipeline.steps[0][1].transform(X[0:1]).shape[1]))
    logger.debug("Vector representation of the 1st article: {}".format(pipeline.steps[0][1].transform(X[0:1])))

    # Retrieve the topics.
    topics = get_topics(pipeline, num_keywords)
    logger.info("Topics: {}".format(topics))

    # Upload the topics into the database.
    #date_today = "{:%Y-%m-%d}".format(datetime.now())
    date_today = datetime.now()
    logger.info("DATE_TODAY = {}".format(date_today))
    res = save_topics(index_topics, topics, date_today)
    logger.info("Result of the uploading to the database: {}".format(res))


if __name__ == "__main__":
    main()


