import ds_logistic as ds
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn import svm
import random
import pickle
from sklearn import preprocessing

# Training a Classifier
count_vec = CountVectorizer(ngram_range=(0, 1))
train, test = ds.get_merge() #use get toxic for un merged dataset
X_train = count_vec.fit_transform(train[0])
X_train = preprocessing.scale(X_train, with_mean=False)

# Support Vector Machines
# clf = svm.SVC(kernel='linear', C = 1.0)
# clf.fit(X=X_train, y=train[1])

# over
clf = LogisticRegression(solver="lbfgs", max_iter=1000)
clf.fit(X=X_train, y=train[1])

# Gaussian
# clf = MultinomialNB()
# clf.fit(X=X_train, y=train[1])

# save the model to disk
pickle.dump(clf, open("./hate_speech_classifier", 'wb'))
pickle.dump(count_vec, open("./hate_speech_CountVectorizer", 'wb'))
