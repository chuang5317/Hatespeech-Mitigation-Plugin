#Labeling functions that could be used by snorkel --  or direcly as detection service
from snorkel.labeling import labeling_function
import re
import preprocessing as pre

# All input parameters for labelling functions are Pandas DataFrame of spacy doc.

# Define the label mappings for convenience
ABSTAIN = 0
POSITIVE = 1
NEGATIVE = 2

# Filtering none hatespeech text
@labeling_function()
def lf_neg_short(df):
    doc = df.at['tokens']
    """Short text tends to be less hateful"""
    return NEGATIVE if len(doc) < 5 else ABSTAIN

# Keywords matching
@labeling_function()
def lf_keyword_strong_swearing(df):
    doc = df.at['tokens']
    strong_swearing = ["cunt", "fuck", "motherfucker", "bastard", "dickhead", "bellend"]
    return POSITIVE if any( word in doc for word in strong_swearing) else ABSTAIN

# Keywords matching
@labeling_function()
def lf_keyword_violence(df):
    doc = df.at['tokens']
    violence = ["beat", "tear", "shoot", "punch", "rape", "assault"]
    return POSITIVE if any( word in doc for word in violence) else ABSTAIN

# More complicated methods
@labeling_function()
def lf_spacy_adj_sexism(df):
    ''' Detects if negative adjectives are apeearing in the same doc with gender nouns'''
    gender_related_words = ["female", "male", "MtF", "FtM", "slut", "bitch", "boy", "girl"] # Add more ...
    if(any (word in df.at['tokens'] for word in gender_related_words)):
        adjs = filter((lambda token: token.pos_ == "ADJ"), df.at['spacy'])
        for a in adjs:
            # print(a.text)
            # print(a.similarity(pre.negative_word))
            if(a.similarity(pre.negative_word) > 0.25):
                return POSITIVE
    return ABSTAIN

@labeling_function()
def lf_spacy_adj_racism(df):
    ''' Detects if negative adjectives are apeearing in the same doc with race nouns'''
    gender_related_words = ["coon", "nigga", "nigger", "paki", "ching chong", "white trash"] # Add more ...
    if(any (word in df.at['tokens'] for word in gender_related_words)):
        adjs = filter((lambda token: token.pos_ == "ADJ"), df.at['spacy'])
        for a in adjs:
            # print(a.text)
            # print(a.similarity(pre.negative_word))
            if(a.similarity(pre.negative_word) > 0.25):
                return POSITIVE
    return ABSTAIN


# Other API result -- TODO : find suitable api and let them be LF as well
