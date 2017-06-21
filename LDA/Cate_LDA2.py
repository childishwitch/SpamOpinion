import io
import re
import string
from math import log
from gensim import corpora, models
import gensim
import time
starttime = time.clock()
replace = r'\s[\.\!\/_,$%^*(+\"\'\:\?\]\[]+|[—！，。？、（）：」「)(【】╱；]+\s'
filename = 'test.txt'
if __name__ == '__main__':
    
    f = io.open('train_8class.txt',mode='r').read()
    #read a line...
    documents = f.split('\n')
    print('First Data: '+str(len(documents)))
    texts = []
    docNum = 0
    for line in documents:
        #裡面有個空白是u3000所以要去掉
        #line = line.replace(u'\u3000 ','')
        #remove the punctuations
        #split the category and the context
        line_list = line.split('\t')
        if (len(line_list) > 1):
            line_list[1] = re.sub(replace,'',line_list[1])
            texts.append(line_list[1].split(' '))
    documents.clear()

    f = io.open('test_8class.txt',mode='r').read()
    #read a line...
    documents = f.split('\n')
    print('Second Data: '+str(len(documents)))
    rightDoc = 0
    wrongDoc = 0
    for line in documents:
        #裡面有個空白是u3000所以要去掉
        #line = line.replace(u'\u3000 ','')
        #remove the punctuations
        #split the category and the context
        line_list = line.split('\t')
        if (len(line_list) > 1):
            line_list[1] = re.sub(replace,'',line_list[1])
            texts.append(line_list[1].split(' '))

    dictionary = corpora.Dictionary(texts)
    dictionary.save('doc2bow.dict')

    corpus = [dictionary.doc2bow(text) for text in texts]

    ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics = 2, id2word = dictionary, passes = 20)
    ldamodel.save('lda.model')
    '''
    ldamodel = gensim.models.ldamodel.LdaModel.load('lda.model')
    dictionary = corpora.Dictionary.load('doc2bow.dict')'''
    f = io.open(filename,mode='r').read()
    f = re.sub(replace,'',f)
    print(f)
    bow = dictionary.doc2bow(f.split(' '))

    topicNum = {}
    topicNum[0] = 'true'
    topicNum[1] = 'false'
    maxCateNum = 0
    maxProb = 0
    for t in ldamodel[bow]:
        print(t)
        if t[1] >= maxProb:
            maxProb = t[1]
            maxCateNum = (int)(t[0])
    maxCate = topicNum[maxCateNum]
    print(maxCate)
