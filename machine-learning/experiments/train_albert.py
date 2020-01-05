import tensorflow as tf
import numpy as np
import os
import pandas as pd
import tensorflow_hub as hub
import tensorflow_datasets as tfds
from datetime import datetime
import run_classifier
import classifier_utils
import tokenization
import optimization
from tensorflow.keras.models import Model
from sklearn.model_selection import train_test_split
import sentencepiece as spm

'''Modified from the tutorial here : https://analyticsindiamag.com/step-by-step-guide-to-implement-multi-class-classification-with-bert-tensorflow/'''
'''There are some minor differences bettweeen bert/albert. Please check their source code if you don't understand anything'''
print("Tensorflow version : " + tf.__version__ + ", requires version : 1.15")

# in davison dataset, 1 is for offensive language and 0 for hatespeech. treating both as hatespeech here
def get_cnn_davison():
    addr = "./dataset/davison.csv"
    train = pd.read_csv(addr)
    # for i in range(len(train)):
      # train.iloc[i, 5] = 0 if train.iloc[i, 5] == 2 else 1
    return train

def get_debug():
  addr =  "./dataset/davison.csv"
  train = pd.read_csv(addr)
  for i in range(len(train)):
    train.iloc[i, 5] = 0 if train.iloc[i, 5] == 2 else 1
  return train


# Set the output directory for saving model file
OUTPUT_DIR = './AlbertModel/'

#@markdown Whether or not to clear/delete the directory and create a new one
DO_DELETE = True #@param {type:"boolean"}

if DO_DELETE:
  try:
    tf.gfile.DeleteRecursively(OUTPUT_DIR)
  except:
    pass

tf.gfile.MakeDirs(OUTPUT_DIR)
print('***** Model output directory: {} *****'.format(OUTPUT_DIR))

train = get_cnn_davison()
(train, val) = train_test_split(train, test_size = 0.25, random_state = 100, train_size = 0.75)
train_InputExamples = train.apply(lambda x: classifier_utils.InputExample(guid=None,
                                                                   text_a = x[6], 
                                                                   text_b = None, 
                                                                   label = x[5]), axis = 1)
val_InputExamples = val.apply(lambda x: classifier_utils.InputExample(guid=None, 
                                                                   text_a = x[6], 
                                                                   text_b = None, 
                                                                   label = x[5]), axis = 1)
print(val_InputExamples)
albert_model = "./modules/albert_base"

def create_tokenizer_from_hub_module():
  """Get the vocab file and casing info from the Hub module."""
  with tf.Graph().as_default():
    tokenization_info = hub.KerasLayer(albert_model, trainable=True, signature='tokens', signature_outputs_as_dict=True)
    vocab_file = "./modules/albert_base/assets/30k-clean.vocab"
    do_lower_case = True
      
  return tokenization.FullTokenizer(
      vocab_file=vocab_file, do_lower_case=do_lower_case, spm_model_file='./modules/albert_xxlarge/assets/30k-clean.model')

tokenizer = create_tokenizer_from_hub_module()

MAX_SEQ_LENGTH = 128

label_list = [0, 1]

task_name = "train_hatespeech"

# Convert our train and val features to InputFeatures that albert understands.
train_features = classifier_utils.convert_examples_to_features(train_InputExamples, label_list, MAX_SEQ_LENGTH, tokenizer, task_name)
val_features = classifier_utils.convert_examples_to_features(val_InputExamples, label_list, MAX_SEQ_LENGTH, tokenizer, task_name)

def create_model(is_predicting, input_ids, input_mask, segment_ids, labels,
                 num_labels):
  
  bert_module = hub.KerasLayer(albert_model, trainable=True, signature='tokens', signature_outputs_as_dict=True)
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
  
