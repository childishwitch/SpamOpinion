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
concepts = {}
howNet = {} 
keywords = set()
dataBaseDir = '../../cate/Cate_LLR/'
dim = 200
if __name__ == '__main__':
    for filename in glob.glob(dataBaseDir+'NEOntology/*.txt'):
        filename = os.path.splitext(os.path.basename(filename))[0]
        #print(filename)
        try:
            for text in io.open(dataBaseDir+'NEOntology/'+filename+'.txt','r').read().split('\n'):
                 concepts[text] = filename
        except UnicodeDecodeError:
            for text in io.open(dataBaseDir+'NEOntology/'+filename+'.txt','r',encoding='big5').read().split('\n'):
                 concepts[text] = filename
    for row in io.open(dataBaseDir+'Mapping_Word2Node_20161013.txt').read().split('\n'):
        row = row.split('\t')
        if len(row) > 1:
            howNet[row[0]] = row[1]
    f = io.open('../test_8class.txt',mode='r').read()
    out = io.open('test.svm',mode='w')
    test = io.open('Test.txt',mode='w')
    tag = io.open('Tag.txt',mode='w')
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
                cate_tmp['keywords'] = io.open('keywords/'+line_list[0]+'.txt','r').read().split('\n')
                keywords.update(cate_tmp['keywords'])
                print(len(keywords))
                #print(line_list[0]+' : '+str(cateCount))
                cateCount += 1
            cate_tmp = evalCate[line_list[0]]
            line_list_s = re.split(replace, line_list[1])
            for sentence in line_list_s:
                sentence = re.sub(replace,'',sentence)
                sentence  = sentence.replace(u'\u3000 ','')
                sentence_list = sentence.split(' ')
                attr = []
                tag_list = []
                test.write(sentence+'\n')
                index = 0
                while index < len(sentence_list):
                    #if s2 not in cate_tmp['keywords'] and s2 not in concepts and s2 not in howNet or s2 == '':
                        #print(sentence_list)
                        #print('remove '+sentence_list.pop(sentence_list.index(s2)))
                        #sentence_list.pop(sentence_list.index(s2))
                    s2 = (sentence_list[index]).strip()
                    if s2 == '':
                        index += 1
                        continue
                    if s2 in keywords:
                        #test.write(str(index)+': '+s2+' K\n')
                        tag_list.append('{'+s2+'}')
                        attr.append('K')
                    elif s2 in concepts:
                        sentence_list.pop(index)
                        sentence_list.insert(index,concepts[s2])
                        tag_list.append('['+concepts[s2]+']')
                        #test.write(str(index)+': '+s2+' C-> '+concepts[s2]+' : '+' '.join(sentence_list)+'\n')
                        attr.append('C')
                    elif s2 in howNet:
                        sentence_list.pop(index)
                        sentence_list.insert(index,howNet[s2])
                        tag_list.append('['+howNet[s2]+']')
                        #test.write(str(index)+': '+s2+' H-> '+howNet[s2]+' : '+' '.join(sentence_list)+'\n')
                        attr.append('H')
                    else:
                        sentence_list.pop(index)
                        #test.write(str(index)+': '+s2+' N : '+' '.join(sentence_list)+'\n')
                        attr.append('N')
                        index-=1
                    '''tag_list.append(s2)'''
                    index+=1
                if(len(sentence_list) >0):
                    texts.append(sentence_list)
                    test.write(' '.join(attr)+'\n')
                    test.write(' '.join(sentence_list)+'\n')
                    tag.write(' '.join(tag_list)+'\n')
    
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
                    continue
            docDim = [x/len(lineTmp) for x in docDim]
            for x in range(dim):
                out.write(' '+str(x+1)+':'+str(docDim[x]))
            out.write('\n')
    out.close()
    documents.clear()
'''
    f = io.open('test_8class.txt',mode='r').read()
    out = io.open('SVM_TestingData_LLR.txt',mode='w')
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
            for word in lineTmp:
                try:
                    docDim = docDim + model[word]
                except KeyError:
                    continue
            docDim = [x/len(lineTmp) for x in docDim]
            for x in range(dim):
                out.write(' '+str(x+1)+':'+str(docDim[x]))
            out.write('\n')
    out.close()
endtime = time.clock()
print('execution time:'+str(endtime-starttime))'''
