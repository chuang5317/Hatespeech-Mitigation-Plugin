import pandas as pd
import twython

addr = "./dataset/NAACL_SRW_2016.csv"

CONSUMER_KEY = 'KW2Fuz056G4aiRoCYgMAI9TKc'
CONSUMER_SECRET = 'QAaw2llacbfQW9TKuwqvKNk0GLuARU1aS2Gq1OLed5ZhQOGAek'
OAUTH_TOKEN = '1196377367364669442-eqSBqQTi2BdQ1v6wQR7Q7wVWKeLuvv'
OAUTH_TOKEN_SECRET = 'pLz9WhD84icERIYqSfNSXxcrnGzHpeOqSMlvUPLcBKItt'

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