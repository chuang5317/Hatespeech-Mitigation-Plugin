"""
Experiments with LSTM.

Plan:
- Trained embeddings + Vanilla LSTM
- Trained embeddings + Bidirectional LSTM
- ELMo contextualized embeddings + LSTM
- ELMo contextualized embeddings + BiLSTM
"""

import re
import string

import nltk
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import SGDClassifier
from sklearn import metrics
from sklearn.utils.class_weight import compute_class_weight


STOP_WORDS = stopwords.words('english')


def load_davidson(path):
    """ Load dataset used in Davidson's paper. """
    original = pd.read_csv(path)

    # Only select relevant columns
    # Relabel data to just the text and 0/1 (not/is hate speech)
    HATESPEECH = 0
    OFFENSIVE = 1
    NEITHER = 2

    df = original[["tweet", "class"]].copy()
    hate_speech = df.index[df["class"] == HATESPEECH]
    other = df.index[df["class"].isin([OFFENSIVE, NEITHER])]
    df.loc[hate_speech, "class"] = 1
    df.loc[other, "class"] = 0
    texts = df["tweet"].tolist()
    labels = df["class"].tolist()
    return texts, labels


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


def tokenize(sentence):
    """ Convert a single sentence string to a list of tokens. """
    return nltk.word_tokenize(sentence)


class Vocabulary:
    """
    Closed vocabulary. Maps unique tokens to integer IDs and vice versa.
    """
    def __init__(self):
        self.token_to_idx = dict()
        self.idx_to_token = list()

    def add_token(self, token):
        assert token not in self.token_to_idx
        idx = len(self.token_to_idx)
        self.token_to_idx[token] = idx
        self.idx_to_token[idx] = token

    def get_id(self, token):
        """ Return integer ID of string token, None if not found. """
        return self.token_to_idx.get(token)


