from __future__ import print_function

import math
from keras import Input
from keras.layers import Embedding,Dense,Dropout,Bidirectional
from keras.layers.recurrent import LSTM
from keras.models import Model
from keras.optimizers import Adam

EMBEDDING_DIM = 100
HIDDEN_SIZE = 16
BATCH_SIZE =16
MAX_SEQUENCE_LENGTH = 40


def lstmModel(x_train, y_train, x_test, y_test, vocab_size, pre_embedding):


    embedding_layer = Embedding(vocab_size,
                                EMBEDDING_DIM,
                                weights=[pre_embedding],
                                input_length=MAX_SEQUENCE_LENGTH,
                                trainable=False)
    sequence_input = Input(shape=(MAX_SEQUENCE_LENGTH,), dtype='int32')
    embedded_sequence = embedding_layer(sequence_input)
    x = Dense(HIDDEN_SIZE, activation='relu')(embedded_sequence)
    x = Dropout(0.2)(x)
    x = LSTM(HIDDEN_SIZE)(x)
    x = Dropout(0.2)(x)
    x = Dense(HIDDEN_SIZE, activation='relu')(x)
    x = Dropout(0.2)(x)
    prediction = Dense(1, activation='sigmoid')(x)

    model = Model(inputs=sequence_input, outputs=prediction)

    optimizer = Adam(lr=0.01)

    model.compile(optimizer=optimizer,
                  loss='binary_crossentropy',
                  metrics=['accuracy'])

    model.fit(x_train, y_train,
              batch_size=BATCH_SIZE,
              epochs=4,
              validation_data=[x_test, y_test])

    x_pred = model.predict(x_test)

    results = [result for result in x_pred]

    return readResult(y_test, results)

    # score, acc = model.evaluate(x_test, y_test,
    #                             batch_size=BATCH_SIZE)
    #
    # print('Test score:', score)
    # print('Test accuracy:', acc)


def bilstmModel(x_train, y_train, x_test, y_test, vocab_size, pre_embedding):


    embedding_layer = Embedding(vocab_size,
                                EMBEDDING_DIM,
                                weights=[pre_embedding],
                                input_length=MAX_SEQUENCE_LENGTH,
                                trainable=False)
    sequence_input = Input(shape=(MAX_SEQUENCE_LENGTH,), dtype='int32')
    embedded_sequence = embedding_layer(sequence_input)
    x = Dense(HIDDEN_SIZE, activation='relu')(embedded_sequence)
    x = Dropout(0.2)(x)
    x = Bidirectional(LSTM(HIDDEN_SIZE))(x)
    x = Dropout(0.2)(x)
    x = Dense(HIDDEN_SIZE, activation='relu')(x)
    x = Dropout(0.2)(x)
    prediction = Dense(1, activation='sigmoid')(x)

    model = Model(inputs=sequence_input, outputs=prediction)

    optimizer = Adam(lr=0.005)

    model.compile(optimizer=optimizer,
                  loss='binary_crossentropy',
                  metrics=['accuracy'])

    model.fit(x_train, y_train,
              batch_size=BATCH_SIZE,
              epochs=4,
              validation_data=[x_test, y_test])

    x_pred = model.predict(x_test)

    results = [result for result in x_pred]

    return readResult(y_test, results)


    # score, acc = model.evaluate(x_test, y_test,
    #                             batch_size=BATCH_SIZE)
    #
    # print('Test score:', score)
    # print('Test accuracy:', acc)


def readResult(y_test,results):

    for i in results[0:60]:
        print(i.tolist())

    index=0
    p=n=tp=tn=fp=fn=0
    for prob in results:
        if prob>0.5:
            predLabel=1
        else:
            predLabel=0
        if y_test[index]>0:
            p+=1
            if predLabel>0:
                tp+=1
            else:
                fn+=1
        else:
            n+=1
            if predLabel==0:
                tn+=1
            else:
                fp+=1
        index+=1

    acc=(tp+tn)/(p+n)
    precisionP=tp/(tp+fp)
    precisionN=tn/(tn+fn)
    recallP=tp/(tp+fn)
    recallN=tn/(tn+fp)
    gmean=math.sqrt(recallP*recallN)
    f_p=2*precisionP*recallP/(precisionP+recallP)
    f_n=2*precisionN*recallN/(precisionN+recallN)
    print ('{gmean:%s recallP:%s recallN:%s} {precP:%s precN:%s fP:%s fN:%s} acc:%s' %(gmean,recallP,recallN,precisionP,precisionN,f_p,f_n,acc))












































