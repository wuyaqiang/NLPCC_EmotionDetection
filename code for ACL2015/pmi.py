#! /usr/bin/env python
#coding=utf-8
from __future__ import division

class PMI:
    def __init__(self):
        # Chinese-English Relations
        self.cn_en_relation={}
        for line in open(r'resource\en_cn_relation_BING.txt','rb'):
            p=line.split('\t')
            if len(p)==2:
                pp=p[0].split('_')
                if len(pp)==2:
                    cn,en=pp
                    self.cn_en_relation[(cn,en)]=int(p[1])
        print len(self.cn_en_relation)
        
        # hits of single words
        self.words={}
        for line in open(r'resource\single_word_hits_BING.txt','rb'):
            p=line.split('\t')
            if len(p)==2:
                w,count=p
                self.words[w]=int(count)
        
        # context co-relation
        self.context={}
        for line in open(r'resource\context_BING.txt','rb'):
            p=line.split('\t')
            if len(p)==2:
                pp=p[0].split('_')
                if len(pp)==2:
                    w0,w1=pp
                    score=int(p[1])
                    self.context[(w0,w1)]=score
                    self.context[(w1,w0)]=score
                    
    def getContextRelation(self,w0,w1):
        if (w0,w1) in self.context:
            return self.context[(w0,w1)]
        else:
            return 0
        
    
    def getCnEnRelation(self,cn,en):
#        if (cn,en) in self.cn_en_relation:
#            return self.cn_en_relation[(cn,en)]
#        else:
#            return 0
        
        if (cn,en) in self.cn_en_relation and cn in self.words and en in self.words:
            # PMI
            a=self.cn_en_relation[(cn,en)]
            b=self.words[cn]
            c=self.words[en]
            return a/(b*c)
        else:
            return 0
                        
