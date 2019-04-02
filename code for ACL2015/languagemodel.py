#! /usr/bin/env python
#coding=utf-8
from __future__ import division

class LanguageModel:
    def __init__(self):
        self.m={}
        self.m0={}
        count=0
        for line in open(r'G:\wangzq\PolyU\Code-Switching\Emotion_CS_Analysis\comments.lm.seg.txt'):
            words=[w.lower() for w in line.split()]
            n=len(words)
            for i in range(n):
                if i<n-1:
                    j=i+1
                    # bigram
                    if words[i] not in self.m:
                        self.m[words[i]]={}
                    if words[j] not in self.m[words[i]]:
                        self.m[words[i]][words[j]]=0
                    self.m[words[i]][words[j]]+=1
                
                # unigram
                if words[i] not in self.m0:
                    self.m0[words[i]]=0
                self.m0[words[i]]+=1
                count+=1
                
        for word0 in self.m0:
            self.m0[word0]/=count
            
        for word0 in self.m:
            sumNum=sum(self.m[word0].values())
            for word1 in self.m[word0]:
                self.m[word0][word1]/=sumNum
        
    def getProb(self,word0,word1):
        if word0 in self.m and word1 in self.m[word0]:
            return self.m[word0][word1]*self.m0[word1]
        else:
            return 0
                
#lm=LanguageModel()