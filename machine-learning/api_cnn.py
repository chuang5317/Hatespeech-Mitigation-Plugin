import pickle
from sklearn.feature_extraction.text import CountVectorizer
import spacy
import sys
import json
import tensorflow as tf
import tensorflow_hub as hub
import tensorflow_datasets as tfds
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
embedding = "https://tfhub.dev/google/tf2-preview/nnlm-en-dim128/1"
hub_layer = hub.KerasLayer(embedding, input_shape=[], 
                           dtype=tf.string, trainable=True)
model = tf.keras.Sequential()
model.add(hub_layer)
model.add(tf.keras.layers.Dense(16, activation='relu'))
model.add(tf.keras.layers.Dense(1, activation='sigmoid'))
model.summary()
model.compile(optimizer='adam',
              loss='binary_crossentropy',
              metrics=['accuracy'])


def detect(text):
    ret = []
    doc = nlp(text)
    count = 0
    # print("paragraph is " + text)
    for s in doc.sents:
        n = len(s.text)
        # print("sentence is" + s.text)
        r = model.predict([s.text])
        # print("r is " + str(r))
        res = r[0][0]
        # print("res is " + str(res))
        if res >= 0.7: #threshold
            ret.append((count, count + n))
            # print("ishatespeech")
        count += n
    print(ret)
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