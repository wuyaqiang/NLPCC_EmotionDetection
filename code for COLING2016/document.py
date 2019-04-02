#! /usr/bin/env python
#coding=utf-8
from post import readPosts,isRealEnglishWord,isASCII
from sentiment import EnSentimentLexicon

class Document:
    # Three Attributes: polarity, words, label
    def __init__(self,polarity,words):
        self.polarity=polarity
        self.words=words
        if polarity==True:
            self.label=1
        else:
            self.label=0

def getVocabrary(documents):
    V={}
    for d in documents:
        for w in d.words:
            if w not in V:
                V[w]=len(V)
    return V

def getVocabrary_df(documents,k=100):
    # DF
    df={}
    for d in documents:                     # 得到documents中每个word的词数，以字典形式存储，如：{‘word1’:3，‘word2’:5，‘word3’:22}
        for w in d.words:
            if w not in df:
                df[w]=0
            df[w]+=1

    df=sorted([(df[w],w) for w in df])      # 将df字典以词频排序，然后变成list，形式如：[(2,'word1'),(5,'word2'),(22,'word3')]
    df.reverse()                            # 将上面一步得到的list逆序，即变成从大到小：[(22,'word3'),(5,'word2'),(2,'word1')]
    df=[w for count,w in df]                # 得到按词频排序的词表：['word3', 'word2', 'word1']

    enLexicon=EnSentimentLexicon()

    # feature selection
    V={}
    for i,w in enumerate(df):
        if i<(k*0.75): # make sure the feature space contain some English words
            V[w]=len(V)
#        elif len(V)<k and (isRealEnglishWord(w) or isASCII(w)):
        elif len(V)<k and enLexicon.getPolarity(w)!=0: # English sentimental word
            V[w]=len(V)
    print ('length of V:',len(V))

    for d in documents:
        for w in d.words.keys():
            if w not in V:
                del d.words[w]

    return V

def getLabel(postLanguage):
    if postLanguage=='f':
        return 0
    else:
        return 1
    
def getVector(post,emotion):
    # emotion
    label=0
    if emotion=='happiness':
        label=getLabel(post.happiness)
    if emotion=='sadness':
        label=getLabel(post.sadness)
    if emotion=='fear':
        label=getLabel(post.fear)
    if emotion=='anger':
        label=getLabel(post.anger)
    if emotion=='surprise':
        label=getLabel(post.surprise)
    
    if label>0:
        return Document(True,post.words)
    else:
        return Document(False,post.words)

def getVectors(posts,emotion):      # 返回的是一个Document对象的列表
    pos=[]
    neg=[]
    for p in posts:
        v=getVector(p,emotion)      # v 是一个document对象
        if v.label>0:
            pos.append(v)
        else:
            neg.append(v)
    print ('-- %s --' %emotion)
    print (len(pos),len(neg))

    lenV=min([len(pos),len(neg),200]) # too many samples
    return neg[:lenV]+pos[:lenV]

# get code-switching emotion data 
def getEmoData(emotion):
    posts=readPosts()
    print 'lenght of posts: %d' %(len(posts))
    LEN_OF_TRAIN=int(len(posts)*0.5)
    pTrains=posts[:LEN_OF_TRAIN]
    pTests=posts[LEN_OF_TRAIN:]

    trains=getVectors(pTrains,emotion)      # Document对象的列表
    tests=getVectors(pTests,emotion)        # Document对象的列表

    documents=trains+tests
    #DF(documents)
    trains=[d for d in trains if len(d.words)>0]
    tests=[d for d in tests if len(d.words)>0]
    documents=trains+tests
    
    #V=getVocabrary(documents)
    
    return trains,tests

def getDocumentsByLanguage(documents,language='cn'):
    newDocuments=[]
    for d in documents:
        words={}
        for w in d.words:
            if language=='EN' and isRealEnglishWord(w):
                words[w]=1
            if language=='CN' and isRealEnglishWord(w)==False:
                words[w]=1
        newDocuments.append(Document(d.polarity,words))
    return newDocuments

def formatK(data,V):
    X=[]
    Y=[]
    
    for i,d in enumerate(data):
        x=[]
        for w in d.words:
            x.append(V[w])
        X.append(x)
        Y.append(d.label)
    return X,Y


