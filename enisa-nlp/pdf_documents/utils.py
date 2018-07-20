from nltk import word_tokenize
from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction import stop_words
import re

REGEX_STOP_WORDS = r"\b("
REGEX_STOP_WORDS += '|'.join(stop_words.ENGLISH_STOP_WORDS)
REGEX_STOP_WORDS += r")\b"

def remove_url(s):
    """Remove URLs from a string."""
    return re.sub(r'http\S+', '', s, flags=re.MULTILINE)

def strip_tags(s):
    """Basic regexp based HTML / XML tag stripper function
    For serious HTML/XML preprocessing you should rather use an external
    library such as lxml or BeautifulSoup.
    """
    s = re.compile(r"<([^>]+)>", flags=re.UNICODE).sub(" ", s)
    #s = re.compile(r"\&\w+\;").sub(" ", s)
    s = re.compile(r"\&[^ ]+\;").sub(" ", s)
    return s

def stop_words(s):
    """Remove English stop words from a string."""
    return re.compile(REGEX_STOP_WORDS).sub(" ", s)
    
def preproc(s):
    return stop_words(strip_tags(remove_url(s.lower())))


def tokenizer(text):
    #ps = PorterStemmer()
    #return [ps.stem(w).lower() for w in word_tokenize(text) if w.isalpha() and len(w)>1]
    return [w.lower() for w in word_tokenize(text) if w.isalpha() and len(w)>1]


class Preprocess(object):
    def __init__(self, preproc):
        self.preproc = preproc

    def fit(self, X, y):
        return self

    def transform(self, X):
        return([self.preproc(x) for x in X])
