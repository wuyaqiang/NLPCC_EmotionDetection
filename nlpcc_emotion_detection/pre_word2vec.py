from gensim.models import  Word2Vec
import logging
import gensim
import os
import numpy as np


EMBEDDING_DIM = 100
# MAX_NUM_WORDS = 50

def preWordEmbedding(word_index):

    embeddings_index = {}

    with open('/home/wuyaqiang/myprojects/Corpus/glove.6B/glove.6B.100d.txt') as f:
    # with open('./resource/sougou100.txt') as f:
        for line in f:
            values = line.split()
            word = values[0]
            word_vec = np.asarray(values[1:], dtype='float32')
            embeddings_index[word] = word_vec


    num_words = len(word_index)

    embedding_matrix = np.random.randn(num_words, EMBEDDING_DIM)

    for word, i in word_index.items():
        # if i >= MAX_NUM_WORDS:
        #     continue
        embedding_vector = embeddings_index.get(word)
        if embedding_vector is not None:
            # words not found in embedding index will be all-zeros.
            embedding_matrix[i-1] = embedding_vector

    return embedding_matrix