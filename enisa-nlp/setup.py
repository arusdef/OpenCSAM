import os
import nltk

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.md')).read()

nltk.download('punkt') # Please use the NLTK Downloader to obtain the resource

setup(
    name='enisa-nlp',
    version='1.0.0',
    description='',
    long_description=README,
    packages=['enisa_elastic', 'knowledge_graph', 'pdf_documents', 'topic'],
    package_data={'enisa_elastic': ['*.cfg'], 'knowledge_graph': ['*.cfg']}
)
