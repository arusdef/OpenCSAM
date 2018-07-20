#!/usr/bin/env python3
"""This script obtains the keyword description from https://heimdalsecurity.com/glossary"""

from pathlib import Path
import urllib.request
from bs4 import BeautifulSoup
import pandas as pd

GLOSSARY_PATH = Path(__file__).resolve().parent / "glossary.csv"


def read_glossary(path=None):
    if path:
        return pd.read_csv(str(path))
    else:
        return pd.read_csv(str(GLOSSARY_PATH))


def download_glossary():
    url = "https://heimdalsecurity.com/glossary"
    page = urllib.request.urlopen(url)
    soup = BeautifulSoup(page, 'html.parser')

    glossary = pd.DataFrame(columns=['topic', 'definition'])
    idx = 0

    for div in soup.find_all('div', attrs={"class": "glossary-left col-md-8"}):
        h3 = div.select('div > h3')
        p = div.select('div > div > p')

        # Avoid entries without a definition.
        if len(p) > 0:
            topic = h3[0].text
            definition = p[0].text
            print(topic)

            glossary.loc[idx] = [topic, definition]
            idx += 1

    glossary.to_csv(str(GLOSSARY_PATH), index=False)


if __name__ == "__main__":
    download_glossary()
