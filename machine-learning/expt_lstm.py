"""
Experiments with LSTM.

Plan:
- Trained embeddings + Vanilla LSTM
- Trained embeddings + Bidirectional LSTM
- ELMo contextualized embeddings + LSTM
- ELMo contextualized embeddings + BiLSTM
"""

import numpy as np
import torch
import torch.nn.functional as F
from sklearn.metrics import f1_score, accuracy_score
from torch import nn
from torch import optim
from torch.nn.utils.rnn import pack_padded_sequence
from torch.utils.data import Dataset, DataLoader
from torch.utils.data.dataset import random_split
from torch.nn.utils import clip_grad_value_
from matplotlib import pyplot as plt

from utils import preprocess, tokenize, load_davidson
from sklearn.utils import class_weight

torch.set_printoptions(profile="full")


class Vocabulary(object):
    """
    Closed vocabulary. Maps unique tokens to integer IDs and vice versa.
    """

    def __init__(self):
        self.PAD_IDX = 0
        self.OOV_IDX = 1
        self.index = 0  # the next available index
        self.token_to_idx = dict()
        self.idx_to_token = dict()
        self.add_token("<PAD>")
        self.add_token("<OOV>")

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

    def __len__(self):
        return len(self.token_to_idx)


class DavidsonDataset(Dataset):
    """
    Helper class for PyTorch data loading.
    """

    def __init__(self, inputs, labels, input_lengths):
        """ Load dataset used in Davidson's paper. """
        assert len(inputs) == len(labels) == len(input_lengths)
        self.inputs = inputs
        self.labels = labels
        self.input_lengths = input_lengths

    def __len__(self):
        return len(self.inputs)

    def __getitem__(self, item):
        return self.inputs[item], self.labels[item], self.input_lengths[item]


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


class HateSpeechLSTMClassifier(nn.Module):
    def __init__(self,
                 vocab_size,
                 pad_idx,
                 device,
                 embedding_dim=128,
                 hidden_size=100,
                 layers=1,
                 dropout=0.,
                 bidirectional=False):
        super().__init__()
        self.device = device
        self.layers = layers
        self.hidden_size = hidden_size

        self.embed = nn.Embedding(
            num_embeddings=vocab_size,
            embedding_dim=embedding_dim,
            padding_idx=pad_idx
        )

        self.lstm = nn.LSTM(
            input_size=embedding_dim,
            hidden_size=hidden_size,
            num_layers=layers,
            batch_first=True,  # input/outputs are (batch, seq, feature)
            dropout=dropout,
            bidirectional=bidirectional
        )

        # O/1 classifier
        self.dropout = nn.Dropout(p=dropout)
        self.hidden_to_tag = nn.Linear(hidden_size, 2)

    def init_hidden(self, batch_size):
        """ Initialize hidden states. """
        h_0 = torch.randn(
            self.layers, batch_size, self.hidden_size).to(self.device)
        c_0 = torch.randn(
            self.layers, batch_size, self.hidden_size).to(self.device)
        return h_0, c_0

    def forward(self, inputs, input_lengths, batch_size):
        self.hidden = self.init_hidden(batch_size)
        x = self.embed(inputs)
        x = pack_padded_sequence(x, input_lengths, batch_first=True,
                                 enforce_sorted=False)
        outputs, (ht, ct) = self.lstm(x, self.hidden)
        output = self.dropout(ht[-1])
        output = self.hidden_to_tag(output)
        output = F.log_softmax(output, dim=1)
        return output


def split_dataset(dataset, ratios):
    """ Split PyTorch dataset into train and validation.

    Ratios: [test_fraction, valid_fraction, test_fraction]
    Usually .6, .2, .2
    """
    assert sum(ratios) == 1
    train, val, test = ratios
    train_size = int(train * len(dataset))
    val_size = int(val * len(dataset))
    test_size = len(dataset) - train_size - val_size
    train_set, val_set, test_set = random_split(
        dataset, [train_size, val_size, test_size])
    return train_set, val_set, test_set