def model_fn_builder(num_labels, learning_rate, num_train_steps,
                     num_warmup_steps):
  """Returns `model_fn` closure for TPUEstimator."""
  def model_fn(features, labels, mode, params):  # pylint: disable=unused-argument
    """The `model_fn` for TPUEstimator."""

    input_ids = features["input_ids"]
    input_mask = features["input_mask"]
    segment_ids = features["segment_ids"]
    label_ids = features["label_ids"]

    is_predicting = (mode == tf.estimator.ModeKeys.PREDICT)
    
    # TRAIN and EVAL
    if not is_predicting:

      (loss, predicted_labels, log_probs) = create_model(
        is_predicting, input_ids, input_mask, segment_ids, label_ids, num_labels)

      train_op = optimization.create_optimizer(
          loss, learning_rate, num_train_steps, num_warmup_steps, use_tpu=False)

      # Calculate evaluation metrics. 
      def metric_fn(label_ids, predicted_labels):
        accuracy = tf.metrics.accuracy(label_ids, predicted_labels)
        true_pos = tf.metrics.true_positives(
            label_ids,
            predicted_labels)
        true_neg = tf.metrics.true_negatives(
            label_ids,
            predicted_labels)   
        false_pos = tf.metrics.false_positives(
            label_ids,
            predicted_labels)  
        false_neg = tf.metrics.false_negatives(
            label_ids,
            predicted_labels)
        
        return {
            "eval_accuracy": accuracy,
            "true_positives": true_pos,
            "true_negatives": true_neg,
            "false_positives": false_pos,
            "false_negatives": false_neg
            }

      eval_metrics = metric_fn(label_ids, predicted_labels)

      if mode == tf.estimator.ModeKeys.TRAIN:
        return tf.estimator.EstimatorSpec(mode=mode,
          loss=loss,
          train_op=train_op)
      else:
          return tf.estimator.EstimatorSpec(mode=mode,
            loss=loss,
            eval_metric_ops=eval_metrics)
    else:
      (predicted_labels, log_probs) = create_model(
        is_predicting, input_ids, input_mask, segment_ids, label_ids, num_labels)

      predictions = {
          'probabilities': log_probs,
          'labels': predicted_labels
      }
      return tf.estimator.EstimatorSpec(mode, predictions=predictions)

  # Return the actual model function in the closure
  return model_fn

BATCH_SIZE = 512
LEARNING_RATE = 2e-5
NUM_TRAIN_EPOCHS = 20.0
# Warmup is a period of time where the learning rate is small and gradually increases--usually helps training.
WARMUP_PROPORTION = 0.1
# Model configs
SAVE_CHECKPOINTS_STEPS = 300
SAVE_SUMMARY_STEPS = 100

# Compute train and warmup steps from batch size
num_train_steps = int(len(train_features) / BATCH_SIZE * NUM_TRAIN_EPOCHS)
num_warmup_steps = int(num_train_steps * WARMUP_PROPORTION)

# Specify output directory and number of checkpoint steps to save
run_config = tf.estimator.RunConfig(
    model_dir=OUTPUT_DIR,
    save_summary_steps=SAVE_SUMMARY_STEPS,
    save_checkpoints_steps=SAVE_CHECKPOINTS_STEPS)

#Initializing the model and the estimator
model_fn = model_fn_builder(
  num_labels=len(label_list),
  learning_rate=LEARNING_RATE,
  num_train_steps=num_train_steps,
  num_warmup_steps=num_warmup_steps)

estimator = tf.estimator.Estimator(
  model_fn=model_fn,
  config=run_config,
  params={"batch_size": BATCH_SIZE})


# Create an input function for training. drop_remainder = True for using TPUs.
train_input_fn = classifier_utils.input_fn_builder(
    features=train_features,
    seq_length=MAX_SEQ_LENGTH,
    is_training=True,
    drop_remainder=False)

# Create an input function for validating. drop_remainder = True for using TPUs.
val_input_fn = classifier_utils.input_fn_builder(
    features=val_features,
    seq_length=MAX_SEQ_LENGTH,
    is_training=False,
    drop_remainder=False)

#Training the model
print('Beginning Training!')
current_time = datetime.now()
estimator.train(input_fn=train_input_fn, max_steps=num_train_steps)
print("Training took time ", datetime.now() - current_time)

#Evaluating the model with Validation set
print(estimator.evaluate(input_fn=val_input_fn, steps=None))