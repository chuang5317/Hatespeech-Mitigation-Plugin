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
    if (df.at['swear']):
        return POSITIVE
    return ABSTAIN

@labeling_function()
def lf_keyword_raicism(df):
    if (df.at['racist']):
        return POSITIVE
    return ABSTAIN

@labeling_function()
def lf_keyword_violence(df):
    if(df.at['violence']):
        return POSITIVE
    return ABSTAIN

@labeling_function()
def lf_spacy_words_sexism(df):
    ''' Detects if negative adjectives are apeearing in the same doc with gender nouns'''
    if(df.at['gender'] and (df.at['negative'] or df.at['violence'])):
        return POSITIVE
    return ABSTAIN

@labeling_function()
def lf_spacy_words_lgbt(df):
    ''' Detects if negative adjectives are appearing in the same doc with lgbt nouns '''
    if(df.at['lgbt'] and (df.at['negative'] or df.at['violence'])):
        return POSITIVE
    return ABSTAIN

@labeling_function()
def lf_spacy_words_gpe(df):
    ''' Detects if negative adjectives are appearing in the same doc with geographical locations '''
    if(df.at['countries']):
        if(df.at['negative'] or df.at['violence']):
            return POSITIVE
    return ABSTAIN

# Keywords matching
@labeling_function()
def lf_keyword_shaming(df):
    if (df.at['shame']):
        return POSITIVE
    return ABSTAIN


@labeling_function()
def lf_spacy_threat(df):
    ''' Detects if negative adjectives are appearing in the same doc with threatening words'''
    if(df.at['threat']):
        return POSITIVE
    return ABSTAIN

@labeling_function() #maybe with +ve adj s later?
def lf_spacy_terrorism(df):
    ''' Detects terrorism/war'''
    if(df.at['terrorism']):
        return POSITIVE
    return ABSTAIN

@labeling_function()
def lf_spacy_animals(df):
    ''' Detects if negative adjectives are apeearing in the same doc with insects/unpleasant animals'''
    animals = ["cow", "insect", "vermin", "monkey", "potato", "goldfish"] # Add more ...
    if(any (word in df.at['tokens'] for word in animals)):
        if(df['negative']):
            return POSITIVE
    return ABSTAIN

@labeling_function()
def lf_spacy_politics(df):
    ''' Detects if negative adjectives are apeearing in the same doc with politics'''
    politics = ["party", "conservative", "labour", "right wing", "left wing", "communist", "capitalist"] # Add more ...
    if(any (word in df.at['tokens'] for word in politics)):
        if(df['negative']):
            return POSITIVE
    return ABSTAIN

# Other API result -- TODO : find suitable api and let them be LF as well
