#! /usr/bin/env python
#coding=utf-8
from document import *
import random
from classify import *
from combined import sumCombined
from blp_classify import *

#output=open('id_list.txt','w')
#ids=['%s' %i for i in range(20000)]
#random.shuffle(ids)
#output.write('\n'.join(ids))

posts=readPosts()

LEN_OF_TRAIN=int(len(posts)*0.6)

pTrains=getDataFromClassify(posts[:LEN_OF_TRAIN])
pTests=getDataFromClassify(posts[LEN_OF_TRAIN:])

DF(pTrains,pTests)

#classify_en(pTrains,pTests)
#classify_translate_simple(pTrains,pTests)

#sumCombined(pTrains,pTests,[classify_cn,classify_en,classify_sentiment])

blp_sentiment(pTrains,pTests)