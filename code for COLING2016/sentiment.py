#! /usr/bin/env python
#coding=utf-8

class EnSentimentLexicon:
    def __init__(self):
        self.lexicon={}
        
        input=open(r'./resource/sentiment.txt','rb')
        for line in input:
            pieces=line.split()
            type=pieces[0][5:]
            word=pieces[2][6:]
            polarity=pieces[5][14:]
            pos=pieces[3][5:]
            stem=pieces[4][9:]
            worded=wording=None
            if pos=='verb' and stem=='y':
                if word[-1]=='e':
                    worded=word+'d'
                    wording=word[:-1]+'ing'
                    words=word+'s'
                elif word[-1]=='y':
                    worded=word[:-1]+'ied'
                    wording=word+'ing'
                    words=word[:-1]+'ies'
                else:
                    worded=word+'ed'
                    wording=word+'ing'
                    if word[-1]!='s':
                        words=word+'s'
                    else:
                        words=word+'es'
            value=1
            if polarity=='positive':
                value=1
            elif polarity=='negative':
                value=-1
            if polarity!='neutral':
                if type=='strongsubj':value*=2
                self.lexicon[word]=value
                if worded!=None and wording!=None:
                    self.lexicon[worded]=value
                    self.lexicon[wording]=value
                    self.lexicon[words]=value
        
        # combine emotion lexicon
        eLexicon=self.readEmotionLexicon()
        for word in eLexicon:
            if word in self.lexicon:
                if self.lexicon[word]*eLexicon[word]<0:
                    del self.lexicon[word]
            else:
                self.lexicon[word]=eLexicon[word]
    
    def getPolarity(self,word):
        if word not in self.lexicon:
            return 0
        else:
            return self.lexicon[word]
        
    def readEmotionLexicon(self):
        eLexicon={}
        for line in open(r'./resource/new-english-emotion-lexicon.txt','rb'):
            line=line.strip()
            word,p=line.split('\t')
            if p=='P':
                eLexicon[word]=1
            else:
                eLexicon[word]=-1
        return eLexicon


class CnSentimentLexicon:
    def __init__(self):
        self.lexicon={}
        for line in open(r'./resource/new-chinese-emotion-lexicon-dutir.txt','rb'):
            p=line.split('\t')
            if len(p)==2:
                if p[1]=='P':
                    self.lexicon[p[0]]=1
                else:
                    self.lexicon[p[0]]=1
                    
    def getPolarity(self,word):
        if word not in self.lexicon:
            return 0
        else:
            return self.lexicon[word]
