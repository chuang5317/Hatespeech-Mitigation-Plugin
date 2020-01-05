import pandas as pd
import twython

addr = "./dataset/NAACL_SRW_2016.csv"

CONSUMER_KEY = xxx
CONSUMER_SECRET = xxx
OAUTH_TOKEN = xxx
OAUTH_TOKEN_SECRET = xxx

twitter = twython.Twython(CONSUMER_KEY, CONSUMER_SECRET,OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
data = pd.read_csv(addr)

i = 0
while i < len(data):
    try:
        print(i)
        tweet = twitter.show_status(id=data.iloc[i, 0])
        data.iloc[i, 0] = tweet['text']
        print(tweet['text'])
        i+=1
    except  Exception as e:
        print(e)
        data = data.drop(data.index[i])
        

data.to_csv("./dataset/NAACL_WITH_TEXT.csv")