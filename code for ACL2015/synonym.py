#! /usr/bin/env python
#coding=utf-8

class Synonym:
    def __init__(self):
        self.d=[] # tong yi ci lin
        for line in open(r'resource\tongyicilin.txt','rb'):
            line=line.strip()
            p=line.split('=')
            if len(p)==2:
                words=[w.strip() for w in p[1].split()]
                n=len(words)
                for i in range(n):
                    for j in range(i+1,n):
                        self.d.append((words[i],words[j]))
                        self.d.append((words[j],words[i]))
        self.d=set(self.d)
        
    def isSyn(self,a,b):
        return (a,b) in self.d



