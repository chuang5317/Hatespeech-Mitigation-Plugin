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
    return POSITIVE if any(word in doc for word in strong_swearing) else ABSTAIN

# Keywords matching
@labeling_function()
def lf_keyword_violence(df):
    doc = df.at['tokens']
    violence = ["beat", "tear", "shoot", "punch", "rape", "assault"]
    return POSITIVE if any(word in doc for word in violence) else ABSTAIN

# Keywords matching
@labeling_function()
def lf_keyword_suicide(df):
    doc = df.at['tokens']
    suicidal = ["suicide", "kill", "dead", "depressed", "depression", "death"]
    return POSITIVE if any(word in doc for word in suicidal) else ABSTAIN

# Keywords matching
@labeling_function()
def lf_keyword_shaming(df):
    doc = df.at['tokens']
    shaming = ["slut", "whore", "pathetic", "stupid", "retarded", "autistic"]
    return POSITIVE if any(word in doc for word in shaming) else ABSTAIN

# More complicated methods

@labeling_function()
def lf_spacy_adj_threat(df):
    ''' Detects if negative adjectives are apeearing in the same doc with threatening words'''
    threats = ["killer", "murderer", "shooter", "stabber", "victim", "gunman"] # Add more ...
    if(any (word in df.at['tokens'] for word in threats)):
        adjs = filter((lambda token: token.pos_ == "ADJ"), df.at['spacy'])
        for a in adjs:
            if(a.similarity(pre.negative_word) > 0.25):
                return POSITIVE
    return ABSTAIN

@labeling_function()
def lf_spacy_adj_terrorism(df):
    ''' Detects if negative adjectives are apeearing in the same doc with terrorism/war'''
    terror = ["terrorism", "terrorist", "bomber", "war", "taliban", "bombs", "guns"] # Add more ...
    if(any (word in df.at['tokens'] for word in terror)):
        adjs = filter((lambda token: token.pos_ == "ADJ"), df.at['spacy'])
        for a in adjs:
            if(a.similarity(pre.negative_word) > 0.25):
                return POSITIVE
    return ABSTAIN

@labeling_function()
def lf_spacy_adj_terrorism(df):
    ''' Detects if negative adjectives are apeearing in the same doc with insects/unpleasant animals'''
    animals = ["cow", "insect", "vermin", "monkey", "potato", "goldfish"] # Add more ...
    if(any (word in df.at['tokens'] for word in animals)):
        adjs = filter((lambda token: token.pos_ == "ADJ"), df.at['spacy'])
        for a in adjs:
            if(a.similarity(pre.negative_word) > 0.25):
                return POSITIVE
    return ABSTAIN

@labeling_function()
def lf_spacy_adj_politics(df):
    ''' Detects if negative adjectives are apeearing in the same doc with politics'''
    politics = ["party", "conservative", "labour", "right wing", "left wing", "communist", "capitalist"] # Add more ...
    if(any (word in df.at['tokens'] for word in politics)):
        adjs = filter((lambda token: token.pos_ == "ADJ"), df.at['spacy'])
        for a in adjs:
            if(a.similarity(pre.negative_word) > 0.25):
                return POSITIVE
    return ABSTAIN

@labeling_function()
def lf_spacy_adj_sexism(df):
    ''' Detects if negative adjectives are apeearing in the same doc with gender nouns'''
    gender_related_words = ["female", "male", "MtF", "FtM", "slut", "bitch", "hoe", "boy", "girl"] # Add more ...
    if(any (word in df.at['tokens'] for word in gender_related_words)):
        adjs = filter((lambda token: token.pos_ == "ADJ"), df.at['spacy'])
        for a in adjs:
            if(a.similarity(pre.negative_word) > 0.25):
                return POSITIVE
    return ABSTAIN



@labeling_function()
def lf_spacy_adj_racism(df):
    ''' Detects if negative adjectives are apeearing in the same doc with race nouns'''
    race_related_words = ["nigger", "chink"] # Add more ...
    if(any (word in df.at['tokens'] for word in race_related_words)):
        adjs = filter((lambda token: token.pos_ == "ADJ"), df.at['spacy'])
        for a in adjs:
            if(a.similarity(pre.negative_word) > 0.25):
                return POSITIVE
    return ABSTAIN

@labeling_function()
def lf_spacy_adj_gpe(df):
    ''' Detects if negative adjectives are apeearing in the same doc with race nouns'''
    race_related_words = ["nigger", "chink"] # Add more ...
    if(df.at['countries'].length > 0):
        adjs = filter((lambda token: token.pos_ == "ADJ"), df.at['spacy'])
        for a in adjs:
            if(a.similarity(pre.negative_word) > 0.25):
                return POSITIVE
    return ABSTAIN


# Other API result -- TODO : find suitable api and let them be LF as well
