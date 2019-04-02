#! /usr/bin/env python
#coding=utf-8
from __future__ import division
from cedict import CEDict
from document import *
from dump import Dump
from languagemodel import LanguageModel

# just for BLP
#def getTranlateFeatures(p,dict,syn):
#    features={}
#    # basic features
#    for w in p.words:
#        features[w]=1
#    
#    # translate features
#    words=[w.lower() for w in p.content.split()]
#    n=len(words)
#    for i in range(n):
#        w=words[i]
#        if dict.isIn(w): # is English word
#            twords=dict.getChinese(w) # translate words
#            if len(twords)==1: # only have one meaning on the dict
##                features['#TRAN_%s' %twords[0]]=1
#                features['%s' %twords[0]]=1
#            else: # more than one meaning, need to disambiguate
#                l_cn=''
#                r_cn=''
#                scores=[[tw,0] for tw in twords]
#                # Left
#                for j in range(i-1,0,-1):
#                    if isASCII(words[j])==False: # Chinese word
#                        #l_cn=words[j]
#                        for k in range(len(twords)):
#                            if syn.isSyn(twords[k],words[j]):
#                                scores[k][1]+=1
#                # Right
#                for j in range(i+1,n):
#                    if isASCII(words[j])==False: # Chinese word
#                        #r_cn=words[j]
#                        for k in range(len(twords)):
#                            if syn.isSyn(twords[k],words[j]):
#                                scores[k][1]+=1
#                
#                for k in range(len(twords)):
#                    if scores[k][1]>0:   
##                        features['#TRAN_%s' %twords[k]]=1
#                        features['%s' %twords[k]]=1
#                    
#                
#    return features

dump=Dump()
def getTranslateFeaturesByLM(p,dict,lm):
    features={}
    # basic features
    for w in p.words:
        features[w]=1
        
    pmiFreqWords=getPMIFrequencyWords()
    # translate features
    words=[w.lower() for w in p.content.split()]
    n=len(words)
    for i in range(n):
        w=words[i]
        if dict.isIn(w): # is English word
            twords=dict.getChinese(w) # translate words
            if len(twords)==1:
                features['#TRAN_%s' %twords[0]]=1
            else:
                tresults=[]
                if i>0:
                    preWord=words[i-1]
                    tresults+=[(lm.getProb(preWord,tword),tword) for tword in twords if lm.getProb(preWord,tword)>0]
                if i<n-1:
                    postWord=words[i+1]
                    tresults+=[(lm.getProb(tword,postWord),tword) for tword in twords if lm.getProb(tword,postWord)>0]
                    if len(tresults)>0:
                        freqTWord=max(tresults)[1]
                        dump.writeline(freqTWord)
                        features['#TRAN_%s' %freqTWord]=1
                
    return features


def getPMIFrequencyWords():
    # init PMI frequency list
    pmiFreqWords={}
    for line in open(r'resource\single_word_hits_BING.txt','rb'):
        line=line.strip()
        if len(line)>0:
            p=line.split('\t')
            if len(p)==2:
                pmiFreqWords[p[0].strip()]=int(p[1])
    return pmiFreqWords

#dump=Dump()
def getTranslateFeaturesByFrequency(p,dict):
    features={}
    # basic features
    for w in p.words:
        features[w]=1
        
    pmiFreqWords=getPMIFrequencyWords()
    # translate features
    words=[w.lower() for w in p.content.split()]
    n=len(words)
    for i in range(n):
        w=words[i]
        if dict.isIn(w): # is English word
            twords=dict.getChinese(w) # translate words
            if len(twords)==1:
                features['#TRAN_%s' %twords[0]]=1
            else:
                tresults=[(pmiFreqWords[tword],tword) for tword in twords if tword in pmiFreqWords]
                if len(tresults)>0:
                    freqTWord=max(tresults)[1]
#                    dump.writeline(w+' '+freqTWord)
                    features['#TRAN_%s' %freqTWord]=1
    return features

def getTranlateFeatures(p,dict):
    features={}
    # basic features
    for w in p.words:
        features[w]=1
    
    # translate features
    words=[w.lower() for w in p.content.split()]
    n=len(words)
    for i in range(n):
        w=words[i]
        if dict.isIn(w): # is English word
            twords=dict.getChinese(w) # translate words
            if len(twords)==1: # only have one meaning on the dict
                features['#TRAN_%s' %twords[0]]=1
        
    return features

