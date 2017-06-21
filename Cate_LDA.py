import io
import re
import string
from math import log
from gensim import corpora, models
import gensim
import time
starttime = time.clock()
replace = r'\s[\.\!\/_,$%^*(+\"\'\:\?\]\[]+|[—！，。？、（）：」「)(【】╱；]+\s'
cateTags = []
evalCate = {}
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
            #initialize evalCate
            if line_list[0] not in evalCate:
                cate_tmp = evalCate[line_list[0]] = {}
                cate_tmp['tp'] = cate_tmp['fp'] = cate_tmp['fn']  = 0
            #remember the tags
            cateTags.append(line_list[0])
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
            cateTags.append(line_list[0])

    dictionary = corpora.Dictionary(texts)

    corpus = [dictionary.doc2bow(text) for text in texts]

ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics = len(evalCate), id2word = dictionary, passes = 20)

endtime = time.clock()
print('execution time:'+str(endtime-starttime))
topicNum = {}
while(input('Type \'y\' to start the evaluation(y/n): ').strip() == 'y'):
    for topic in ldamodel.print_topics(num_topics=len(evalCate), num_words=20):
        print(topic)
    for cateName in evalCate.keys():
        topicNum[int(input('What is the id of '+cateName+'? ').strip())] = cateName
        '''print(topicNum)'''
    starttime = time.clock()
    for x in range(len(corpus)):
        maxCateNum = 0
        maxProb = 0
        for t in ldamodel[corpus[x]]:
            '''print(t)'''
            if t[1] >= maxProb:
                maxProb = t[1]
                maxCateNum = (int)(t[0])
        '''print('choose: '+str(maxCateNum)+' : '+str(maxProb))'''
        cate = cateTags[x]
        '''print('maxCate is: '+topicNum[maxCateNum])'''
        maxCate = topicNum[maxCateNum]
        if maxCate == cate:
            rightDoc+=1
            evalCate[cate]['tp'] += 1
        else:
            wrongDoc+=1
            evalCate[maxCate]['fp'] += 1
            evalCate[cate]['fn'] += 1
    #display result
    print('Classify using LDA method\nrightDoc: '+str(rightDoc)+'\twrongDoc: '+str(wrongDoc)+'\naccuracy: '+str((float(rightDoc)/(rightDoc+wrongDoc))))
    for key in evalCate.keys():
        cateTmp = evalCate[key]
        p = (float(cateTmp['tp'])/(cateTmp['tp']+cateTmp['fp']))
        r = (float(cateTmp['tp'])/(cateTmp['tp']+cateTmp['fn']))
        print('Category: '+key+'\nPrecision: '+str(p)+'\tRecall: '+str(r)+'\tF-Score: '+str(2*p*r/(p+r)))
    print('Micro-AVG Precision: '+str(float(sum([evalCate[cateNo]['tp'] for cateNo in evalCate]))/sum([evalCate[cateNo2]['tp']+evalCate[cateNo2]['fp'] for cateNo2 in evalCate]))+'\tMicro-AVG Recall: '+str(float(sum([evalCate[cateNo3]['tp'] for cateNo3 in evalCate]))/sum([evalCate[cateNo4]['tp']+evalCate[cateNo4]['fn'] for cateNo4 in evalCate])))
    endtime = time.clock()
    print('execution time:'+str(endtime-starttime))
