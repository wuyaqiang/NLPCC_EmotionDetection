#! /usr/bin/env python
#coding=utf-8
import re

# Chinese-English Dict

class CEDict:
    def __init__(self):
        self.ec={} # english to chinese
        p=re.compile('^.+? (.+?) \[.+?\] \/(.+?)$')
        
        for line in open(r'resource\cedict_ts.u8','rb'):
            line=line.strip()
            if len(line)>0:
                m=p.findall(line)
                if len(m)==1:
                    cword,e=m[0]
                    for ee in e.split('/'):
                        ee=ee.lower()
                        if len(ee)>0:
                            if ee not in self.ec:
                                self.ec[ee]=[]
                            self.ec[ee].append(cword)
        #print len(self.ec)
        
    def getChinese(self,e):
        if e in self.ec:
            return self.ec[e]
        else:
            return []
    
    def isIn(self,e):
        return e in self.ec
                
                
