"""
Experiment with sklearn's SGDClassifier and batch training.
"""
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import SGDClassifier
from sklearn import metrics
from sklearn.utils.class_weight import compute_class_weight
from .utils import preprocess, tokenize, STOP_WORDS


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


def get_bag_of_words(sentences):
    """ Convert sentences into a Bag-of-Words representation (for baseline).

    Later we should use dense embeddings instead (e.g. Word2Vec, Glove),
    training from scratch (e.g. PyTorch Embedding()) or even better
    contextualized embeddings (ELMo).
    """
    count_vectorizer = CountVectorizer(
        ngram_range=(1, 1),
        # tokenizer=tokenize,
        stop_words=STOP_WORDS,
        max_features=1000)
    bow = count_vectorizer.fit_transform(sentences)
    matrix = bow.toarray()
    # plot_bow_distribution(matrix, count_vectorizer)
    return matrix, count_vectorizer


def plot_bow_distribution(bow_matrix, cv):
    """ Plot the distribution of words. For tweaking BoW params. """
    features = cv.get_feature_names()
    counts = bow_matrix.sum(axis=0)
    plt.bar(features, counts)
    plt.xticks(rotation=90)
    plt.show()


def batch_iterator(batch_size, x_data, y_data):
    """ An generator that outputs batches lazily. """
    assert batch_size > 0
    assert (x_data.shape[0] == y_data.shape[0])

    for offset in range(0, x_data.shape[0], batch_size):
        x_batch = x_data[offset:offset + batch_size, :]
        y_batch = y_data[offset:offset + batch_size]
        yield x_batch, y_batch


def shuffle_data(x_data, y_data):
    """ In-place shuffle inputs and labels and preserve relative order. """
    assert(x_data.shape[0] == y_data.shape[0])
    indices = np.arange(x_data.shape[0])
    np.random.shuffle(indices)
    x_data[:] = x_data[indices]
    y_data[:] = y_data[indices]


def demo(model, vectorizer):
    """ Test model with a single sentences from the user. """
    while True:
        raw_input = input("> ")
        sentence = preprocess([raw_input])
        vec = vectorizer.transform(sentence)
        answer = model.predict(vec)
        print(answer)


def train(model, X_train, y_train, X_val, y_val, epochs, batch_size,
          print_every=32):
    # Training loop
    # We implement our own loop instead of one call to sklearn's fit()
    # for better customizability and allow for minibatch learning.
    # Good reference: https://scikit-learn.org/0.15/auto_examples/applications/plot_out_of_core_classification.html#example-applications-plot-out-of-core-classification-py

    print("Begin training loop...")
    for epoch in range(1, epochs + 1):
        # print("Epoch {}".format(epoch))

        # SGD preparation
        shuffle_data(X_train, y_train)
        batches = batch_iterator(batch_size, X_train, y_train)

        # SGD
        for batch_idx, (inputs, labels) in enumerate(batches):
            # if batch_idx % print_every == 0:
            #     print("Epoch {} Batch {}".format(epoch, batch_idx))
            # Handles everything else (feed forward -> back prop -> update)
            model.partial_fit(inputs, labels, classes=[0, 1])

        y_train_pred = model.predict(X_train)
        accuracy = metrics.accuracy_score(y_train, y_train_pred)
        precision = metrics.precision_score(y_train, y_train_pred)
        recall = metrics.precision_score(y_train, y_train_pred)
        f1 = metrics.f1_score(y_train, y_train_pred)
        print(
            "Epoch {:<4} Train Acc {:.4f} Prec {:.4f} Rec {:.4f} F1 {:.4f}".format(
                epoch, accuracy, precision, recall, f1))

        y_val_pred = model.predict(X_val)
        accuracy = metrics.accuracy_score(y_val, y_val_pred)
        precision = metrics.precision_score(y_val, y_val_pred)
        recall = metrics.precision_score(y_val, y_val_pred)
        f1 = metrics.f1_score(y_val, y_val_pred)
        print(
            "Epoch {:<4} Val   Acc {:.4f} Prec {:.4f} Rec {:.4f} F1 {:.4f}".format(
                epoch, accuracy, precision, recall, f1))
        print("---")

        # print("Epoch {} Val accuracy {}".format(epoch, model.score(X_val, y_val)))


def main():
    print("Loading data...")
    inputs, labels = load_davidson("./dataset/davison.csv")
    y_all = np.array(labels)

    print("Preprocessing sentences...")
    inputs = preprocess(inputs)

    print("Generating bag of words...")
    X_all, vectorizer = get_bag_of_words(inputs)

    # Train/test split
    print("Splitting data...")
    test_size = 0.4
    batch_size = 64
    epochs = 1000
    X_train, X_test, y_train, y_test = train_test_split(
        X_all, y_all, test_size=test_size)

    # For unbalanced data set. SGDClassifier requires a dict
    class_weights = compute_class_weight("balanced", [0, 1], y_train)
    class_weight_dict = {0: class_weights[0], 1: class_weights[1]}

    # TODO: set and tune hyperparameters
    model = SGDClassifier(
        loss="log",
        penalty="l2",
        learning_rate="constant",
        eta0=0.03,
        class_weight=class_weight_dict
    )

    # TODO: validation set or k-fold CV
    X_val = X_test
    y_val = y_test

    train(model, X_train, y_train, X_val, y_val, epochs, batch_size)


if __name__ == "__main__":
    main()



