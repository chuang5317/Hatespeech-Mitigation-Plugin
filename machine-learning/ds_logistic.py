import pandas as pd
from boto3 import resource
from boto3.dynamodb.conditions import Key

# The boto3 dynamoDB resource
dynamodb_resource = resource('dynamodb', region_name='us-east-1')

def scan_table_allpages(table_name, filter_key=None, filter_value=None):
    """
    Perform a scan operation on table.
    Can specify filter_key (col name) and its value to be filtered.
    This gets all pages of results. Returns list of items.
    """
    table = dynamodb_resource.Table(table_name)

    if filter_key and filter_value:
        filtering_exp = Key(filter_key).eq(filter_value)
        response = table.scan(FilterExpression=filtering_exp)
    else:
        response = table.scan()

    items = response['Items']
    while True:
        if response.get('LastEvaluatedKey'):
            response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
            items += response['Items']
        else:
            break

    return items

def get_dynamo():
    items = scan_table_allpages("Hatespeech_incorrect_labels")
    train = ([item["sentence"] for item in items], list(map(lambda x: 0 if x == "Non-offensive" else 1, [item["label"] for item in items])))
    return train

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
    dbtext, dbscore = get_dynamo()
    train = ((dtraintext + ttraintext + dbtext), (dtrainscore + ttrainscore + dbscore))
    test = ((dtesttext + ttesttext), (dtestscore + ttestscore))
    return (train, test)
