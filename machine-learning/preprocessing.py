# Preprocessing of text. Please visit https://spacy.io/api for more information
import spacy
import pandas as pd

spacy_nlp = spacy.load("en_core_web_md") # sm, md, lg
#Trade off : md, lg give more accurate result but sm is significantly faster

# Constants for word similarity comparison
negative_word = spacy_nlp("disgusting")
violence_word = spacy_nlp("beat")
swear_word = spacy_nlp("bellend")
gender_word = spacy_nlp("girl")
racist_word = spacy_nlp("nigger")
lgbt_word = spacy_nlp("homosexual")
shaming_word = spacy_nlp("autistic")
threat_word = spacy_nlp("killer")
terrorism_word = spacy_nlp("terrorist")

def preprocess(texts):
    spacy = []
    tokens = []
    countries = []
    violence = []
    swear = []
    negative = []
    nouns = []
    gender = []
    racist = []
    lgbt = []
    shame = []
    threat = []
    terrorism = []
    # add more series here later to accelerate the running speed
    for text in texts:
        nlp = spacy_nlp(text)
        spacy.append(nlp)
        thisTokenList = []
        thisCountries = []
        thisNouns = []
        thisViolence = False
        thisNegative = False
        thisSwear = False
        thisGender = False
        thisRacist = False
        thisLGBT = False
        thisShame = False
        thisThreat = False
        thisTerrorism = False
        for token in nlp:
            thisTokenList.append(token.text)
        for ent in nlp.ents:
            if(ent.label_ == "GPE"):
                thisCountries.append(ent)
        for n in nlp: 
            if(n.similarity(swear_word) > 0.33):
                thisSwear = True
                break
        for n in nlp: 
            if(n.similarity(gender_word) > 0.33):
                thisGender = True
                break
        for n in nlp: 
            if(n.similarity(racist_word) > 0.33):
                thisRacist = True
                break
        for n in nlp: 
            if(n.similarity(lgbt_word) > 0.33):
                thisLGBT = True
                break
        for n in nlp: 
            if(n.similarity(shaming_word) > 0.33):
                thisShame = True
                break
        for n in nlp: 
            if(n.similarity(threat_word) > 0.33):
                thisThreat = True
                break
        for n in nlp:
            if(n.similarity(terrorism_word) > 0.33):
                thisTerrorism = True
                break
        adjs_ = filter((lambda token: token.pos_ == "ADJ"), nlp)
        for a in adjs_:
            if(a.similarity(negative_word) > 0.33):
                thisNegative = True
                break
        verbs_ = filter((lambda token: token.pos_ == "VERB"), nlp)
        for v in verbs_:
            if(v.similarity(violence_word) > 0.24):
                thisViolence = True
                break
        countries.append(thisCountries)
        tokens.append(thisTokenList)
        violence.append(thisViolence)
        negative.append(thisNegative)
        swear.append(thisSwear)
        gender.append(thisGender)
        racist.append(thisRacist)
        lgbt.append(thisLGBT)
        shame.append(thisShame)
        threat.append(thisThreat)
        terrorism.append(thisTerrorism)

    df = pd.DataFrame()
    df['spacy'] = spacy
    df['tokens'] = tokens
    df['countries'] = countries
    df['violence'] = violence
    df['negative'] = negative
    df['swear'] = swear
    df['gender'] = gender
    df['racist'] = racist
    df['lgbt'] = lgbt
    df['shame'] = shame
    df['threat'] = threat
    df['terrorism'] = terrorism
    return df
