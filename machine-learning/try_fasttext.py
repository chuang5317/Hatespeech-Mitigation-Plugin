import dataset as ds
import fasttext
import re
import pandas as pd
from sklearn.metrics import f1_score

model = fasttext.load_model('ft.bin')
dstest = ds.get_davison_test()

ftrain = pd.DataFrame()
ftrain[0] = list(map(lambda a : "__label__" + str(a),  dstest[0]))
ftrain[1] = dstest[1]
ftrain.to_csv('ft.test', index = None, header = False, sep=' ')
print(model.test("ft.test"))

y_true = []
y_pred = []

for i in range(len(dstest[0])):
    true = dstest[0][i]
    pred = int(model.predict([dstest[1][i].replace('\n','')])[0][0][0][-1:])
    y_true.append(true)
    y_pred.append(pred)
    if (true != pred):
        print(dstest[1][i])

print(f1_score(y_true, y_pred, average='macro'))
