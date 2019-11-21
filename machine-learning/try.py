import pickle
import dataset as ds
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import f1_score

clf = pickle.load(open("./hate_speech_classifier", 'rb'))
count_vec = pickle.load(open("./hate_speech_CountVectorizer", 'rb'))

def davision_f1score():

    df_train = ds.get_davison_test()
    y_true = []
    y_pred = []

    for i in range(len(df_train[0])):
        y_true.append(df_train[0][i])
        y_pred.append(clf.predict(count_vec.transform([df_train[1][i]])))

    print(f1_score(y_true, y_pred, average='macro'))


def impermium_f1score():
    df_train = ds.get_imperium_test()
    y_true = []
    y_pred = []

    for i in range(len(df_train[0])):
        case = 0
        if (clf.predict(count_vec.transform([df_train[1][i]])) == 1):
            case = 1

        y_true.append(df_train[0][i])
        y_pred.append(case)

    print(f1_score(y_true, y_pred, average='macro'))

def trac_f1score():
    df_train = ds.get_trac_test()
    y_true = []
    y_pred = []

    for i in range(len(df_train[0])):
        p_case = 0
        if (clf.predict(count_vec.transform([df_train[1][i]])) == 1):
            p_case = 1

        t_case = 0
        if (df_train[0][i] == 'OAG' or df_train[0][i] == 'CAG'):
            t_case = 1

        y_true.append(t_case)
        y_pred.append(p_case)

    print(f1_score(y_true, y_pred, average='macro'))

trac_f1score()


