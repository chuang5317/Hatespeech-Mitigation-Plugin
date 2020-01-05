import dataset as ds
import re
import pandas as pd
from sklearn.metrics import f1_score
import os
import tensorflow as tf
from tensorflow import keras
import tensorflow_hub as hub
import math
import datetime

# predicts the accuracy and time on the Davison dataset
embedding = "./modules/static"
embedding_layer = hub.KerasLayer(embedding, input_shape=[], dtype=tf.string, trainable=True)
relu = tf.keras.layers.Dense(16, activation='relu')
sigmoid = tf.keras.layers.Dense(1, activation='sigmoid')
model = keras.models.load_model("cnn.h5", custom_objects={'KerasLayer': embedding_layer})

model.summary()
a = datetime.datetime.now()

df_train = ds.get_toxic()[2]
size = len(df_train[0])
half = int(round(size/2)) 
print(half)
y_true = df_train[1][0: half]
y_pred = []

for i in range(half):
    print(i)
    pred = 1 if model.predict([df_train[0][i]])[0] >= 0.5 else 0
    y_pred.append(pred)

# Only testing half of the test set as testing them at once gives sig kill
# for i in range(half, size):
#     print(i)
#     pred = 1 if model.predict([df_train[0][i]])[0] >= 0.5 else 0
#     y_pred.append(pred)

print(f1_score(y_true, y_pred, average='macro'))

b = datetime.datetime.now()
c = b - a
print(c.microseconds)

