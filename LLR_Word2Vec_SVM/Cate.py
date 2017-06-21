import io
import string
#from math import log
#from gensim import corpora, models
import time
import glob, os
starttime = time.clock()
evalCate = {}
if __name__ == '__main__':
    rightDoc = wrongDoc = 0
    '''for line in open('cateNo.log','rU').read().split('\n'):
        print(line)
        if(line.strip() != ''):
            lineList = line.split(' ')
            filename = lineList[0]
            fnNo = int(lineList[2])
            evalCate[fnNo] = {'title':filename}
            print('fileNo: '+lineList[2]+' filename: '+filename)'''
    evalCate = {1:{'title':'true'},2:{'title':'false'}}
    for cate in evalCate:
        cateTmp = evalCate[cate]
        cateTmp['tp'] = cateTmp['fp'] = cateTmp['fn'] = 0
    f = io.open('test.svm',mode='r').read()
    out = io.open('tdata.out',mode='r').read()
    documents = f.split('\n')
    predict = out.split('\n')
    rightDoc = 0
    wrongDoc = 0
    for lineNo in range(len(documents)):
        print(str(lineNo))
        line_list = (documents[lineNo]).split(' ')
        if (len(line_list) > 1):
            if(line_list[0] == predict[lineNo]):
                rightDoc+=1
                evalCate[int(line_list[0])]['tp'] += 1
            else:
                wrongDoc+=1
                evalCate[int(line_list[0])]['fn'] += 1
                evalCate[int(predict[lineNo])]['fp'] += 1
        else:
            print('lineNo: '+str(lineNo+1)+' has some trouble')
    #display result
    docNum = rightDoc+wrongDoc
    print('Testing Data: '+str(docNum))
    print('Classify using LLR+Word2Vec+SVM(c:1 g:1) method\nrightDoc: '+str(rightDoc)+'\twrongDoc: '+str(wrongDoc)+'\naccuracy: '+str((float(rightDoc)/(rightDoc+wrongDoc))))
    for cateNo in evalCate:
        cateTmp = evalCate[cateNo]
        if cateTmp['fp'] == 0:
            print('Category: '+cateTmp['title']+'\n')
            print('fp is zero!!!\n')
        if cateTmp['tp'] == 0:
            print('Category: '+cateTmp['title']+'\n')
            print('tp is zero!!!\n')
            p = cateTmp['p'] = 0
            r = cateTmp['r'] = 0
            f = cateTmp['f'] = 0
        else:
            p = cateTmp['p'] = (float(cateTmp['tp'])/(cateTmp['tp']+cateTmp['fp']))
            r = cateTmp['r'] = (float(cateTmp['tp'])/(cateTmp['tp']+cateTmp['fn']))
            cateTmp['f'] = 2*p*r/(p+r)
            print('Category: '+cateTmp['title']+str(cateTmp['tp']+cateTmp['fn'])+'\nPrecision: '+str(cateTmp['p'])+'\tRecall: '+str(cateTmp['r'])+'\tF-Score: '+str(cateTmp['f']))
    print('Micro-AVG Precision: '+str(float(sum([((evalCate[cateNo]['p'])*(float(evalCate[cateNo]['tp']+evalCate[cateNo]['fn'])/docNum)) for cateNo in evalCate])))+'\tMicro-AVG Recall: '+str(float(sum([((evalCate[cateNo]['r'])*(float(evalCate[cateNo]['tp']+evalCate[cateNo]['fn'])/docNum)) for cateNo in evalCate])))+'\tMicro-AVG F-Score: '+str(float(sum([((evalCate[cateNo]['f'])*(float(evalCate[cateNo]['tp']+evalCate[cateNo]['fn'])/docNum)) for cateNo in evalCate]))))
    #print('Micro-AVG Precision: '+str(float(sum([evalCate[cateNo]['tp'] for cateNo in evalCate]))/sum([evalCate[cateNo2]['tp']+evalCate[cateNo2]['fp'] for cateNo2 in evalCate]))+'\tMicro-AVG Recall: '+str(float(sum([evalCate[cateNo3]['tp'] for cateNo3 in evalCate]))/sum([evalCate[cateNo4]['tp']+evalCate[cateNo4]['fn'] for cateNo4 in evalCate])))
    endtime = time.clock()
print('execution time:'+str(endtime-starttime))
