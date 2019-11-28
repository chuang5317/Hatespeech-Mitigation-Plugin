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

# def lookup_tweets(tweet_IDs, api):
#     full_tweets = []
#     tweet_count = len(tweet_IDs)
#     try:
#         for i in range((tweet_count / 100) + 1):
#             # Catch the last group if it is less than 100 tweets
#             end_loc = min((i + 1) * 100, tweet_count)
#             full_tweets.extend(
#                 api.statuses_lookup(id=tweet_IDs[i * 100:end_loc])
#             )
#         return full_tweets
#     except tweepy.TweepError:
#         print 'Something went wrong, quitting...'

# consumer_key = 'XXX'
# consumer_secret = 'XXX'
# access_token = 'XXX'
# access_token_secret = 'XXX'

# auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
# auth.set_access_token(access_token, access_token_secret)

# api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

# # do whatever it is to get por.TweetID - the list of all IDs to look up

# results = lookup_tweets(por.TweetID, api)

# for tweet in results:
#     if tweet:
#         print tweet.text
