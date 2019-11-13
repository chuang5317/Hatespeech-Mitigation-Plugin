import pickle
from sklearn.feature_extraction.text import CountVectorizer
import spacy
nlp = spacy.load('en_core_web_sm') 
clf = pickle.load(open("./hate_speech_classifier", 'rb'))
count_vec = pickle.load(open("./hate_speech_CountVectorizer", 'rb'))

def detect(text):
    ret = []
    doc = nlp(text)
    for s in doc.sents:
        trans = count_vec.transform([s.text])
        res = clf.predict(trans)
        print(res)
        if res == 1:
            print(s)
            ret.append((s.start, s.end))
    return ret
#Example usagae:
print(detect("Today is a sunny day. U son of a bitch. Go to hell."))
print(detect("Do you have an Nvidia graphics card on your desktop? That’s great until you are in need of the latest drivers especially when you are a gamer. Unlike Windows, Nvidia drivers for Linux desktops are quite hard to come by, and installing the latest drivers on your Linux desktop can be quite an arduous process. Fortunately for Linux users, there are the third party graphics drivers PPA which keeps an updated Nvidia driver for installation."))