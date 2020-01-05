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

nlp = spacy.load('en_core_web_md') 
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
        if res[0] == 1:
            # print(s)
            count = text.find(s.text, count) #spacy skips spaces and returns
            ret.append((count, count + n))
        count += n
    return ret

def main():
    app.run(debug = True)

if __name__ == "__main__":
    main()