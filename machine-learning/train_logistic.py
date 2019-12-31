import dataset as ds
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
import random
import pickle
import pandas as pd

def get_davison():
    addr = "./dataset/davison.csv"
    original = pd.read_csv(addr)
    texts = original.iloc[:,6].tolist()
    labels = list(map((lambda x: 1 if x == 1 else 0),  original.iloc[:,5].tolist()))
    train = (texts[:20000], labels[:20000])
    test = (texts[20000:], labels[20000:])
    return (train, test)

def get_toxic():
    addr = "./dataset/jigsaw-toxic-comment-classification-challenge/train.csv"
    original = pd.read_csv(addr)
    print(len(original))
    texts = original.iloc[:,1].tolist()
    separate = original.iloc[:,2:]
    labels = []
    for i in range(len(original)):
        rowList = separate.iloc[i].tolist()
        labels.append(1 if 1 in rowList else 0)
    # print(labels)
    train = (texts[:130000], labels[:130000])
    test = (texts[130000:],  labels[130000:])
    return (train, test)


# Training a Classifier
count_vec = CountVectorizer(ngram_range=(0, 1))
train, test = get_toxic()
X_train = count_vec.fit_transform(train[0])

# over
clf = LogisticRegression(solver="lbfgs", max_iter=1000)
clf.fit(X=X_train, y=train[1])

# save the model to disk
pickle.dump(clf, open("./hate_speech_classifier", 'wb'))
pickle.dump(count_vec, open("./hate_speech_CountVectorizer", 'wb'))
