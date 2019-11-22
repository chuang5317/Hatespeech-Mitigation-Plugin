import tensorflow as tf
import numpy as np
import os
import pandas as pd
import tensorflow_hub as hub
import tensorflow_datasets as tfds

def get_cnn_davison():
    addr = "./dataset/davison.csv"
    original = pd.read_csv(addr)
    texts = original.iloc[:,6].tolist()
    labels = list(map((lambda x: 1 if x == 1 else 0),  original.iloc[:,5].tolist()))
    train = (texts[:10000], labels[:10000])
    validation = (texts[10000:20000], labels[10000:20000])
    test = (texts[20000:], labels[20000:])
    return (train, validation, test)

(train, validation, test) = get_cnn_davison()
train_data = tf.data.Dataset.from_tensor_slices(train)
test_data = tf.data.Dataset.from_tensor_slices(test)
validation_data = tf.data.Dataset.from_tensor_slices(validation)
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
history = model.fit(train_data.shuffle(10000).batch(512),
                    epochs=20,
                    validation_data=validation_data.batch(512),
                    verbose=1)
results = model.evaluate(test_data.batch(512), verbose=2)

for name, value in zip(model.metrics_names, results):
  print("%s: %.3f" % (name, value))

model.save('cnn.h5') 
