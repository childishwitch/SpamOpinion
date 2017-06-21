#encoding: utf-8
import io
import re
import string
from math import log
import json
replace = r'\s[\.\!\/_,$%^*(+\"\'\:\?\]\[]+|[—！，。？、（）：」「)(【】╱；]+\s'
category = {}
termNum = 0
jsonName = 'category0.25.json'
trainFile = 'train_8class.txt'
testFile = 'test_8class.txt'
if __name__ == '__main__':
    f = io.open(trainFile,mode='r').read()
    #read a line...
    documents = f.split('\n')
    docNum = len(documents)
    print('Training Data: '+str(docNum))
    for line in documents:
        #裡面有個空白是u3000所以要去掉
        #line = line.replace(u'\u3000 ','')
        #remove the punctuations 
        #split the category and the context
        line_list = line.split('\t')
        if (len(line_list) > 1):
            line_list[1] = re.sub(replace,'',line_list[1])
            if line_list[0] not in category:
                cate_tmp = category[line_list[0]] = {}
                cate_tmp['tp'] = cate_tmp['fp'] = cate_tmp['fn'] = cate_tmp['termNum'] = 0
                cate_tmp['doc_prob'] = 1#caculate the number of doc in this cate first
                cate_tmp['termf'] = {}
            cate_tmp = category[line_list[0]]
            term_tmp = set()#to count terms in the document
            for term in line_list[1].split(' '):
                if term == '':
                    continue
                if term not in cate_tmp['termf']:
                    cate_tmp['termf'][term] = 0
                (cate_tmp['termf'][term])+=1
                cate_tmp['termNum']+=1
    #caculate the probability and amount of terms
    for cate_tmp in category:
        category[cate_tmp]['doc_prob'] /= float(len(category))
    del documents
    jsonFile=io.open(jsonName,'w')
    jsonFile.write(json.dumps(category))
    jsonFile.close()
    '''category = json.loads(io.open(jsonName,'r').read())'''

    for cate_tmp in category:
        termNum += len(category[cate_tmp]['termf']) 

    f = io.open(testFile,mode='r').read()
    #read a line...
    documents = f.split('\n')
    print('Testing Data: '+str(len(documents)))
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
            cate = line_list[0]
            weightDic = {}
            for cateName in category:
                weightDic[cateName] = 0 
            for term in line_list[1].split(' '):
                if term == '':
                    continue
                for cateName in category:
                    if term in category[cateName]['termf']:
                        weightDic[cateName] += log(((category[cateName]['termf'][term]+1)*(category[cateName]['doc_prob']))/((category[cateName]['termNum'])+termNum))
                    else:
                        weightDic[cateName] += log((category[cateName]['doc_prob'])/((category[cateName]['termNum'])+termNum))
                        
            '''maxCate = (weightDic.keys())[0]
            for cateName in category:
                if weightDic[cateName] > weightDic[maxCate]:maxCate = cateName'''
            maxCate = max(weightDic.keys(), key=(lambda k: weightDic[k]))
            '''print(maxCate)'''
            #evaluation
            if maxCate == cate:
                rightDoc+=1
                category[cate]['tp'] += 1
            else:
                wrongDoc+=1
                category[maxCate]['fp'] += 1
                category[cate]['fn'] += 1
    print('rightDoc: '+str(rightDoc)+'\twrongDoc: '+str(wrongDoc)+'\naccuracy: '+str((float(rightDoc)/(rightDoc+wrongDoc))))
    for cateName in category:
        cateTmp = category[cateName]
        p = (float(cateTmp['tp'])/(cateTmp['tp']+cateTmp['fp']))
        r = (float(cateTmp['tp'])/(cateTmp['tp']+cateTmp['fn']))
        print('Category: '+cateName+'\t'+str(cateTmp['tp']+cateTmp['fn'])+'\nPrecision: '+str(p)+'\tRecall: '+str(r)+'\tF-Score: '+str(2*p*r/(p+r))+'\ttp: '+str(cateTmp['tp']))
