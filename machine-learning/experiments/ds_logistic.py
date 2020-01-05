import pandas as pd
def get_davison():
    addr = "./dataset/davison.csv"
    original = pd.read_csv(addr)
    texts = original.iloc[:,6].tolist()
    labels = list(map((lambda x: 0 if x == 2 else 1),  original.iloc[:,5].tolist()))
    train = (texts[:20000], labels[:20000])
    test = (texts[20000:], labels[20000:])
    return (train, test)

def get_toxic():
    addr = "./dataset/jigsaw-toxic-comment-classification-challenge/train.csv"
    original = pd.read_csv(addr)
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

def get_merge():
    dtrain, dtest = get_davison()
    ttrain, ttest = get_toxic()
    (dtraintext, dtrainscore) = dtrain
    (dtesttext, dtestscore) = dtest
    (ttraintext, ttrainscore) = ttrain
    (ttesttext, ttestscore) = ttest
    train = ((dtraintext + ttraintext), (dtrainscore + ttrainscore))
    test = ((dtesttext + ttesttext), (dtestscore + ttestscore))
    return (train, test)
