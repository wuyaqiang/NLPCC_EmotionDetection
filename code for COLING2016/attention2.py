#! /usr/bin/env python
#coding=utf-8
from __future__ import print_function
from __future__ import division
from functools import reduce
import re
import tarfile
import math

import numpy as np
np.random.seed(1337)  # for reproducibility

from keras.utils.data_utils import get_file
from keras.layers.embeddings import Embedding
from keras.layers.core import Dense, Merge, Dropout, RepeatVector, Activation, Flatten, TimeDistributedDense
from keras.layers import recurrent,Lambda, merge
from keras.models import Sequential
from keras.preprocessing.sequence import pad_sequences
from keras.layers.convolutional import Convolution1D, MaxPooling1D, AveragePooling1D

from keras.engine import Input

from sklearn.metrics import average_precision_score

from seya.layers.recurrent import Bidirectional
from keras.layers.recurrent import LSTM, GRU
from keras.preprocessing import sequence

EMBED_SIZE = 32
HIDDEN_SIZE= 32
MAX_LEN= 100
BATCH_SIZE = 16
EPOCHS = 10

nb_filter = 10
filter_length = 5


def attention2(X_train,y_train,X_test,y_test,vocab_size):
    X_train = sequence.pad_sequences(X_train, maxlen=MAX_LEN)
    X_test = sequence.pad_sequences(X_test, maxlen=MAX_LEN)
       
    print('Build model...')
    
    input_ = Input(shape=(input_length, input_dim))
    lstm = GRU(self.HID_DIM, input_dim=input_dim, input_length = input_length, return_sequences=True)(input_)
    att = TimeDistributed(Dense(1))(lstm)
    att = Flatten()(att)
    att = Activation(activation="softmax")(att)
    att = RepeatVector(self.HID_DIM)(att)
    att = Permute((2,1))(att)
    mer = merge([att, lstm], "mul")
    hid = AveragePooling1D(pool_length=input_length)(mer)
    hid = Flatten()(hid)

attention2([],[],[],[],10)
