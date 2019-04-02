#! /usr/bin/env python
#coding=utf-8
from __future__ import division
from maxent import me_classify
import math

def sumCombined(pTrains,pTests,classifies):
    resultsList=[]
    for classify in classifies:
        resultsList.append(classify(pTrains,pTests)[1])
    trueLabel=[label for label,p in pTests]
    
    Nt=len(pTests)
    Nc=len(classifies)
    Nl=5 # number of labels
    acc=0
    
    tp=[0,0,0,0,0]
    realCount=[0,0,0,0,0]
    predCount=[0,0,0,0,0]
    
    for i in range(Nt):
        mResult=[0,0,0,0,0]
        for j in range(Nc):
            for k in range(Nl):
                mResult[k]+=resultsList[j][i][k]
                #print resultsList[j][i]
        mResult=sorted([(mResult[k],k) for k in range(Nl)])
        predLabel=mResult[-1][1]
        if predLabel==trueLabel[i]:
            acc+=1
        
        realLabel=trueLabel[i]
        if predLabel==realLabel:
            tp[realLabel]+=1
        predCount[predLabel]+=1
        realCount[realLabel]+=1
    
    print 'acc: %f' %(acc/Nt)
    
    f=[0,0,0,0,0]
    for i in range(5):
        p=tp[i]/predCount[i]
        r=tp[i]/realCount[i]
        f[i]=2*p*r/(p+r)
    
    print '\t'.join(['%s' %ff for ff in f])
