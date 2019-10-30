import labelingFunctions as lf 
import preprocessing as pre

# Get hate speech sentences from: https://www.quora.com/What-are-some-examples-of-%E2%80%98hate-speech%E2%80%99-in-the-United-States-2017
# Run this file and see what are the LFs doing
print(lf.lf_neg_short(pre.spacy_nlp("ok")))
print(lf.lf_keyword_strong_swearing(pre.spacy_nlp("fuck you!")))
# print(lf.lf_spacy_adj_sexism(pre.spacy_nlp("you stupid ugly fucking slut i’ll go to your flat and cut your fucking head off you inbred whore.")))
# print(lf.lf_spacy_adj_sexism(pre.spacy_nlp("i can't think of any example")))
