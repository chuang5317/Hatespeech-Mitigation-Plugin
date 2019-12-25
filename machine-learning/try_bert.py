import tensorflow as tf
import numpy as np
import os
import pandas as pd
import tensorflow_hub as hub
import tensorflow_datasets as tfds
from datetime import datetime
import bert
from bert import run_classifier
from bert import tokenization
from bert import optimization
from tensorflow.keras.models import Model
from sklearn.model_selection import train_test_split
import sentencepiece as spm
from tensorflow.contrib import predictor
from pathlib import Path
import tensorflow.compat.v1 as tf_compat

OUTPUT_DIR = './BertModel'
bert_embedding = "./modules/bert"
def create_tokenizer_from_hub_module():
  """Get the vocab file and casing info from the Hub module."""
  with tf.Graph().as_default():
    tokenization_info = hub.KerasLayer(bert_embedding, trainable=True, signature='tokens', signature_outputs_as_dict=True)
    vocab_file = './modules/bert/assets/vocab.txt'
    do_lower_case = False
      
  return bert.tokenization.FullTokenizer(
      vocab_file=vocab_file, do_lower_case=do_lower_case)

tokenizer = create_tokenizer_from_hub_module()

MAX_SEQ_LENGTH = 128
BATCH_SIZE = 256
label_list = [0, 1, 2]
is_predicting = True
num_labels = len(label_list)

def create_model(is_predicting, input_ids, input_mask, segment_ids, labels,
                 num_labels):
  
  bert_module = hub.KerasLayer(bert_embedding, trainable=True, signature='tokens', signature_outputs_as_dict=True)
  bert_inputs = dict(
      input_ids=input_ids,
      input_mask=input_mask,
      segment_ids=segment_ids)
  bert_outputs = bert_module(inputs=bert_inputs)

  # Use "pooled_output" for classification tasks on an entire sentence.
  # Use "sequence_outputs" for token-level output.
  output_layer = bert_outputs["pooled_output"]

  hidden_size = output_layer.shape[-1].value

  # Create our own layer to tune for politeness data.
  output_weights = tf.get_variable(
      "output_weights", [num_labels, hidden_size],
      initializer=tf.truncated_normal_initializer(stddev=0.02))

  output_bias = tf.get_variable(
      "output_bias", [num_labels], initializer=tf.zeros_initializer())

  with tf.variable_scope("loss"):

    # Dropout helps prevent overfitting
    output_layer = tf.nn.dropout(output_layer, keep_prob=0.9)

    logits = tf.matmul(output_layer, output_weights, transpose_b=True)
    logits = tf.nn.bias_add(logits, output_bias)
    log_probs = tf.nn.log_softmax(logits, axis=-1)

    # Convert labels into one-hot encoding
    one_hot_labels = tf.one_hot(labels, depth=num_labels, dtype=tf.float32)

    predicted_labels = tf.squeeze(tf.argmax(log_probs, axis=-1, output_type=tf.int32))
    # If we're predicting, we want predicted labels and the probabiltiies.
    if is_predicting:
      return (predicted_labels, log_probs)

    # If we're train/eval, compute loss between predicted and actual label
    per_example_loss = -tf.reduce_sum(one_hot_labels * log_probs, axis=-1)
    loss = tf.reduce_mean(per_example_loss)
    return (loss, predicted_labels, log_probs)

"""Returns `model_fn` closure for TPUEstimator."""
def model_fn(features, labels, mode, params):  # pylint: disable=unused-argument
  """The `model_fn` for TPUEstimator."""

  input_ids = features["input_ids"]
  input_mask = features["input_mask"]
  segment_ids = features["segment_ids"]
  label_ids = features["label_ids"]
  (predicted_labels, log_probs) = create_model(
    is_predicting, input_ids, input_mask, segment_ids, label_ids, num_labels)
  predictions = {
      'probabilities': log_probs,
      'labels': predicted_labels
  }
  return tf.estimator.EstimatorSpec(mode, predictions=predictions)


tf.keras.backend.clear_session()
estimator = tf.estimator.Estimator(model_fn, 'OUTPUT_DIR', params={"batch_size": BATCH_SIZE})

# A method to get predictions
def getPrediction(in_sentences):

  labels = ["Hatespeech", "Offensive Language", "Neither"]

  #Transforming the test data into BERT accepted form
  input_examples = [run_classifier.InputExample(guid="", text_a = x, text_b = None, label = 0) for x in in_sentences] 
  
  #Creating input features for Test data
  input_features = run_classifier.convert_examples_to_features(input_examples, label_list, MAX_SEQ_LENGTH, tokenizer)

  #Predicting the classes 
  predict_input_fn = run_classifier.input_fn_builder(features=input_features, seq_length=MAX_SEQ_LENGTH, is_training=False, drop_remainder=False)
  predictions = estimator.predict(predict_input_fn, yield_single_examples=False)
  return [(sentence, prediction['probabilities'], prediction['labels'], labels[prediction['labels']]) for sentence, prediction in zip(in_sentences, predictions)]

print(getPrediction(["Sentence here"]))