import io
import re
import string
#from math import log
#from gensim import corpora, models
import gensim, logging
import time
import glob
import os
'''logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)'''
starttime = time.clock()
replace = r'\s[\.\!\/_,$%^*(+\"\'\:\?\]\[]+|[—！，。？、（）：」「)(【】╱；]+\s'
evalCate = {}
dim = 200
if __name__ == '__main__':
    f = io.open('train_8class.txt',mode='r').read()
    out = io.open('train.svm',mode='w')
    #read a line...
    documents = f.split('\n')
    print('Training Data: '+str(len(documents)))
    texts = []
    docNum = 0
    cateCount = 1
    for line in documents:
        #裡面有個空白是u3000所以要去掉
        #remove the punctuations
        #split the category and the context
        line_list = line.split('\t')
        if (len(line_list) > 1):
            #initialize evalCate
            if line_list[0] not in evalCate:
                cate_tmp = evalCate[line_list[0]] = {}
                cate_tmp['tp'] = cate_tmp['fp'] = cate_tmp['fn']  = 0
                cate_tmp['cateNo'] = cateCount
                cateCount += 1
            cate_tmp = evalCate[line_list[0]]
            line_list_s = re.split(replace, line_list[1])
            for sentence in line_list_s:
                sentence = re.sub(replace,'',sentence)
                sentence  = sentence.replace(u'\u3000 ','')
                sentence_list = sentence.split()
                if(len(sentence_list) >0):
                    texts.append(sentence_list)
    
    model = gensim.models.Word2Vec(texts, workers=4, min_count=1, size=dim)
    #turn word vectors to doc vector
    for line in documents:
        line_list = line.split('\t')
        if (len(line_list) > 1):
            line_list[1] = re.sub(replace,'',line_list[1])
            out.write(str(evalCate[line_list[0]]['cateNo']))
            docDim = [0]*dim
            lineTmp = line_list[1].split(' ')
            for word in lineTmp:
                try:
                    docDim = docDim + model[word]
                except KeyError:
                    print(word)
                    continue
            docDim = [x/len(lineTmp) for x in docDim]
            for x in range(dim):
                out.write(' '+str(x+1)+':'+str(docDim[x]))
            out.write('\n')
    out.close()
    documents.clear()

    f = io.open('test_8class.txt',mode='r').read()
    out = io.open('test.svm',mode='w')
    documents = f.split('\n')
    print('Testing Data: '+str(len(documents)))
    rightDoc = 0
    wrongDoc = 0
    for line in documents:
        line_list = line.split('\t')
        if (len(line_list) > 1):
            line_list[1] = re.sub(replace,'',line_list[1])
            docDim = [0]*dim
            out.write(str(evalCate[line_list[0]]['cateNo']))
            lineTmp = line_list[1].split(' ')
            errorC = 0
            for word in lineTmp:
                try:
                    docDim = docDim + model[word]
                except KeyError:
                    errorC+=1
                    continue
            print(str(errorC))
            docDim = [x/len(lineTmp) for x in docDim]
            for x in range(dim):
                out.write(' '+str(x+1)+':'+str(docDim[x]))
            out.write('\n')
    out.close()
