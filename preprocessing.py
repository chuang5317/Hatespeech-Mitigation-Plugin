# Preprocessing of text. Please visit https://spacy.io/api for more information
import spacy
import pandas as pd

spacy_nlp = spacy.load("en_core_web_sm") # sm, md, lg
#Trade off : md, lg give more accurate result but sm is significantly faster

# Constants for word similarity comparison
negative_word = spacy_nlp("bad")

def preprocess(texts):
    spacy = []
    tokens = []
    # add more series here later to accelerate the running speed
    for text in texts:
        nlp = spacy_nlp(text)
        spacy.append(nlp)
        thisTokenList = []
        for token in nlp:
            thisTokenList.append(token.text)
        tokens.append(thisTokenList)
    df = pd.DataFrame()
    df['spacy'] = spacy
    df['tokens'] = tokens
    return df
