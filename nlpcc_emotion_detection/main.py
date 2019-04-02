from __future__ import print_function

from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.utils import to_categorical
import numpy as np

from nn import lstmModel,bilstmModel
from stopwords import afterStopwords
from pre_processing import readPosts
from pre_word2vec import preWordEmbedding

MAX_NUM_WORDS = 40
MAX_SEQUENCE_LENGTH = 40
NUM_OF_DEV_DATA = 728

all_texts = []
all_labels = []

all_posts = readPosts()


for post in all_posts:
    # sentence = afterStopwords(post.content)     # Remove the stop words.
    # all_texts.append(sentence)
    all_texts.append(post.content)
    all_labels.append(post.label)


print('Found %s Train Post !' % len(all_texts))
print('Found %s Train Label !' % len(all_labels))

tokenizer = Tokenizer()
# tokenizer = Tokenizer(num_words=MAX_NUM_WORDS)
tokenizer.fit_on_texts(all_texts)
sequences = tokenizer.texts_to_sequences(all_texts)


word_index = tokenizer.word_index
print('Found %s unique tokens.' % len(word_index))


data = pad_sequences(sequences, maxlen=MAX_SEQUENCE_LENGTH)


labels = np.asarray(all_labels)
# labels = to_categorical(np.asarray(all_labels))

print('Shape of data tensor:', data.shape)
print('Shape of label tensor:', labels.shape)

x_train = data[ : -NUM_OF_DEV_DATA]
y_train = labels[ : -NUM_OF_DEV_DATA]
x_dev = data[ -NUM_OF_DEV_DATA : ]
y_dev = labels[ -NUM_OF_DEV_DATA : ]

print('x_train.shape: ',x_train.shape)
print('y_train.shape: ',y_train.shape)


matrix = preWordEmbedding(word_index)


lstmModel(x_train=x_train, y_train=y_train, x_test=x_dev, y_test=y_dev, vocab_size=len(word_index),pre_embedding=matrix)






















