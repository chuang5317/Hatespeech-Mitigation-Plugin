import tensorflow as tf
import numpy as np
import os
import pandas as pd
import tensorflow_hub as hub
import tensorflow_datasets as tfds

print("Tensorflow version : " + tf.__version__ + ", requires version : 2.20")

# This is a single label, binary classification CNN

#Unbalanced ds, too much hatespeech
def get_cnn_davison():
    addr = "./dataset/davison.csv"
    original = pd.read_csv(addr)
    print(len(original))
    texts = original.iloc[:,6].tolist()
    labels = list(map(lambda x : 0 if x == 2 else 1, original.iloc[:,5].tolist()))
    train = (texts[:15000], labels[:15000])
    validation = (texts[15000:20000], labels[15000:20000])
    test = (texts[20000:],  labels[20000:])
    return (train, validation, test)

# A more balanced dataset
(train, validation, test) = ds.get_toxic()
train_data = tf.data.Dataset.from_tensor_slices(train)
test_data = tf.data.Dataset.from_tensor_slices(test)
validation_data = tf.data.Dataset.from_tensor_slices(validation)
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
# overfits after epoch 2 -- val_loss increases and val_accuracy decrease
history = model.fit(train_data.shuffle(10000).batch(512),
                    epochs=2,
                    validation_data=validation_data.batch(512),
                    verbose=1)
results = model.evaluate(test_data.batch(512), verbose=2)

for name, value in zip(model.metrics_names, results):
  print("%s: %.3f" % (name, value))

model.save('cnn.h5') 