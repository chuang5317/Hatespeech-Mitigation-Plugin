import dataset as ds
import labelingFunctions as lf
from snorkel.labeling import LabelModel, PandasLFApplier
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn import svm
from sklearn.naive_bayes import GaussianNB
import fasttext
import random
import nltk
from nltk.corpus import wordnet as wn
from snorkel.augmentation import transformation_function
import pickle
import pandas as pd

def get_cnn_davison():
    addr = "./dataset/davison.csv"
    original = pd.read_csv(addr)
    texts = original.iloc[:,6].tolist()
    labels = list(map((lambda x: 1 if x == 1 else 0),  original.iloc[:,5].tolist()))
    train = (texts[:20000], labels[:20000])
    test = (texts[20000:], labels[20000:])
    return (train, test)

# Training a Classifier
count_vec = CountVectorizer(ngram_range=(0, 1))
train, test = get_cnn_davison()
X_train = count_vec.fit_transform(train[0])

# over
clf = LogisticRegression(solver="lbfgs", max_iter=1000)
clf.fit(X=X_train, y=train[1])

# save the model to disk
pickle.dump(clf, open("./hate_speech_classifier", 'wb'))
pickle.dump(count_vec, open("./hate_speech_CountVectorizer", 'wb'))
