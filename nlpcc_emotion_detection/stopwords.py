
def stopwordsList(filepath):
    stopwords = [line.strip() for line in open(filepath, 'r',encoding='GB18030').readlines()]
    return stopwords


def afterStopwords(sentence):
    stopwords = stopwordsList('./stopwords/HIT_stopwords.txt')
    result_sentence = ''
    for word in sentence:
        if word not in stopwords:
            if word != '\t':
                result_sentence += word
                # result_sentence += " "
    return result_sentence
