import os
import pandas as pd
import preprocessing as pre
import spacy
# import tweepy

# All functions should return a Pandas DataFrame of spacy documents
# e.g. "spacy" "tokens"        "label"              .....more
# 0    doc1    (list of words) (this colum will be created in train.py)
# 1    doc2                     -
# ...  ...      ...

# For plain text.
def get_sample_dataset_from_paintext(folder):
    texts = []
    for file in os.listdir(folder):
        filepath = os.path.join(folder, file)
        f = open(filepath, 'r')
        texts.append(f.read())
        f.close()
    return pre.preprocess(texts)

# different csv have different structure... need individual functions
def get_E6oV3lV():
    addr = "./dataset/train_E6oV3lV.csv"
    original = pd.read_csv(addr)
    texts = original.iloc[:,2].tolist()
    return pre.preprocess(texts)

def get_debug():
    addr = "./dataset/for_debug.csv"
    original = pd.read_csv(addr)
    texts = original.iloc[:,6].tolist()
    return pre.preprocess(texts)

def get_combined():
    addr1 = "./dataset/davison.csv"
    original1 = pd.read_csv(addr1)
    texts = original1.iloc[:,6].tolist()
    addr2 = "./dataset/train_E6oV3lV.csv"
    original2 = pd.read_csv(addr2)
    texts += original2.iloc[:,2].tolist()
    return pre.preprocess(texts)

def get_davison():
    addr = "./dataset/davison.csv"
    original = pd.read_csv(addr)
    texts = original.iloc[:,6].tolist()[:20000]
    return pre.preprocess(texts)

def get_davison_test():
    addr = "./dataset/davison.csv"
    original = pd.read_csv(addr)
    texts = original.iloc[:,6].tolist()[20000:]
    scores = original.iloc[:,5].tolist()[20000:]
    return [scores, texts]

def get_trac_test():
    addr = "./dataset/agr_en_dev.csv"
    original = pd.read_csv(addr)
    texts = original.iloc[:,1]
    scores = original.iloc[:,2]
    return [scores, texts]

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
    train = (texts[:75000], labels[:75000])
    validation = (texts[75000:130000], labels[75000:130000])
    test = (texts[130000:],  labels[130000:])
    return (train, validation, test)