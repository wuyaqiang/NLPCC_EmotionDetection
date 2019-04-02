#! /usr/bin/env python
#coding=utf-8
from __future__ import division
from cedict import CEDict
from document import *

FEATURE_WEIGHT=3

def getSentimentFeatures(p,cn_lexicon,en_lexicon):
    features={}
    # basic features
    for w in p.words:
        features[w]=1
    
    score=sum([cn_lexicon.getPolarity(w) for w in p.cn])
    if score>0:
        features['#CN_POS']=FEATURE_WEIGHT
    elif score<0:
        features['#CN_NEG']=FEATURE_WEIGHT
    
    score=sum([en_lexicon.getPolarity(w) for w in p.en])
    if score>0:
        features['#EN_POS']=FEATURE_WEIGHT
    elif score<0:
        features['#EN_NEG']=FEATURE_WEIGHT
        
    return features
    
def getFeaturesSenseAndSentiment(p,dict,pmi,cn_lexicon,en_lexicon):
    features={}
    # basic features
    for w in p.words:
        features[w]=1
    
    # word sense with Chinese and English co-relation
    words=[w.lower() for w in p.content.split()]
    n=len(words)
    for i in range(n):
        w=words[i]
        if dict.isIn(w): # is English word
            twords=dict.getChinese(w) # translate words
            if len(twords)==1: # only have one meaning on the dict
                features['#TRAN_%s' %twords[0]]=1
            else:
                tresults=[(pmi.getCnEnRelation(cword,w),cword) for cword in twords]
                freqWord=max(tresults)
                if freqWord[0]>0:
                    features['#TRAN_%s' %freqWord[1]]=1
    
    # sentiment features
    score=sum([cn_lexicon.getPolarity(w) for w in p.cn])
    if score>0:
        features['#POS']=1
    elif score<0:
        features['#NEG']=1
    
    score=sum([en_lexicon.getPolarity(w) for w in p.en])
    if score>0:
        features['#POS']=1
    elif score<0:
        features['#NEG']=1
    
    return features
