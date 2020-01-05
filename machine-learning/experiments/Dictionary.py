from nltk import tokenize
import boto3


#if one person is describing another person with these words, classify as hatespeech, obtained from facebook
check = ["cunt", "dick", "asshole", "fuck", "bitch", "motherfucker", "suck my dick", "kiss my ass", "eat shit",
         "vomit", "throw up", "vile", "disgusting", "yuck", "ugly", "hideous", "filthy", "dirty", "smelly",
         "dumb", "stupid", "idiot", "illiterate", "uneducated", "retarded", "crazy", "insane",
         "whore", "slut", "perverts", "homophobic", "islamophobic", "racist", "niger", "bent", "gay",
         "terrorist", "nonce", "pedo", "rapist"]


def syntax_analyser(text):
    comprehend = boto3.client(service_name='comprehend', region_name='region')
    comprehend.detect_syntax(Text=text, LanguageCode='en')
    #next need to go through each JSON token, see if its an adj (PartsOfSpeech, TAG), if so check if it (Text) is in the dictionary above

#returns an array of Strings, each a sentence. Takes in a string.
def to_sentence(text):
    return tokenize.sent_tokenize(text)

#returns an array of Strings, each a paragraph. Takes in a string.
def to_paragraph(text):
    return text.split("\n\n")
