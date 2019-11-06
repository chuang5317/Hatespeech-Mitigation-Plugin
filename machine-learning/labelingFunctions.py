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
    if (df.at['swear_noun']):
        return POSITIVE
    return ABSTAIN

@labeling_function()
def lf_keyword_raicism(df):
    if (df.at['racist_noun']):
        return POSITIVE
    return ABSTAIN

# Keywords matching
@labeling_function()
def lf_keyword_violence(df):
    # violence = ["beat", "tear", "shoot", "punch", "rape", "assault"]
    if(df.at['violence_verb']):
        return POSITIVE
    return ABSTAIN

# More complicated methods
@labeling_function()
def lf_spacy_words_sexism(df):
    ''' Detects if negative adjectives are apeearing in the same doc with gender nouns'''
    if(df.at['gender_noun'] and (df.at['negative_adj'] or df.at['violence_verb'])):
        return POSITIVE
    return ABSTAIN

@labeling_function()
def lf_spacy_words_lgbt(df):
    ''' Detects if negative adjectives are appearing in the same doc with lgbt nouns '''
    if(df.at['lgbt_noun'] and (df.at['negative_adj'] or df.at['violence_verb'])):
        return POSITIVE
    return ABSTAIN

@labeling_function()
def lf_spacy_words_gpe(df):
    ''' Detects if negative adjectives are appearing in the same doc with geographical locations '''
    if(df.at['countries']):
        if(df.at['negative_adj'] or df.at['violence_verb']):
            return POSITIVE
    return ABSTAIN


# Other API result -- TODO : find suitable api and let them be LF as well
