"""
Experiments with LSTM.

Plan:
- Trained embeddings + Vanilla LSTM
- Trained embeddings + Bidirectional LSTM
- ELMo contextualized embeddings + LSTM
- ELMo contextualized embeddings + BiLSTM
"""

import pandas as pd
from .utils import preprocess, tokenize, STOP_WORDS


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