def train(model, criterion, optimizer, train_loader, train_batch_size, val_loader, val_batch_size, device, epochs, eval_every=4):

    # For plotting learning curves
    train_losses = []
    train_accs = []
    val_losses = []
    val_accs = []

    for epoch in range(epochs):
        model.train()
        total_train_loss = 0.
        total_accuracy = 0.
        for inputs, labels, input_lengths in train_loader:
            inputs = inputs.to(device)
            labels = labels.to(device)
            input_lengths = input_lengths.to(device)
            model.zero_grad()
            output = model(inputs, input_lengths, train_batch_size)
            loss = criterion(output, labels)
            total_train_loss += loss.item()
            _, preds = output.max(dim=1)
            acc = (labels == preds).sum().item() / labels.shape[0]
            total_accuracy += acc

            loss.backward()
            clip_grad_value_(model.parameters(), 5.)
            optimizer.step()

        avg_loss = total_train_loss / len(train_loader)
        avg_acc = total_accuracy / len(train_loader)
        train_losses.append(avg_loss)
        train_accs.append(avg_acc)

        print("(Train) Epoch {} Loss {:.4f} Acc {:.4f}".format(epoch + 1, avg_loss, avg_acc))

        if (epoch + 1) % eval_every == 0:
            model.eval()
            loss, accuracy, f1 = evaluate(model, criterion, val_loader,
                                          val_batch_size, device)
            val_losses.append(loss)
            val_accs.append(accuracy)

    if eval_every == 1:
        assert len(train_losses) == len(val_losses)
        x_axis = np.arange(0, len(train_losses))
        plt.plot(x_axis, train_losses, label='train loss')
        plt.plot(x_axis, val_losses, label='validation loss')
        plt.legend()
        plt.show()

        plt.plot(x_axis, train_accs, label='train accuracy')
        plt.plot(x_axis, val_accs, label='validation accuracy')
        plt.legend()
        plt.show()


def evaluate(model, loss_function, val_data_loader, val_batch_size, device):
    """ Evaluate the model and return mean loss, accuracy and F1. """
    with torch.no_grad():
        loss_list = []
        acc_list = []
        y_pred_batches = []
        y_true_batches = []
        for inputs, labels, input_lengths in val_data_loader:
            inputs = inputs.to(device)
            labels = labels.to(device)
            input_lengths = input_lengths.to(device)
            output = model(inputs, input_lengths, val_batch_size)
            loss = loss_function(output, labels)
            loss_list.append(loss.item())

            # Need to move values from GPU to CPU for sklearn score calculations
            _, outputs = output.cpu().max(dim=1)
            labels = labels.cpu()

            acc = accuracy_score(labels, outputs)
            acc_list.append(acc)

            y_pred_batches.append(outputs)
            y_true_batches.append(labels)

        loss_avg = np.mean(loss_list)
        acc_avg = np.mean(acc_list)

        # Might be faster to concatenate batches at the end rather than
        # appending each row to the list in the validation loop
        y_pred = torch.cat(y_pred_batches, dim=0)
        y_true = torch.cat(y_true_batches, dim=0)
        f1_avg = f1_score(y_true, y_pred, average="binary")

        print("(Val)   Loss {:.4f} F1 {:.4f} Acc {:.4f}".format(loss_avg, f1_avg, acc_avg))
        return loss_avg, acc_avg, f1_avg


def main():
    # PyTorch to device
    device_name = "cuda" if torch.cuda.is_available() else "cpu"
    print("Running model on {}...".format(device_name))
    device = torch.device(device_name)

    # Load data and preprocess
    data_path = "./dataset/davison.csv"
    print("Loading data from {}...".format(data_path))
    inputs, labels = load_davidson(data_path)

    print("Preprocessing, tokenizing and padding sequences...")
    inputs = preprocess(inputs)
    inputs = [tokenize(sent) for sent in inputs]
    vocab = Vocabulary.build(inputs)
    inputs = convert_to_idxs(inputs, vocab)
    input_lengths = [len(seq) for seq in inputs]
    inputs = pad_sequences(inputs, vocab)

    # Convert to PyTorch tensors for efficiency
    inputs = torch.tensor(inputs)
    labels = torch.tensor(labels)
    input_lengths = torch.tensor(input_lengths)

    # class weights for unbalanced data
    class_weights = class_weight.compute_class_weight("balanced",
                                                      np.array([0, 1]),
                                                      labels.numpy())
    class_weights = torch.FloatTensor(class_weights).to(device)

    # Training hyperparameters
    train_batch_size = 64
    val_batch_size = 64
    learn_rate = 0.003
    epochs = 1000

    print("Splitting data...")
    davidson_ds = DavidsonDataset(inputs, labels, input_lengths)
    train_set, val_set, test_set = split_dataset(davidson_ds, (0.6, 0.2, 0.2))
    train_loader = DataLoader(train_set,
                              batch_size=train_batch_size,
                              shuffle=True,
                              drop_last=True)
    val_loader = DataLoader(val_set,
                            batch_size=val_batch_size,
                            shuffle=True,
                            drop_last=True)

    # Set up training
    model = HateSpeechLSTMClassifier(len(vocab), vocab.PAD_IDX, device, layers=2, dropout=0.5)
    model = model.to(device)

    criterion = nn.NLLLoss(weight=class_weights)
    optimizer = optim.SGD(model.parameters(), lr=learn_rate)

    print("Begin training...")
    train(model, criterion, optimizer, train_loader, train_batch_size,
          val_loader, val_batch_size, device, epochs, eval_every=20)
    evaluate(model, criterion, val_loader, val_batch_size, device)

    print("Done.")


if __name__ == "__main__":
    main()
