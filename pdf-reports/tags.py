#!/usr/bin/env python3
"""This script scraps the webpage with ENISA reports and extracts topics and keywords for each of them."""

import urllib.request
from bs4 import BeautifulSoup
import pandas as pd

ARTICLES = set()
PAGES = set()

def parse(quote_page):
    """Parse the page."""

    if quote_page not in PAGES:
        print("Currently processing " + quote_page)
        PAGES.add(quote_page)

        page = urllib.request.urlopen(quote_page)
        soup = BeautifulSoup(page, 'html.parser')

        for link in soup.find_all('a'):
            ref = link.get('href')
            if 'faceted_query' not in ref:
                ARTICLES.add(ref)
            else:
                parse(ref)


TOPICS = set()
KEYWORDS = set()

def get_tags(link):
    """Get topic and keywords."""

    name = link.split('/')[-1]

    topics = set()
    keywords = set()

    page = urllib.request.urlopen(link)
    soup = BeautifulSoup(page, 'html.parser')

    for link in soup.find_all('a'):
        ref = link.get('href')
        if "https://www.enisa.europa.eu/topics/" in ref:
            topics.add(link.string)
            TOPICS.add(link.string)
        if "https://www.enisa.europa.eu/@@search?Subject" in ref:
            keywords.add(link.string)
            KEYWORDS.add(link.string)

    return name, list(topics), list(keywords)


def extract_tags_to_csv(filename):
    """Extract topics and keywords for all articles and save them in a csv file."""

    tags = pd.DataFrame(columns=['name', 'topics', 'keywords'])

    idx = 0
    for ref in ARTICLES:
        name, topics, keywords = get_tags(ref)

        print('-' * 80)
        print(name)
        print('-' * 80)
        print(topics)
        print(keywords)

        tags.loc[idx] = [name, topics, keywords]
        idx += 1

    tags.to_csv(filename, index=False)


def main():
    start_page = 'https://www.enisa.europa.eu/publications/@@faceted_query?b_start:int=0'
    parse(start_page)
    extract_tags_to_csv("tags.csv")

    print("Found {} topics:".format(len(TOPICS)))
    print(sorted(TOPICS))

    print("Found {} keywords:".format(len(KEYWORDS)))
    print(sorted(KEYWORDS))


if __name__ == "__main__":
    main()