import dataset as ds
import labelingFunctions as lf 
from snorkel.labeling import LabelModel, PandasLFApplier
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
import random
import nltk
from nltk.corpus import wordnet as wn
from snorkel.augmentation import transformation_function

# Define the label mappings for convenience
ABSTAIN = 0
POSITIVE = 1
NEGATIVE = 2

df_train = ds.get_debug()

# Define the set of labeling functions (LFs)
lfs = [lf.lf_neg_short, lf.lf_keyword_strong_swearing, lf.lf_keyword_violence,
        lf.lf_spacy_adj_sexism, lf.lf_spacy_adj_racism] # and one more in order to run ...

# Apply the LFs to the unlabeled training data
applier = PandasLFApplier(lfs)
L_train = applier.apply(df_train)

# Train the label model and compute the training labels
# Cardinality was 2. Got : ValueError: L_train has cardinality 3, cardinality=2 passed in.
label_model = LabelModel(cardinality=3, verbose=True)
label_model.fit(L_train, n_epochs=500, log_freq=50, seed=123)
df_train["label"] = label_model.predict(L=L_train, tie_break_policy="abstain")
# Filter out useless data
# df_train = df_train[df_train.label != ABSTAIN]
print("Useful data remaining: " + str(df_train.shape[0]))

# Ignoring Transformation Functions for Data Augmentation for now...
# TODO: create transformation functions for different categories of hatespeech

# Ignoring slicing for now...
# TODO: figure out if we need slicing

# Training a Classifier
docs = df_train.iloc[:,0].tolist() # first column of data frame (first_name)
print(df_train)

train_text = []
for doc in docs:
    # print(doc.text)
    train_text.append(doc.text)
print(train_text)

X_train = CountVectorizer(ngram_range=(1, 2)).fit_transform(train_text)

clf = LogisticRegression(solver="lbfgs")
clf.fit(X=X_train, y=df_train.label.values)

# TODO: apply this classifier to text & test if the outcome is good

print("Done!")