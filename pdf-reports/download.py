#!/usr/bin/env python3
""" The script scraps remote resources and downloads required PDF files """

import os.path
import urllib.request
from bs4 import BeautifulSoup

ARTICLES = set()
PAGES = set()

def parse(quote_page):
    """ Parse the Page """

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

def download(link):
    """ Download the Thing """

    directory = "documents/"
    if not os.path.exists(directory):
        os.makedirs(directory)

    full_ref = link + "/at_download/fullReport"
    file_name = directory + link.split('/')[-1] + ".pdf"

    if not os.path.isfile(file_name):
        print("Currently downloading " + full_ref)
        urllib.request.urlretrieve(full_ref, file_name)

def main():
    """ Main """

    start_page = 'https://www.enisa.europa.eu/publications/@@faceted_query?b_start:int=0'
    parse(start_page)

    print("---")

    for ref in ARTICLES:
        download(ref)

if __name__ == "__main__":
    main()
