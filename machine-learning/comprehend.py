import os, boto3

NEGATIVE_SENTIMENT_THRESHOLD = os.getenv('NEGATIVE_SENTIMENT_THRESHOLD', 0.6)

#if one person is describing another person with these words, classify as hatespeech, obtained from facebook
check = ["cunt", "dick", "asshole", "fuck", "bitch", "motherfucker", "suck my dick", "kiss my ass", "eat shit",
         "vomit", "throw up", "vile", "disgusting", "yuck", "ugly", "hideous", "filthy", "dirty", "smelly",
         "dumb", "stupid", "idiot", "illiterate", "uneducated", "retarded", "crazy", "insane",
         "whore", "slut", "perverts", "homophobic", "islamophobic", "racist", "nigger", "bent", "gay",
         "terrorist", "nonce", "pedo", "rapist", "blacks"]
         
def analyse(text):
    comprehend = boto3.client(service_name='comprehend')
    sentiment = comprehend.detect_sentiment(Text=text, LanguageCode='en')
    result = False
    
    if (sentiment["SentimentScore"]["Negative"] > NEGATIVE_SENTIMENT_THRESHOLD):
        #result = comprehend.detect_syntax(Text=text, LanguageCode='en')
        result = any(word in text.lower() for word in check)
    #next need to go through each JSON token, see if its an adj (PartsOfSpeech, TAG), if so check if it (Text) is in the dictionary above
    return {"hatespeech": result, "sentiment": sentiment["SentimentScore"]}

def lambda_handler(event, context):
    return analyse(event["input"])
