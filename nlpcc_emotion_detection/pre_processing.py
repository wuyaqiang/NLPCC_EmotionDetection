import os


class Post:
    def __init__(self, content, happiness, sadness, anger, fear, surprise):
        self.content = content
        self.happiness = happiness.lower()
        self.sadness = sadness.lower()
        self.anger = anger.lower()
        self.fear = fear.lower()
        self.surprise = surprise.lower()

        self.label = getLabel(self)

        self.words = {}     # the whole content words
        self.en = {}        # the english content words
        self.cn = {}        # the chinese content words

        for w in content.split():
            w = w.lower()
            self.words[w] = 1
            if isASCII(w):
                self.en[w] = 1
            else:
                self.cn[w] = 1

def isASCII(word):
    flag=True
    for c in word:
        if ord(c)>128:
            flag=False
            break
    return flag



def readPosts():
    posts = []
    postBegin = False
    post = []
    d = {}
    for fpath in os.listdir(r'../data'):
        for line in open(r'../data/%s' %fpath,'r'):
            line = line.strip()
            if len(line) > 0:
                if line[:10] == '<Tweet id=':
                    postBegin = True
                    continue
                if line == '</Tweet>':
                    postBegin = False
                    content = post[5 * 3 + 1]
                    happiness = post[0 * 3 + 1].lower()
                    sadness = post[1 * 3 + 1].lower()
                    anger = post[2 * 3 + 1].lower()
                    fear = post[3 * 3 + 1].lower()
                    surprise = post[4 * 3 + 1].lower()

                    if content not in d:
                        posts.append(Post(content, happiness, sadness, anger, fear, surprise))
                        d[content] = 0

                    post = []
                    continue
                if postBegin:
                    post.append(line)
    return posts


# def getLabel(post):
#     label = [0,0,0,0,0]
#
#     if post.happiness == 't':   label[0] = 1
#     if post.sadness == 't':     label[1] = 1
#     if post.anger == 't':       label[2] = 1
#     if post.fear == 't':        label[3] = 1
#     if post.surprise == 't':    label[4] = 1
#
#     return label

def getLabel(post):
    label = 0
    if post.happiness == 't':   label = 1
    return label




























