from __future__ import absolute_import, division, print_function, unicode_literals
import pickle
import spacy
import sys
import json
import bert
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
embedding = "./modules/static"
embedding_layer = hub.KerasLayer(embedding, input_shape=[], dtype=tf.string, trainable=True)
model = tf.keras.Sequential()
model.add(embedding_layer)
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
        # print("sentence is " + s.text)
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