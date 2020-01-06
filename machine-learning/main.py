from concurrent.futures import ThreadPoolExecutor
import pickle
from sklearn.feature_extraction.text import CountVectorizer
import spacy
import sys
import json
from flask import Flask, render_template, redirect, url_for,request
from flask import make_response
import ds_logistic as ds
from sklearn.linear_model import LogisticRegression
import random

executor = ThreadPoolExecutor(2)

app = Flask(__name__)

@app.route("/", methods=['POST'])
def home():
    datafromjs = request.get_data(as_text=True)
    ret = json.dumps(detect(datafromjs))
    resp = make_response(ret)
    resp.headers['Content-Type'] = "application/json"
    resp.headers.add('Access-Control-Allow-Origin', '*')
    resp.headers.add("Access-Control-Allow-Methods", "POST, GET, OPTIONS")
    resp.headers.add("Access-Control-Allow-Headers", "*")
    return resp

@app.route("/train", methods=["GET"])
def train_endpoint():
    executor.submit(train)
    resp = make_response("Training has started")
    return resp

def train():
    global clf, count_vec
    print("Training")
    # Training a Classifier
    count_vec_local = CountVectorizer(ngram_range=(0, 1))
    train, test = ds.get_merge() #use get toxic for un merged dataset
    X_train = count_vec_local.fit_transform(train[0])

    # over
    clf_local = LogisticRegression(solver="lbfgs", max_iter=1000)
    clf_local.fit(X=X_train, y=train[1])

    # save the model to disk
    pickle.dump(clf_local, open("./hate_speech_classifier", 'wb'))
    pickle.dump(count_vec_local, open("./hate_speech_CountVectorizer", 'wb'))

    clf = clf_local
    count_vec = count_vec_local
    print("Finished Training")

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
        # print(res)
        if res[0] == 1:
            print(s)
            count = text.find(s.text, count)
            print((count, count + n))
            ret.append((count, count + n))
        count += n
    print(ret)
    return ret

def main():
    print("running")
    app.run(debug = False, host='0.0.0.0', port=8081)

if __name__ == "__main__":
    main()
