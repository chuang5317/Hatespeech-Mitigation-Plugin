"""
Miscellaneous helper functions (e.g. text preprocessing)
"""
import nltk
from nltk.corpus import stopwords
import re
import string


STOP_WORDS = stopwords.words('english')


def tokenize(sentence):
    """ Convert a single sentence string to a list of tokens. """
    return nltk.word_tokenize(sentence)


def preprocess(sentences):
    """ Preprocess input text. """
    res = []
    for sentence in sentences:
        # Convert to lower case and remove punctuation and remove numbers
        # Could remove stopwords, keep tweet hashtags, lemmatize, POS tag etc.
        new_sentence = sentence.lower()
        new_sentence = new_sentence.translate(
            str.maketrans("", "", string.punctuation))
        new_sentence = re.sub(r"\d+", "", new_sentence)
        res.append(new_sentence)
    return res