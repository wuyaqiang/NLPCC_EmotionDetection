#! /usr/bin/env python
#coding=utf-8
from __future__ import division
import subprocess
import math

malletPath='c:\\mallet\\dist;c:\\mallet\\dist\\mallet.jar;c:\\mallet\\dist\\mallet-deps.jar'

def getlexicon(documents):
    words=[]
    # get the words use in train documents
    for document in documents:
        words+=document.words.keys()
    words=set(words)
    
    # create the (word,id) pairs
    lexicon=dict([(word,i+1) for i,word in enumerate(words)])
    return lexicon
    

def createMEText(documents,lexicon,path):
    lines=[]
    for i,document in enumerate(documents):
        line="%s %d " % (i+1,document.label)
#        if document.polarity==True:
#            line="%s 1 " % (i+1)
#        else:
#            line="%s 0 " % (i+1)
        pairs=[(lexicon[word],document.words[word]) for word in document.words.keys() if word in lexicon]
        line+=' '.join(['%d=%d' %(pair[0],pair[1]) for pair in pairs])
        lines.append(line)
        
    text='\n'.join(lines)
    output=open(path,'w')
    output.write(text)
    output.close()
    
def createResults(tests):
    input=open('result.output','rb')
    results=[]
    acc=0
    
    tp=[0,0,0,0,0]
    realCount=[0,0,0,0,0]
    predCount=[0,0,0,0,0]
    
    for i,line in enumerate(input):
        p=line.split()
        label,prob=p[2].split(':')
        label=int(label)
        #results.append(label)
        if label==tests[i].label:
            acc+=1

        predLabel=label
        realLabel=tests[i].label
        if predLabel==realLabel:
            tp[realLabel]+=1
        predCount[predLabel]+=1
        realCount[realLabel]+=1
            
        # result
        result=[0,0,0,0,0]
        for pp in p[2:]:
            label,prob=pp.split(':')
            label=int(label)
            prob=float(prob)
            result[label]=prob
        results.append(result)
    
    acc=acc/len(tests)
    print 'acc: %f' %(acc)
    
    f=[0,0,0,0,0]
    for i in range(5):
        p=tp[i]/predCount[i]
        r=tp[i]/realCount[i]
        f[i]=2*p*r/(p+r)
    
    print '\t'.join(['%s' %ff for ff in f])
    
    return acc,results
        
def fileToBin(trainFilePath,trainBinPath,testFilePath,testBinPath):
    # train file to binary
    cmd='java -cp %s lltCsv2Vectors --input %s --output  %s' %(malletPath,trainFilePath,trainBinPath)
    retcode=subprocess.Popen(cmd.split())      
    retcode.wait()
    if retcode < 0:
        print 'child is terminated'
    else:
        print 'vector modification successful'
    
    # test file to binary
    cmd='java -cp %s lltCsv2Vectors  --use-pipe-from %s --input %s --output %s' %(malletPath,trainBinPath,testFilePath,testBinPath)
    retcode=subprocess.Popen(cmd.split())      
    retcode.wait()
    if retcode < 0:
        print 'child is terminated'
    else:
        print 'vector modification successful'
    
    

def train(trainBinPath,modelPath):
    cmd='java -Xms1024m -cp %s cc/mallet/classify/tui/Vectors2Classify --input %s --output-classifier  %s --trainer MaxEnt' %(malletPath,trainBinPath,modelPath)
    retcode=subprocess.Popen(cmd.split())      
    retcode.wait()
    if retcode < 0:
        print 'child is terminated'
    else:
        print 'classifier training successful'

    
def classify(modelPath,testBinPath,resultPath):
    cmd='java -cp %s lltClassification --classifier %s --testing-file %s --report test:raw' % (malletPath,modelPath,testBinPath)
    retcode=subprocess.Popen(cmd.split(),stdout=file(resultPath,'w'))
    retcode.wait()
    if retcode < 0:
        print 'testing is terminated'
    else:
        print 'testing successful'
    
    
def me_classify(trains,tests):
    lexicon=getlexicon(trains)
    createMEText(trains,lexicon,'train.txt')
    createMEText(tests,lexicon,'test.txt')
    
    fileToBin('train.txt','train.bin','test.txt','test.bin')
    train('train.bin','train.model')
    classify('train.model','test.bin','result.output')
    
    #根据result.output创建结果集合
    return createResults(tests)
    
