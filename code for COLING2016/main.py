#! /usr/bin/env python
#coding=utf-8
from document import getEmoData,getVocabrary_df,formatK,getDocumentsByLanguage
from svmclassify import svm_classify
from nn import *

trains,tests=getEmoData('anger')
V=getVocabrary_df(trains+tests,k=1000)
trains_cn,tests_cn=getDocumentsByLanguage(trains,'CN'),getDocumentsByLanguage(tests,'CN')
trains_en,tests_en=getDocumentsByLanguage(trains,'EN'),getDocumentsByLanguage(tests,'EN')

trainList=[trains_en,trains_cn,trains]
testList=[tests_en,tests_cn,tests]

#trains=trains_cn
#tests=tests_cn

# SVM
# svm_classify(trains,tests)

# NN
#X_train,y_train=formatK(trains,V)
#X_test,y_test=formatK(tests,V)
#lstm_prediction(X_train,y_train,X_test,y_test,len(V))


# Multi Model


n=3

X_train_list=[]
y_train=[]
X_test_list=[]
y_test=[]

for i in range(n):
    X_train,y_train=formatK(trainList[i],V)
    X_train_list.append(X_train)

    X_test,y_test=formatK(testList[i],V)
    X_test_list.append(X_test)

print(len(X_train_list))

cnn_combined3(X_train_list,y_train,X_test_list,y_test,len(V),n)

