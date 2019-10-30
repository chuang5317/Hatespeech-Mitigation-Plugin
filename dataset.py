import os
import pandas as pd
import preprocessing as pre
# All functions should return a Pandas DataFrame of spacy documents
# e.g. 0        "label"
# 0    doc1     (this colum will be created in train.py)
# 1    doc2     -
# ...  ...      ...

# For plain text.
def get_sample_dataset_from_paintext(folder):
    ret = []
    for file in os.listdir(folder):
        filepath = os.path.join(folder, file)
        f = open(filepath, 'r')
        ret.append(pre.preprocess(f.read()))
        f.close()
    return pd.DataFrame(ret)

# different csv have different structure... need individual functions
def get_E6oV3lV():
    ret = []
    addr = "./dataset/train_E6oV3lV.csv"
    original = pd.read_csv(addr)
    texts = original.iloc[:,2].tolist()
    for text in texts:
        ret.append(pre.preprocess(text))
    return pd.DataFrame(ret)

#TODO: get data from tweet id -- use tweepy
