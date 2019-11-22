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
# print(reloaded_model.get_config())
model.summary()
def get_cnn_davison():
    addr = "./dataset/davison.csv"
    original = pd.read_csv(addr)
    texts = original.iloc[:,6].tolist()
    labels = list(map((lambda x: 1 if x == 1 else 0),  original.iloc[:,5].tolist()))
    train = (texts[:10000], labels[:10000])
    validation = (texts[10000:20000], labels[10000:20000])
    test = (texts[20000:], labels[20000:])
    return (train, validation, test)

_,_,test = get_cnn_davison()
y_true = []
y_pred = []

print(len(test[0]))

for i in range(len(test[0])):
    print(i)
    true = test[1][i]
    t = test[0][i]
    pred = model.predict([t])[0][0]
    y_true.append(true)
    y_pred.append(int(round(pred)))
#     if (true != pred):
#         print(test[0][i])

print(y_pred)
print(f1_score(y_true, y_pred, average='macro'))

