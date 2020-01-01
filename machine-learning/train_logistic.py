import ds_logistic as ds
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
import random
import pickle
# from sklearn import svm
# from sklearn.naive_bayes import GaussianNB

# Training a Classifier
count_vec = CountVectorizer(ngram_range=(0, 1))
train, test = ds.get_merge() #use get toxic for un merged dataset
X_train = count_vec.fit_transform(train[0])

# over
clf = LogisticRegression(solver="lbfgs", max_iter=1000)
clf.fit(X=X_train, y=train[1])


# Support Vector Machines
# clf = svm.SVC(kernel='linear', C = 1.0)
# clf.fit(X=X_train, y=df_train.label.values)

# Naive Bayes Classification
# gnb = GaussianNB()
# gnb.fit(X=X_train, y=df_train.label.values)

# save the model to disk
pickle.dump(clf, open("./hate_speech_classifier", 'wb'))
pickle.dump(count_vec, open("./hate_speech_CountVectorizer", 'wb'))
