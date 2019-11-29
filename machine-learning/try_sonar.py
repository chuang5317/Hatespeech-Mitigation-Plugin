from hatesonar import Sonar
import dataset as ds
from sklearn.metrics import f1_score

sonar = Sonar()
x = sonar.ping(text="At least I'm not a nigger")
print(x['text'])

df_train = ds.get_trac_test()
y_true = []
y_pred = []

for i in range(len(df_train[0])):
    predicted = sonar.ping(df_train[1][i])
    p = 0
    if predicted['top_class'] == 'hate_speech':
        p = 1
    elif predicted['top_class'] == 'offensive_language':
        p = 1
    y_pred.append(p)

    true = df_train[0][i]
    t = 0
    if true == 'OAG':
        t = 1
    elif true == 'CAG':
        t = 1
    y_true.append(t)

print(f1_score(y_true, y_pred, average='macro'))



