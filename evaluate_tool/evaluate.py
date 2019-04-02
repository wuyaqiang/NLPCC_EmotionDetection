#-------------------------------------------------------------------------------
# Name:        Evaluation for NLPCC-2018 ShareTask, Code-switching prediction
# Purpose:     evaluate the results of code-switching prediction
#
# Author:      zhongqing
#
# Created:     13/02/2018
# Copyright:   (c) zhongqing 2018
# Licence:     <your licence>
#-------------------------------------------------------------------------------
from __future__ import division
from sys import argv

class Post:
    def __init__(self,content,happiness,sadness,anger,fear,surprise):
        self.content=content
        self.emotions={}
        self.emotions['happiness']=happiness=='T'
        self.emotions['sadness']=sadness=='T'
        self.emotions['anger']=anger=='T'
        self.emotions['fear']=fear=='T'
        self.emotions['surprise']=surprise=='T'


def read_posts(fpath):
    posts=[]
    postBegin=False
    post=[]
    d={}
    #print fpath
    for line in open(fpath,'rb'):
        line=line.strip()
        if len(line)>0:
            if line[:10]=='<Tweet id=':
                postBegin=True
                continue
            if line=='</Tweet>':
                postBegin=False
                content=post[5*3+1]
                happiness=post[1]
                sadness=post[1*3+1]
                anger=post[2*3+1]
                fear=post[3*3+1]
                surprise=post[4*3+1]

                if content not in d:
                    posts.append(Post(content,happiness,sadness,anger,fear,surprise))
                    d[content]=0

                post=[]
                continue
            if postBegin:
                post.append(line)
    #print 'length of posts',len(posts)
    return posts

def eval_one_emotion(golds,results,emotion):
    n=len(golds)
    tp=0
    np=0
    pp=0
    for i in range(n):
        if golds[i].emotions[emotion]==True:
            np+=1
            if results[i].emotions[emotion]==True:
                tp+=1
        if results[i].emotions[emotion]==True:
            pp+=1

    p=tp/pp
    r=tp/np
    f1=2*p*r/(p+r)

    print '[%s]\tP:%f\tR:%f\tF1:%f' %(emotion,p,r,f1)

def main():
    if len(argv)==2:
        # check format
        result_path=argv[1]
        results=read_posts(result_path)
        print 'Format check is passed.'
    elif len(argv)==3:
        # evaluate
        gold_path=argv[1]
        result_path=argv[2]
        
        golds=read_posts(gold_path)
        results=read_posts(result_path)
    
        if len(golds)!=len(results):
            print 'the length of results is different from gold data'
            print 'USEAGE: evaluate.py [gold_path] [result_path]'
            return
    
        eval_one_emotion(golds,results,'happiness')
        eval_one_emotion(golds,results,'sadness')
        eval_one_emotion(golds,results,'anger')
        eval_one_emotion(golds,results,'fear')
        eval_one_emotion(golds,results,'surprise')
        
    else:
        print 'wrong number of arguments'
        print 'USEAGE: '
        print 'Evaluate: \t evaluate.py [gold_path] [result_path]'
        print 'Check Format: \t evaluate.py [result_path]'
    
    

if __name__ == '__main__':
    main()
