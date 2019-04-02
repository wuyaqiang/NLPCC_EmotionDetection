#! /usr/bin/env python
#coding=utf-8
from __future__ import division
import numpy as ny
from cedict import CEDict
import os
import random

dict=CEDict() # init Chinese-English Dict

class CDocument:
    def __init__(self,label,words):
        self.label=label
        self.words=words

class Post:
    def __init__(self,content,happiness,sadness,anger,fear,surprise):
        self.content=content
        self.happiness=happiness.lower()
        self.sadness=sadness.lower()
        self.anger=anger.lower()
        self.fear=fear.lower()
        self.surprise=surprise.lower()
        
        self.words={}
        self.en={}
        self.cn={}
        for w in content.split():
            w=w.lower()
            self.words[w]=1
            if isASCII(w): 
                if isRealEnglishWord(w):
                    self.en[w]=1
            else: # Chinese
                self.cn[w]=1

def isRealEnglishWord(word):
    cwords=dict.getChinese(word)
    return len(cwords)>0
            
def isASCII(word):
    flag=True
    for c in word:
        if ord(c)>128:
            flag=False
            break
    return flag

def dfCN(documents):
    df={}
    for d in documents:
        for w in d.cn:
            if w not in df:
                df[w]=0
            df[w]+=1
    for d in documents:
        for w in d.cn.keys():
            if df[w]<10:
                del d.cn[w]

def readPosts():
    posts=[]
    postBegin=False
    post=[]
    d={}
    
    for fpath in os.listdir(r'../data'):
        for line in open(r'../data/%s' %fpath,'rb'):
            line=line.strip()
            if len(line)>0:
                if line[:10]=='<Tweet id=':
                    postBegin=True
                    continue
                if line=='</Tweet>':
                    postBegin=False
                    content=post[5*3+1]
                    happiness=post[0*3+1].lower()
                    sadness=post[1*3+1].lower()
                    anger=post[2*3+1].lower()
                    fear=post[3*3+1].lower()
                    surprise=post[4*3+1].lower()
                    
                    if content not in d:
                        posts.append(Post(content,happiness,sadness,anger,fear,surprise))
                        d[content]=0
                    
                    post=[]
                    continue
                if postBegin:
                    post.append(line)
                
   
    # random the posts
    id_list=[int(line) for line in open(r'./resource/id_list.txt','rb')]
    posts=[posts[i] for i in id_list if i<len(posts) and len(posts[i].en)>0]
    print len(posts)
    
    for i in range(len(posts)):
        posts[i].id=i
    
    dfCN(posts)
    
    return posts
