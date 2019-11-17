import pickle
from sklearn.feature_extraction.text import CountVectorizer

clf = pickle.load(open("./hate_speech_classifier", 'rb'))
count_vec = pickle.load(open("./hate_speech_CountVectorizer", 'rb'))


x_test = count_vec.transform(["apply this classifier to text & test if the outcome is good"])
x_test1 = count_vec.transform(["imperial is such a great university!"])
x_test2 = count_vec.transform(["all other universities are not as good as imperial"])
x_test3 = count_vec.transform(["african universities are very bad because they are full of african people"]) 
x_test4 = count_vec.transform(["black people are all very bad and should not be allowed in university"]) #
x_test5 = count_vec.transform(["fuck niggers and fuck their african countries"])#
x_test6 = count_vec.transform(["fags should go to hell"])#
x_test7 = count_vec.transform(["We have to kill all the Palestinians unless they are resigned to live here as slaves"])#
x_test8 = count_vec.transform(["\"The true Negro does not want integration. ... He realizes his potential is far better among his own race.\" -- Rev. Jerry Falwell"])#
x_test9 = count_vec.transform(["The National Organization of Women is actually the “National Organization of Witches.” Rev. Jerry Falwell"])
x_test10 = count_vec.transform(["Check your white privileges you cis white male!"]) 
x_test11 = count_vec.transform(["I hate eating apple pie, its nasty as hell"])#
x_test12 = count_vec.transform(["The robotics coursework is hard af I regret taking the course"]) 
x_test13 = count_vec.transform(["Hello its me!"]) 
x_test14 = count_vec.transform(["I don't like Alex he is nothing more than an uneducated pig."]) #
x_test15 = count_vec.transform(["Scientists say they can recreate living dinosaurs within the next 5 years"]) 
x_test16 = count_vec.transform(["I can't believe you didn'in Titanic. Do you have any emotion? Have you ever cired?"])#

print(clf.predict(x_test))
print(clf.predict(x_test1))
print(clf.predict(x_test2))
print(clf.predict(x_test3))
print(clf.predict(x_test4))
print(clf.predict(x_test5))
print(clf.predict(x_test6))
print(clf.predict(x_test7))
print(clf.predict(x_test8))
print(clf.predict(x_test9))
print(clf.predict(x_test10))
print(clf.predict(x_test11))
print(clf.predict(x_test12))
print(clf.predict(x_test13))
print(clf.predict(x_test14))
print(clf.predict(x_test15))
print(clf.predict(x_test16))