def getTranlateFeaturesBySyn(p,dict,syn):
    features={}
    # basic features
    for w in p.words:
        features[w]=1
    
    # translate features
    words=[w.lower() for w in p.content.split()]
    n=len(words)
    for i in range(n):
        w=words[i]
        if dict.isIn(w): # is English word
            twords=dict.getChinese(w) # translate words
            if len(twords)==1: # only have one meaning on the dict
                features['#TRAN_%s' %twords[0]]=1
            else: # more than one meaning, need to disambiguate
                l_cn=''
                r_cn=''
                scores=[[tw,0] for tw in twords]
                # Left
                for j in range(i-1,0,-1):
                    if isASCII(words[j])==False: # Chinese word
                        #l_cn=words[j]
                        for k in range(len(twords)):
                            if syn.isSyn(twords[k],words[j]):
                                scores[k][1]+=1
                # Right
                for j in range(i+1,n):
                    if isASCII(words[j])==False: # Chinese word
                        #r_cn=words[j]
                        for k in range(len(twords)):
                            if syn.isSyn(twords[k],words[j]):
                                scores[k][1]+=1

                        
#                for tword in twords:
#                    if syn.isSyn(tword,l_cn) or syn.isSyn(tword,r_cn):
#                        output.write('%s\t%s\n' %(w,tword))
                
                for k in range(len(twords)):
                    if scores[k][1]>0:
                        #output.write('%s\t%s\n' %(w,twords[k]))   
                        features['#TRAN_%s' %twords[k]]=1
#                maxTWord=max([(score,tw) for tw,score in scores])
#                if maxTWord[0]>0:
#                    output.write('%s\t%s\n' %(w,maxTWord[1]))   
#                    features['#TRAN_%s' %maxTWord[1]]=1
                    
                
    return features
    

def getTranlatePairs(p,dict,syn):
    pairs=[]
    # translate features
    words=[w.lower() for w in p.content.split()]
    n=len(words)
    for i in range(n):
        w=words[i]
        if dict.isIn(w): # is English word
            twords=dict.getChinese(w) # translate words
            if len(twords)>1: # more than one meaning, need to disambiguate
                l_cn=''
                r_cn=''
                scores=[[tw,0] for tw in twords]
                # Left
                for j in range(i-1,0,-1):
                    if isASCII(words[j])==False and words[j] not in set(['！','。','，','：','…','（','）','《','》','；']): # Chinese words
                        l_cn=words[j]
                        break
                # Right
                for j in range(i+1,n):
                    if isASCII(words[j])==False and words[j] not in set(['！','。','，','：','…','（','）','《','》','；']): # Chinese word
                       r_cn=words[j]
                if l_cn!='' or r_cn!='':
                    for tword in twords:
                        pairs.append((l_cn,r_cn,tword,w))
                        
    return pairs

    
## get English-Chinese pair
#ecpairs={}
#dict=CEDict()
#for p in posts:
#    words=[w.lower() for w in p.content.split()]
#    n=len(words)
#    for i in range(n):
#        w=words[i]
#        if dict.isIn(w): # English word
#            if i-1>=0:
#                l0=words[i-1]
#            else:
#                l0=''
#            if i-2>=0:
#                l1=words[i-2]
#            else:
#                l1=''
#            
#            if i+1<n:
#                r0=words[i+1]
#            else:
#                r0=''
#            if i+2<n:
#                r1=words[i+2]
#            else:
#                r1=''
#            pair=(l1,l0,w,r0,r1)
##            ecpairs[pair]=0
#            ecpairs[pair]=0
#                
#print len(ecpairs)
#
#output=open('dump.txt','w')
#for pair in ecpairs:
#    output.write('%s\t%s\t $$$ %s $$$ \t%s\t%s\n' %pair)
#            
#            
#

#dict=CEDict()
#syn=Synonym()
#
#pairs=[]
#for p in posts:
#    pairs+=getTranlatePairs(p,dict,syn)
#    
#output=open('EN_CN_Pairs.txt','w')
#for pair in set(pairs):
#    output.write('%s $$$ %s $$$ %s $$$ %s\n' %pair)
#