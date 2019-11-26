import dataset as ds
import labelingFunctions as lf
from snorkel.labeling import LabelModel, PandasLFApplier
import fasttext
import random
import nltk
from nltk.corpus import wordnet as wn
from snorkel.augmentation import transformation_function
import pickle
import pandas as pd

# Define the label mappings for convenience
ABSTAIN = 0
POSITIVE = 1
NEGATIVE = 2


df_train = ds.get_davison() #out performed combined dataset

# Define the set of labeling functions (LFs)
lfs = [lf.lf_keyword_strong_swearing, lf.lf_keyword_violence,
        lf.lf_spacy_words_sexism, lf.lf_keyword_raicism, lf.lf_spacy_words_gpe,
        lf.lf_keyword_shaming,  lf.lf_spacy_threat, lf.lf_spacy_terrorism,
        lf.lf_neg_nonehumansubject]
# Unused ones :
# lf.lf_spacy_animals, lf.lf_spacy_politics,  # giving false positives

# Apply the LFs to the unlabeled training data
applier = PandasLFApplier(lfs)
L_train = applier.apply(df_train)

# Train the label model and compute the training labels
# Cardinality was 2. Got : ValueError: L_train has cardinality 3, cardinality=2 passed in.
label_model = LabelModel(cardinality=3, verbose=True)
label_model.fit(L_train, n_epochs=500, log_freq=50, seed=123)
df_train["label"] = label_model.predict(L=L_train, tie_break_policy="abstain")

# Filter out useless data
df_train = df_train[df_train.label != ABSTAIN]
print("Useful data remaining: " + str(df_train.shape[0]))

# Ignoring Transformation Functions for Data Augmentation for now...
# TODO: create transformation functions for different categories of hatespeech

# Ignoring slicing, don't think we need it

# Training a Classifier
docs = df_train.iloc[:,0].tolist() # first column of data frame (first_name)

train_text = []
train_label = []
for doc in docs:
    train_text.append(doc.text)
for i in range(df_train.shape[0]):
    train_label.append("__label__" + str(df_train.iloc[i]['label']))

nintypercent = (int)(df_train.shape[0] * 0.9)

#output to .train file for fast text
ftrain = pd.DataFrame()
ftrain[0] = train_label
ftrain[1] = train_text
ftrain.to_csv('ft.train', index = None, header = False, sep=' ')

model = fasttext.train_supervised(input="ft.train", lr=1.0, epoch=25, wordNgrams=2)
model.save_model("ft.bin")