# Preprocessing of text. Please visit https://spacy.io/api for more information
import spacy
spacy_nlp = spacy.load("en_core_web_sm") # sm, md, lg
#Trade off : md, lg give more accurate result but sm is significantly faster

# Constants for word similarity comparison
negative_word = spacy_nlp("bad")

def preprocess(text):
    return spacy_nlp(text)