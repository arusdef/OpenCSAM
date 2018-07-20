#!/usr/bin/env python3
"""This example shows how to assign topics to the pdf documents
using cosine similariy between the document text and the glossary definitions."""

from pathlib import Path
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

from keywords import *


path = Path.cwd() / "../../pdf-reports/"
pdf = read_plaintext_with_keywords(path)
pdf = add_chapter_fields(pdf)

path = Path.cwd() / "../keywords/glossary.csv"
glossary = read_glossary(path)

# Vectorize the text from the pdf documents and the glossary definitions.
cv = CountVectorizer(ngram_range=(1, 1), preprocessor=preproc, stop_words='english')
#text1 = pdf['text']
text1 = pdf["all_chapters"]
#text2 = glossary['definition']
# Make sure that the topic itself (not only the definition)
# will be used for the text matching.
text2 = ["{} {}".format(a, b) for (a, b) in zip(glossary['topic'], glossary['definition'])]
text = np.concatenate((text1, text2))
cv.fit(text)
X1 = cv.transform(text1)
X2 = cv.transform(text2)

for (title, keywords, topics, v1) in zip(pdf['title'], pdf['keywords'], pdf['topics'], X1):
    # Calculate cosine similarity between the pdf report and all glossary definitions.
    cosine_similarities = cosine_similarity(v1, X2).flatten() 
    # Find the top 3 related topics.
    related_docs_indices = cosine_similarities.argsort()[:-4:-1]

    print('-' * 80)
    print(title)
    print(keywords)
    print(topics)
    print('-' * 80)
    for i in related_docs_indices:
        print("{:.3f} {}".format(cosine_similarities[i], glossary['topic'].iloc[i]))
