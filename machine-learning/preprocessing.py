# Preprocessing of text. Please visit https://spacy.io/api for more information
import spacy
import pandas as pd

spacy_nlp = spacy.load("en_core_web_md") # sm, md, lg
#Trade off : md, lg give more accurate result but sm is significantly faster

# Constants for word similarity comparison
negative_word = spacy_nlp("bad")

def preprocess(texts):
    spacy = []
    tokens = []
    countries = []
    names = []
    # add more series here later to accelerate the running speed

    for text in texts:
        nlp = spacy_nlp(text)
        spacy.append(nlp)
        thisTokenList = []
        thisCountries = []
        thisNames = []
        for token in nlp:
            thisTokenList.append(token.text)
        for ent in nlp.ents:
            if(ent.label_ == "GPE"):
                thisCountries.append(ent)
            if(ent.label_ == "PERSON"):
                thisNames.append(ent)
        countries.append(thisCountries)
        tokens.append(thisTokenList)
        names.append(thisNames)

    df = pd.DataFrame()
    df['spacy'] = spacy
    df['tokens'] = tokens
    df['names'] = names
    df['countries'] = countries
    return df
