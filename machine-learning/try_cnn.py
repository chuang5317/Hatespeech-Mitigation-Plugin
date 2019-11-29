import dataset as ds
import re
import pandas as pd
from sklearn.metrics import f1_score
import os
import tensorflow as tf
from tensorflow import keras
import tensorflow_hub as hub
import math

embedding = "https://tfhub.dev/google/tf2-preview/nnlm-en-dim128/1"
hub_layer = hub.KerasLayer(embedding, input_shape=[], 
                           dtype=tf.string, trainable=True)
relu = tf.keras.layers.Dense(16, activation='relu')
sigmoid = tf.keras.layers.Dense(1, activation='sigmoid')
model = keras.models.load_model("cnn.h5", custom_objects={'KerasLayer': hub_layer})

model.summary()

score, text = ds.get_trac_test()
y_true = []
y_pred = []

print(len(text))

for i in range(len(text)):
    print(i)
    true = score[i]
    t = text[i]
    pred = model.predict([t])[0][0]
    y_true.append(true)
    y_pred.append(int(round(pred)))

print(y_pred)
print(f1_score(y_true, y_pred, average='macro'))

