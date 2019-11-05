# Preprocessing of text. Please visit https://spacy.io/api for more information
import spacy
import pandas as pd

spacy_nlp = spacy.load("en_core_web_md") # sm, md, lg
#Trade off : md, lg give more accurate result but sm is significantly faster

# Constants for word similarity comparison
negative_word = spacy_nlp("bad")
violence_word = spacy_nlp("beat")

def preprocess(texts):
    spacy = []
    tokens = []
    countries = []
    names = []
    violence_verb = []
    negative_adj = []
    nouns = []
    # add more series here later to accelerate the running speed
    for text in texts:
        nlp = spacy_nlp(text)
        spacy.append(nlp)
        thisTokenList = []
        thisCountries = []
        thisNames = []
        thisNouns = []
        thisViolenceVerb = False
        thisNegativeAdj = False
        for token in nlp:
            thisTokenList.append(token.text)
        for ent in nlp.ents:
            if(ent.label_ == "GPE"):
                thisCountries.append(ent)
            if(ent.label_ == "PERSON"):
                thisNames.append(ent)
        nouns_ = filter((lambda token: token.pos_ == "NOUN"), nlp)
        for n in nouns_:
            thisNouns.append(n.text)
        adjs_ = filter((lambda token: token.pos_ == "ADJ"), nlp)
        for a in adjs_:
            if(a.similarity(negative_word) > 0.20):
                thisNegativeAdj = True
                break
        verbs_ = filter((lambda token: token.pos_ == "VERB"), nlp)
        for v in verbs_:
            if(v.similarity(violence_word) > 0.20):
                thisViolenceVerb = True
                break
        countries.append(thisCountries)
        tokens.append(thisTokenList)
        names.append(thisNames)
        nouns.append(thisNouns)
        violence_verb.append(thisViolenceVerb)
        negative_adj.append(thisNegativeAdj)

    df = pd.DataFrame()
    df['spacy'] = spacy
    df['tokens'] = tokens
    df['names'] = names
    df['nouns'] = nouns
    df['countries'] = countries
    df['violence_verb'] = violence_verb
    df['negative_adj'] = negative_adj
    return df
