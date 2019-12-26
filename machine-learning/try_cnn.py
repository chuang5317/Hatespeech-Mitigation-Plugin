import dataset as ds
import re
import pandas as pd
from sklearn.metrics import f1_score
import os
import tensorflow as tf
from tensorflow import keras
import tensorflow_hub as hub
import math

embedding = "./modules/static"
embedding_layer = hub.KerasLayer(embedding, input_shape=[], dtype=tf.string, trainable=True)
relu = tf.keras.layers.Dense(16, activation='relu')
sigmoid = tf.keras.layers.Dense(1, activation='sigmoid')
model = keras.models.load_model("cnn.h5", custom_objects={'KerasLayer': embedding_layer})

model.summary()
print(model.predict(["Any other results?"])) 
#CNN is not working, predicts everything as 0.9+ to get low loss and high accuracy!!

