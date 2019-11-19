import pickle
import dataset as ds
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import f1_score

clf = pickle.load(open("./hate_speech_classifier", 'rb'))
count_vec = pickle.load(open("./hate_speech_CountVectorizer", 'rb'))

df_train = ds.get_davison_test()
y_true = []
y_pred = []

for i in range(len(df_train[0])):
    true = df_train[0][i]
    pred = clf.predict(count_vec.transform([df_train[1][i]]))
    y_true.append(true)
    y_pred.append(pred)
    if (true != pred):
        print(df_train[1][i])

print(f1_score(y_true, y_pred, average='macro'))
