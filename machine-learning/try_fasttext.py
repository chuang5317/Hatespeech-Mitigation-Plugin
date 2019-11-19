import dataset as ds
import fasttext
import re
import pandas as pd
from sklearn.metrics import f1_score

model = fasttext.load_model("ft.bin")
dstest = ds.get_davison_test()

# x_test = model.predict("apply this classifier to text & test if the outcome is good")
# x_test1 = model.predict("imperial is such a great university!")
# x_test2 = model.predict("all other universities are not as good as imperial")
# x_test3 = model.predict("african universities are very bad because they are full of african people") 
# x_test4 = model.predict("black people are all very bad and should not be allowed in university") #
# x_test5 = model.predict("fuck niggers and fuck their african countries")#
# x_test6 = model.predict("fags should go to hell")#
# x_test7 = model.predict("We have to kill all the Palestinians unless they are resigned to live here as slaves")#
# x_test8 = model.predict("\"The true Negro does not want integration. ... He realizes his potential is far better among his own race.\" -- Rev. Jerry Falwell")#
# x_test9 = model.predict("The National Organization of Women is actually the “National Organization of Witches.” Rev. Jerry Falwell")
# x_test10 = model.predict("Check your white privileges you cis white male!") 
# x_test11 = model.predict("I hate eating apple pie, its nasty as hell")#
# x_test12 = model.predict("The robotics coursework is hard af I regret taking the course") 
# x_test13 = model.predict("Hello its me!") 
# x_test14 = model.predict("I don't like Alex he is nothing more than an uneducated pig.") #
# x_test15 = model.predict("Scientists say they can recreate living dinosaurs within the next 5 years") 
# x_test16 = model.predict("I can't believe you didn'in Titanic. Do you have any emotion? Have you ever cired?")#

# print(x_test)
# print(x_test1)
# print(x_test2)
# print(x_test3)
# print(x_test4)
# print(x_test5)
# print(x_test6)
# print(x_test7)
# print(x_test8)
# print(x_test9)
# print(x_test10)
# print(x_test11)
# print(x_test12)
# print(x_test13)
# print(x_test14)
# print(x_test15)
# print(x_test16)

# print(dstest)
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
