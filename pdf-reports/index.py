#!/usr/bin/env python3
"""This script uploads the pdf documents to Elasticsearch."""

import os
from elasticsearch import Elasticsearch
from configparser import ConfigParser
from keywords import *
from pathlib import Path

# Includes dependecies from another project
import sys
sys.path.insert(0, '../enisa-nlp/pdf_documents')
from read_data import read_plaintext_with_keywords
from document_structure import add_chapter_fields

# Read config file.
parser = ConfigParser()
parser.read('index.cfg')

url = os.getenv('ES_URL', parser.get('Elasticsearch', 'url'))
username = os.getenv('ES_USERNAME', parser.get('Elasticsearch', 'username'))
password = os.getenv('ES_PASSWORD', parser.get('Elasticsearch', 'password'))
port = os.getenv('ES_PORT', parser.get('Elasticsearch', 'port'))

# Load documents into a dataframe.
path = Path.cwd()
df = read_plaintext_with_keywords(path)
df = add_chapter_fields(df)
print(df.columns)

# Connect to database.
es = Elasticsearch(url, port=port, http_auth=(username, password), verify_certs=False)

# Upload to database.
records = df.T.to_dict()
records = [records[i] for i in records]
for idx, row in enumerate(records):
    res = es.index(index="pdf_documents", doc_type='document', id=idx, body=row)
    print(res)
