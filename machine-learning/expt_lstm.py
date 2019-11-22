"""
Experiments with LSTM.

Plan:
- Trained embeddings + Vanilla LSTM
- Trained embeddings + Bidirectional LSTM
- ELMo contextualized embeddings + LSTM
- ELMo contextualized embeddings + BiLSTM
"""

import pandas as pd
from utils import load_davidson, preprocess, tokenize, STOP_WORDS
import torch
from torch.utils.data import Dataset, DataLoader
import numpy as np


class Vocabulary(object):
    """
    Closed vocabulary. Maps unique tokens to integer IDs and vice versa.
    """
    def __init__(self):
        self.PAD_IDX = 0
        self.OOV_IDX = 1
        self.index = 2  # the next available index
        self.token_to_idx = dict()
        self.idx_to_token = dict()
        self.token_to_idx["<PAD>"] = 0
        self.idx_to_token[0] = "<PAD>"

    def add_token(self, token):
        """ Add a new token and assign it an unique ID.s """
        if token in self.token_to_idx:
            return

        idx = self.index
        self.token_to_idx[token] = idx
        self.idx_to_token[idx] = token
        self.index += 1

    def get_id(self, token):
        """ Return integer ID of string token, 0 if not found. """
        return self.token_to_idx.get(token, self.OOV_IDX)

    @staticmethod
    def build(inputs):
        """ Build given a list of sentences (list of string tokens). """
        vocab = Vocabulary()
        for token_list in inputs:
            for token in token_list:
                vocab.add_token(token)
        return vocab


class DavidsonDataset(Dataset):
    """
    Helper class for PyTorch data loading.
    """
    def __init__(self, inputs, labels):
        """ Load dataset used in Davidson's paper. """
        assert len(inputs) == len(labels)
        self.inputs = inputs
        self.labels = labels

    def __len__(self):
        return len(self.inputs)

    def __getitem__(self, item):
        return self.inputs[item], self.labels[item]


def convert_to_idxs(sentences, vocabulary):
    """ Convert each sentence to a list of token ids. """
    return [[vocabulary.get_id(token) for token in sent] for sent in sentences]


def pad_sequences(sentence_ids, vocabulary):
    """ Make sure each sentence (list of token IDs) is the same length by
    padding each sentence with dummy <PAD> tokens.
    The vocabulary has the reserved integer ID for <PAD> tokens. """

    # Some people set a cut-off limit (e.g. 512 words), but the sentences in our
    # data sets aren't too long, so just set the limit to the length of the
    # longest sentence.
    max_sentence_len = max(len(sent) for sent in sentence_ids)
    array = np.ones((len(sentence_ids), max_sentence_len))

    res = []
    for sent in sentence_ids:
        tmp = sent[:]
        pad_length = max_sentence_len - len(sent)
        tmp.extend([vocabulary.PAD_IDX for _ in range(pad_length)])
        res.append(tmp)
    return res


if __name__ == "__main__":
    # inputs, labels = load_davidson("./dataset/davison.csv")
    inputs = [
        "Mary had a little lamb...",
        "The quick, brown Fox jumps over the lazy dog!!!",
        "Hello, how are you today?",
        "You should go and die!"
    ]
    labels = 0, 0, 0, 1
    inputs = preprocess(inputs)
    inputs = [tokenize(sent) for sent in inputs]
    vocab = Vocabulary.build(inputs)
    inputs = convert_to_idxs(inputs, vocab)
    inputs = pad_sequences(inputs, vocab)

    inputs = torch.tensor(inputs)
    labels = torch.tensor(labels)

    davidson_ds = DavidsonDataset(inputs, labels)
