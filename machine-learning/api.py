import pickle
from sklearn.feature_extraction.text import CountVectorizer
import spacy
import sys
import json
from flask import Flask, render_template, redirect, url_for,request
from flask import make_response
app = Flask(__name__)

@app.route("/", methods=['POST'])
def home():
    if request.method == 'POST':
        datafromjs = request.get_data(as_text=True)
        ret = json.dumps(detect(datafromjs))
        resp = make_response(ret)
        resp.headers['Content-Type'] = "application/json"
        return resp

nlp = spacy.load('en_core_web_sm') 
clf = pickle.load(open("./hate_speech_classifier", 'rb'))
count_vec = pickle.load(open("./hate_speech_CountVectorizer", 'rb'))

def detect(text):
    ret = []
    doc = nlp(text)
    count = 0
    for s in doc.sents:
        n = len(s.text)
        trans = count_vec.transform([s.text])
        res = clf.predict(trans)
        # print(res)
        if res == 1:
            # print(s)
            ret.append((count, count + n))
        count += n
    return ret

def main():
    app.run(debug = True)

if __name__ == "__main__":
    main()
    
#Example usagae:
# print(detect("Today is a sunny day. U son of a bitch. Go to hell."))
# print(detect("Do you have an Nvidia graphics card on your desktop? That’s great until you are in need of the latest drivers especially when you are a gamer. Unlike Windows, Nvidia drivers for Linux desktops are quite hard to come by, and installing the latest drivers on your Linux desktop can be quite an arduous process. Fortunately for Linux users, there are the third party graphics drivers PPA which keeps an updated Nvidia driver for installation."))
# print(detect("The political situation in Bolivia is very sad."))
# print(detect("Damn the indigenous people damaging the city, they should die."))
# print(detect("Actually, they are only fighting for justice"))
# print(detect("People are protesting for their democracy"))
# print(detect("The government is oppresing the wealthy"))
# print(detect("There was a coup against the filthy peasents"))
# print(detect("The military is only trying to help the people"))
# print(detect("Whatever it is, it better stop soon"))