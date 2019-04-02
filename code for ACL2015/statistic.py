#! /usr/bin/env python
#coding=utf-8
from __future__ import division
from document import *
from sentiment import *

posts=readPosts()

print len(posts)

happinessPosts=[]
sadnessPosts=[]
fearPosts=[]
angerPosts=[]
surprisePosts=[]

n=0
n_e=0
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
    
    if count>0:
        flag=0
        if p.happiness in set(['both']):
            flag=1
            happinessPosts.append((0,p))
        if p.sadness in set(['both']):
            flag=1
            sadnessPosts.append((1,p))
        if p.fear in set(['both']):
            flag=1
            fearPosts.append((3,p))
        if p.anger in set(['both']):
            flag=1
            angerPosts.append((2,p))
        if p.surprise in set(['both']):
            flag=1
            surprisePosts.append((4,p))
        
        if flag>0:
            n_e+=1
            
        n+=1

print n_e
print n_e/n

#print len(happinessPosts)/n
#print len(sadnessPosts)/n
#print len(fearPosts)/n
#print len(angerPosts)/n
#print len(surprisePosts)/n

print n

cn={}
en={}
for p in posts:
    for w in p.cn:
        if w not in cn:
            cn[w]=0
        cn[w]+=1
    for w in p.en:
        if w not in en:
            en[w]=0
        en[w]+=1
        
enLexicon=EnSentimentLexicon()
cnLexicon=CnSentimentLexicon()

cn=sorted([(cn[w],w) for w in cn if cnLexicon.getPolarity(w)!=0])
cn.reverse()

en=sorted([(en[w],w) for w in en if enLexicon.getPolarity(w)!=0])
en.reverse()


output=open('cn_words.txt','w')
output.write('\n'.join(['%s\t%s' %(w,count) for count,w in cn]))

output=open('en_words.txt','w')
output.write('\n'.join(['%s\t%s' %(w,count) for count,w in en]))
