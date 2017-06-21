import io
import re
import string
from math import log
import json
replace = r'\s[\.\!\/_,$%^*(+\"\'\:\?\]\[]+|[—！，。？、（）：」「)(【】╱；]+\s'
category = {}
evalCate = {}
jsonName = 'categoryDict.json'
jsonName2 = 'evalDict.json'
if __name__ == '__main__':
    f = open('train_8class.txt',mode='r').read()
    jsonFile=open(jsonName,mode='w')
    jsonFile2=open(jsonName2,mode='w')
    #read a line...
    documents = f.split('\n')
    docNum = 0
    idx2cate = []
    for line in documents:
        #裡面有個空白是u3000所以要去掉
        #line = line.replace(u'\u3000 ','')
        #remove the punctuations 
        #split the category and the context
        line_list = line.split('\t')
        if (len(line_list) > 1):
            docNum+=1
            line_list[1] = re.sub(replace,'',line_list[1])
            cateName = line_list[0]
            if cateName not in category:
                category[cateName] = {}
                evalTmp = evalCate[cateName] = {}
                evalTmp['tp'] = evalTmp['fp'] = evalTmp['fn'] = 0
                evalTmp['cateNo'] = len(idx2cate)+1
                idx2cate.append(cateName)
            cate_tmp = category[cateName]
            term_tmp = set()#to count terms in the document
            for term in line_list[1].split(' '):
                if term == '':
                    continue
                if term not in cate_tmp:
                    term_tmp.add(term)
                    cate_tmp[term] = {'df':1,'tf':1,'idx':len(cate_tmp)}
                    continue
                if term not in term_tmp:
                   term_tmp.add(term)
                   (cate_tmp[term])['df']+=1
                (cate_tmp[term])['tf']+=1

    print('Training Data: '+str(docNum))

    print('---computing tfidf and write down the log')
    for cateName in category.keys():
        w = io.open(cateName + '.log',mode='w')
        cate_tmp = category[cateName]
        for term in cate_tmp:
            term_tmp = cate_tmp[term]
            cate_tmp[term] = {'idx':term_tmp['idx'],'tfidf':(term_tmp['tf'])*(log(float(docNum)/(term_tmp['df'])))}
            w.write(term + ":" + str(term_tmp['df']) + ":"+str(term_tmp['tf'])+":"+str(cate_tmp[term]['tfidf']) + "\n")
        w.close()
    '''jsonFile.write(json.dumps(category))
    jsonFile.close()
    jsonFile2.write(json.dumps(evalCate))
    jsonFile2.close()
    category=json.loads(open(jsonName,mode='r').read())
    evalCate=json.loads(open(jsonName2,mode='r').read())'''

    print('---writing training svm---')
    f = open('train_8class.txt',mode='r').read()
    out = open('train_8class.svm',mode='w')
    test = open('train_8class.log',mode='w')
    documents = f.split('\n')
    docNum = 0
    for line in documents:
        line_list = line.split('\t')
        if (len(line_list) > 1):
            print('computing doc '+str(docNum)+' in training data')
            test.write('computing doc '+str(docNum)+' in training data\n')
            line_list[1] = re.sub(replace,'',line_list[1])
            cate = line_list[0]
            vecDict = {}
            for cateName in category:
                vecDict[cateName] = [0]*len(category[cateName])
            for term in line_list[1].split(' '):
                if term == '':
                    continue
                for cateName in category:
                    cate_tmp = category[cateName]
                    docVec = vecDict[cateName]
                    if term in cate_tmp:
                        docVec[cate_tmp[term]['idx']] += cate_tmp[term]['tfidf']
                        #print('find '+term+' in '+cateName)
            out.write(str(evalCate[cate]['cateNo']))
            base = 0
            for idx in range(len(idx2cate)):
                cateName = idx2cate[idx]
                docVec = vecDict[cateName]
                test.write(cateName+' '.join('{0}:{1}'.format(vecIdx+1,docVec[vecIdx]) for vecIdx in range(len(docVec)) if docVec[vecIdx] > 0)+'\n')
                out.write(' '+' '.join('{0}:{1}'.format(base+vecIdx+1,docVec[vecIdx]) for vecIdx in range(len(docVec)) if docVec[vecIdx] > 0))
                base += len(docVec)
            out.write('\n')
            docNum+=1
    out.close()
    test.close()

    '''
    print('---writing testing svm---')
    f = open('test_8class.txt',mode='r').read()
    out = open('test_8class.svm',mode='w')
    documents = f.split('\n')
    docNum = 0
    for line in documents:
        line_list = line.split('\t')
        if (len(line_list) > 1):
            print('computing doc '+str(docNum)+' in testing data')
            line_list[1] = re.sub(replace,'',line_list[1])
            cate = line_list[0]
            vecDict = {}
            for cateName in category:
                vecDict[cateName] = [0]*len(category[cateName])
            for term in line_list[1].split(' '):
                if term == '':
                    continue
                for cateName in category:
                    cate_tmp = category[cateName]
                    docVec = vecDict[cateName]
                    if term in cate_tmp:
                        docVec[cate_tmp[term]['idx']] += cate_tmp[term]['tfidf']
            out.write(str(evalCate[cate]['cateNo']))
            base = 0
            for idx in range(len(idx2cate)):
                cateName = idx2cate[idx]
                docVec = vecDict[cateName]
                out.write(' '+' '.join('{0}:{1}'.format(base+vecIdx+1,docVec[vecIdx]) for vecIdx in range(len(docVec)) if docVec[vecIdx] > 0))
                base += len(docVec)
            out.write('\n')
            docNum+=1
    out.close()
    print('Testing Data: '+str(docNum))'''


