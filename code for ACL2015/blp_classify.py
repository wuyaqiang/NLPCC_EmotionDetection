#! /usr/bin/env python
#coding=utf-8
from __future__ import division
from maxent import me_classify
from document import CDocument
from cedict import CEDict 
from translate_features import *
from synonym import Synonym
from languagemodel import LanguageModel
from pmi import PMI
from sentiment_features import *
from sentiment import CnSentimentLexicon,EnSentimentLexicon
from blp import BLP

def blp_all(pTrains,pTests):
    trains=[CDocument(label,p.words) for label,p in pTrains]    
    tests=[CDocument(label,p.words) for label,p in pTests]
#    for d in trains+tests:
#        d.words['SMOOTH']=1
    
    blp=BLP(trains+tests)
    blp.LP_Classify(trains,tests)
    
def blp_cn(pTrains,pTests):
    trains=[CDocument(label,p.cn) for label,p in pTrains]    
    tests=[CDocument(label,p.cn) for label,p in pTests]
    for d in trains+tests:
        d.words['SMOOTH']=1
    
    blp=BLP(trains+tests)
    blp.LP_Classify(trains,tests)

def blp_en(pTrains,pTests):
    trains=[CDocument(label,p.en) for label,p in pTrains]    
    tests=[CDocument(label,p.en) for label,p in pTests]
    for d in trains+tests:
        d.words['SMOOTH']=1
    
    blp=BLP(trains+tests)
    blp.LP_Classify(trains,tests)


def blp_translate_simple(pTrains,pTests):
    dict=CEDict()
    
    trains=[]
    tests=[]
    
    for label,p in pTrains:
        words=getTranlateFeatures(p,dict)
        trains.append(CDocument(label,words))
    for label,p in pTests:
        words=getTranlateFeatures(p,dict)
        tests.append(CDocument(label,words))
        
    blp=BLP(trains+tests)
    blp.LP_Classify(trains,tests)

def blp_translate_cerelation(pTrains,pTests):
    dict=CEDict()
    pmi=PMI()
    
    trains=[]
    tests=[]
    
    for label,p in pTrains:
        words=getTranlateFeaturesCERelation(p,dict,pmi)
        trains.append(CDocument(label,words))
    for label,p in pTests:
        words=getTranlateFeaturesCERelation(p,dict,pmi)
        tests.append(CDocument(label,words))
    
#    for d in trains+tests:
#        d.words['SMOOTH']=1
    
    
    blp=BLP(trains+tests)
    blp.LP_Classify(trains,tests)
    

def blp_translate_pmi(pTrains,pTests):
    dict=CEDict()
    syn=Synonym()
    pmi=PMI()
    
    trains=[]
    tests=[]
    
    for label,p in pTrains:
        words= getTranlateFeaturesPMI(p,dict,pmi)
        trains.append(CDocument(label,words))
    for label,p in pTests:
        words= getTranlateFeaturesPMI(p,dict,pmi)
        tests.append(CDocument(label,words))
    
    blp=BLP(trains+tests)
    blp.LP_Classify(trains,tests)
    
def blp_sentiment(pTrains,pTests):
    cn_lexicon=CnSentimentLexicon()
    en_lexicon=EnSentimentLexicon()
    
    trains=[]
    tests=[]
    
    for label,p in pTrains:
        words=getSentimentFeatures(p,cn_lexicon,en_lexicon)
        trains.append(CDocument(label,words))
    for label,p in pTests:
        words=getSentimentFeatures(p,cn_lexicon,en_lexicon)
        tests.append(CDocument(label,words))
    
    blp=BLP(trains+tests)
    blp.LP_Classify(trains,tests)
    
def blp_sense_sentiment(pTrains,pTests):
    dict=CEDict()
    pmi=PMI()
    
    cn_lexicon=CnSentimentLexicon()
    en_lexicon=EnSentimentLexicon()
    
    trains=[]
    tests=[]
    
    for label,p in pTrains:
        words=getFeaturesSenseAndSentiment(p,dict,pmi,cn_lexicon,en_lexicon)
        trains.append(CDocument(label,words))
    for label,p in pTests:
        words=getFeaturesSenseAndSentiment(p,dict,pmi,cn_lexicon,en_lexicon)
        tests.append(CDocument(label,words))
    
    blp=BLP(trains+tests)
    blp.LP_Classify(trains,tests)

def blp_translate_syn(pTrains,pTests):
    dict=CEDict()
    syn=Synonym()
    
    trains=[]
    tests=[]
    
    for label,p in pTrains:
        words=getTranlateFeaturesBySyn(p,dict,syn)
        trains.append(CDocument(label,words))
    for label,p in pTests:
        words=getTranlateFeaturesBySyn(p,dict,syn)
        tests.append(CDocument(label,words))
    
    blp=BLP(trains+tests)
    blp.LP_Classify(trains,tests)
    

def blp_translate_lm(pTrains,pTests):
    dict=CEDict()
    syn=Synonym()
    lm=LanguageModel()
    
    trains=[]
    tests=[]
    
    for label,p in pTrains:
        words=getTranslateFeaturesByLM(p,dict,lm)
        trains.append(CDocument(label,words))
    for label,p in pTests:
        words=getTranslateFeaturesByLM(p,dict,lm)
        tests.append(CDocument(label,words))
    
    blp=BLP(trains+tests)
    blp.LP_Classify(trains,tests)
    
