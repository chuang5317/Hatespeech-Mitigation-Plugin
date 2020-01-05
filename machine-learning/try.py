import pickle
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import f1_score
import datetime
import ds_logistic as ds

clf = pickle.load(open("./hate_speech_classifier", 'rb'))
count_vec = pickle.load(open("./hate_speech_CountVectorizer", 'rb'))

df_test = ds.get_merge()[1]
print(len(df_test))
print(len(df_test[0]))
print(len(df_test[1]))
y_true = df_test[1]
y_pred = []
a = datetime.datetime.now()
for i in range(len(df_test[0])):
    pred = clf.predict(count_vec.transform([df_test[0][i]]))[0]
    y_pred.append(pred)


print(f1_score(y_true, y_pred, average='macro'))
b = datetime.datetime.now()
c = b - a
print(c.microseconds)