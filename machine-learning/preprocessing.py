# Preprocessing of text. Please visit https://spacy.io/api for more information
import spacy
import pandas as pd

spacy_nlp = spacy.load("en_core_web_md") # sm, md, lg
#Trade off : md, lg give more accurate result but sm is significantly faster

# Constants for word similarity comparison
negative_word = spacy_nlp("bad")
violence_word = spacy_nlp("beat")
swear_word = spacy_nlp("bellend")
gender_word = spacy_nlp("girl")
racist_word = spacy_nlp("nigger")
lgbt_word = spacy_nlp("homosexual")

def preprocess(texts):
    spacy = []
    tokens = []
    countries = []
    names = []
    violence_verb = []
    swear_noun = []
    negative_adj = []
    nouns = []
    gender_noun = []
    racist_noun = []
    lgbt_noun = []
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
        thisSwearNoun = False
        thisGenderNoun = False
        thisRacistNoun = False
        thisLGBTNoun = False
        for token in nlp:
            thisTokenList.append(token.text)
        for ent in nlp.ents:
            if(ent.label_ == "GPE"):
                thisCountries.append(ent)
            if(ent.label_ == "PERSON"):
                thisNames.append(ent)
        for n in nlp: 
            if(n.similarity(swear_word) > 0.35):
                thisSwearNoun = True
                break
        for n in nlp: 
            if(n.similarity(gender_word) > 0.35):
                thisGenderNoun = True
                break
        for n in nlp: 
            if(n.similarity(racist_word) > 0.35):
                thisRacistNoun = True
                break
        for n in nlp: 
            if(n.similarity(lgbt_word) > 0.35):
                thisLGBTNoun = True
                break
        adjs_ = filter((lambda token: token.pos_ == "ADJ"), nlp)
        for a in adjs_:
            if(a.similarity(negative_word) > 0.24):
                thisNegativeAdj = True
                break
        verbs_ = filter((lambda token: token.pos_ == "VERB"), nlp)
        for v in verbs_:
            if(v.similarity(violence_word) > 0.24):
                thisViolenceVerb = True
                break
        countries.append(thisCountries)
        tokens.append(thisTokenList)
        names.append(thisNames)
        violence_verb.append(thisViolenceVerb)
        negative_adj.append(thisNegativeAdj)
        swear_noun.append(thisSwearNoun)
        gender_noun.append(thisGenderNoun)
        racist_noun.append(thisRacistNoun)
        lgbt_noun.append(thisLGBTNoun)

    df = pd.DataFrame()
    df['spacy'] = spacy
    df['tokens'] = tokens
    df['names'] = names
    df['countries'] = countries
    df['violence_verb'] = violence_verb
    df['negative_adj'] = negative_adj
    df['swear_noun'] = swear_noun
    df['gender_noun'] = gender_noun
    df['racist_noun'] = racist_noun
    df['lgbt_noun'] = lgbt_noun
    return df
