#! /usr/bin/env python
#coding=utf-8
from __future__ import division
from numpy import *
from numpy.linalg import *
from maxent import me_classify
from document import CDocument


# Label Propagation with Bipartite Graph
class BLP:
    def __init__(self,documents):
        # word-vocabulary from label and unlabel documents
        V=[]
        for document in documents:
            V+=document.words.keys()
        V=[word for word in set(V)]
        
        # word--document Associations
        wd=dict([(word,[]) for word in V])
        for i,document in enumerate(documents):
            for word in document.words:
                wd[word].append(i)
                
        # document--document transfer matrix
        self.dd=zeros((len(documents),len(documents)))
        for i,document in enumerate(documents):
            # document--word transfer probability, p(w|d)
            pwd=1/len(document.words)
            for word in document.words:
                # word--document transfer probability, p(d|w)
                pdw=zeros((len(documents)))
                for j in wd[word]:
                    pdw[j]+=1
                pdw=pdw/len(wd[word])*pwd
                self.dd[i]+=pdw
            print i
        
        for i,document in enumerate(documents):
            document.index=i
    
    def createLPArgument(self,label,unlabel):
        # normailize the transfer matrix
        # unlabel--unlabel transfer matrix    
        self.Tuu=zeros((len(unlabel),len(unlabel)),dtype=float32)
        # unlabel--label transfer matrix
        self.Tul=zeros((len(unlabel),len(label)),dtype=float32)
        
        for i,document in enumerate(unlabel):
            index=document.index
            sumJ=sum(self.dd[index,document.index] for document in label+unlabel if document.index!=index)+1
            for j,document in enumerate(label):
                self.Tul[i,j]=self.dd[index,document.index]/sumJ
            for j,document in enumerate(unlabel):
                if i!=j:
                    self.Tuu[i,j]=self.dd[index,document.index]/sumJ
                else:
                    self.Tuu[i,j]=1/sumJ
        
        # Yl & I
        self.Yl=[[0]*len(label),[0]*len(label),[0]*len(label),[0]*len(label),[0]*len(label)]
        for i,document in enumerate(label):
            self.Yl[document.label][i]=1
           
        self.Yl=transpose(self.Yl)
        self.I=diag([1 for i in range(len(unlabel))])


    def LP(self,label,unlabel):
        self.createLPArgument(label,unlabel)
        Yu=dot(dot(inv(self.I-self.Tuu),self.Tul),self.Yl)
        return Yu
    
    def LP_Classify(self,label,tests):
        Yu=self.LP(label,tests)
        
        tUnlabel=[]
        results=[]
        acc=0
        
        tp=[0,0,0,0,0]
        realCount=[0,0,0,0,0]
        predCount=[0,0,0,0,0]
        
        for i,document in enumerate(tests):
            y0=Yu[i,0]/sum([y[0] for y in Yu])
            y1=Yu[i,1]/sum([y[1] for y in Yu])
            y2=Yu[i,2]/sum([y[2] for y in Yu])
            y3=Yu[i,3]/sum([y[3] for y in Yu])
            y4=Yu[i,4]/sum([y[4] for y in Yu])
            result=max([(y0,0),(y1,1),(y2,2),(y3,3),(y4,4)])
            results.append((result[0],result[1],i)) # (score,label,index)
            #document=CDocument(resultLabel,document.words)
            #tUnlabel.append(document)
            if result[1]==document.label:
                acc+=1
            
            predLabel=result[1]  
            realLabel=document.label
            if predLabel==realLabel:
                tp[realLabel]+=1
            predCount[predLabel]+=1
            realCount[realLabel]+=1
            
        f=[0,0,0,0,0]
        for i in range(5):
            p=tp[i]/predCount[i]
            r=tp[i]/realCount[i]
            f[i]=2*p*r/(p+r)
        
        print 'acc: %f' %(acc/len(tests))
        print '\t'.join(['%s' %ff for ff in f])


