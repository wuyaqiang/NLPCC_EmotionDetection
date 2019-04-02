#! /usr/bin/env python
#coding=utf-8
import numpy as ny
from cedict import CEDict
import os

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

def readPosts():
    posts=[]
    postBegin=False
    post=[]
    d={}
    for fpath in os.listdir('data1'):
        print fpath
        for line in open(r'data1\%s' %fpath,'rb'):
            line=line.strip()
            if len(line)>0:
                if line[:12]=='< Tweet id =':
                    postBegin=True
                    continue
                if line=='< / Tweet >':
                    postBegin=False
                    content=post[7*3+1]
                    happiness=post[2*3+1]
                    sadness=post[3*3+1]
                    anger=post[4*3+1]
                    fear=post[5*3+1]
                    surprise=post[6*3+1]
                    
                    if content not in d:
                        posts.append(Post(content,happiness,sadness,anger,fear,surprise))
                        d[content]=0
                    
                    post=[]
                    continue
                if postBegin:
                    post.append(line)
                
   
    # random the posts
    id_list=[int(line) for line in open(r'id_list.txt','rb')]
    posts=[posts[i] for i in id_list if i<len(posts) and len(posts[i].en)>0]
    print len(posts)
    
    return [p for p in posts if len(p.en)>0]

def overSamples(posts,n):
    m=len(posts)
    return [posts[i%m] for i in range(n)]
        
def getDataFromClassify(posts):
    happinessPosts=[]
    sadnessPosts=[]
    fearPosts=[]
    angerPosts=[]
    surprisePosts=[]
    for p in posts:
        count=0
        if p.happiness!='none':
            count+=1
        if p.sadness!='none':
            count+=1
        if p.fear!='none':
            count+=1
        if p.anger!='none':
            count+=1
        if p.surprise!='none':
            count+=1
        
        if count==1:
            if p.happiness!='none':
                happinessPosts.append((0,p))
            if p.sadness!='none':
                sadnessPosts.append((1,p))
            if p.fear!='none':
                fearPosts.append((3,p))
            if p.anger!='none':
                angerPosts.append((2,p))
            if p.surprise!='none':
                surprisePosts.append((4,p))

    print len(happinessPosts),len(sadnessPosts),len(fearPosts),len(angerPosts),len(surprisePosts)
    
    n=len(angerPosts)
    return happinessPosts[:n]+sadnessPosts[:n]+angerPosts+overSamples(fearPosts,n)+overSamples(surprisePosts,n)

def DF(trains,tests):
    df={}
    for label,p in trains+tests:
        for w in p.words:
            if w not in df:
                df[w]=0
            df[w]+=1

    
    
    for label,p in trains+tests:
        for w in p.words.keys():
            if w in df and df[w]<3:
                del p.words[w]

def getDocumentWordRelations(documents):
    # document-word
    dw={}
    for d in documents:
        for w in d.words:
            if w not in dw:
                dw[w]=len(dw)
    
    m=ny.zeros((len(documents),len(dw)))
    for i in range(len(documents)):
        for w in documents[i].words:
            j=dw[w]
            m[i,j]=1
    
    return m

