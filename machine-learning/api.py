import pickle
from sklearn.feature_extraction.text import CountVectorizer
import spacy
import sys
import json
from flask import Flask, render_template, redirect, url_for,request, jsonify
from flask import make_response
app = Flask(__name__)

@app.route("/", methods=['POST'])
def home():
    if request.method == 'POST':
        data = request.json
        nodes = data["nodes"]

        # Expect a list of [{"id": <int>, "text": <str>}]
        results = []
        for node in nodes:
            # "hatespeech" value to be replaced by NLP engine's decision
            res = {"id": node["id"], "hatespeech": "true" if detect(node["text"]) else "false"}
            results.append(res)
        return jsonify({"result": results})

nlp = spacy.load('en_core_web_sm') 
clf = pickle.load(open("./hate_speech_classifier", 'rb'))
count_vec = pickle.load(open("./hate_speech_CountVectorizer", 'rb'))

def detect(text):
    trans = count_vec.transform([text])
    res = clf.predict(trans)[0] == 1
    return res

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