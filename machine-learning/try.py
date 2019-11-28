import pickle
import dataset as ds
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import f1_score

clf = pickle.load(open("./hate_speech_classifier", 'rb'))
count_vec = pickle.load(open("./hate_speech_CountVectorizer", 'rb'))

df_train = ds.get_davison_test()
y_true = []
y_pred = []

##class = class label for majority of CF users. 0 - hate speech 1 - offensive language 2 - neither
for i in range(len(df_train[0])):
    true = df_train[0][i]
    pred = clf.predict(count_vec.transform([df_train[1][i]]))[0]
    y_true.append(2 if true == 2 else 1)
    y_pred.append(pred)
#     if (true != pred):
#         print(df_train[1][i])
# print(y_true)
# print(y_pred)
print(f1_score(y_true, y_pred, average='macro'))
