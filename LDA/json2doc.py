import json
import jieba
import sys
import io
import re
import string
from gensim import corpora, models
import gensim
jsonName = sys.argv[1]
replace = set([ch for ch in '!"#$%&\'()*+,-./:;<=>?@[\]^_`{|}~'])
replace2 = r'\s[\.\!\/_,$%^*(+\"\'\:\?\]\[]+|[—！，。？、（）：」「)(【】╱；]+\s'
jieba.set_dictionary('dict.txt.big.txt')
doc = json.loads(io.open(jsonName,'r').read())
content = ''.join(doc['content'].split())
list1 = jieba.lcut(content)
#print('|'.join(list1))
list2 = doc['content'] = []
for w in list1:
    #w = ''.join(ch for ch in w if w not in replace)
    w = w.strip()
    if w != '':
        list2.append(w)
'''title = doc['title']
title = re.sub(replace2,'',title)
list1 = jieba.lcut(title)
list2 = doc['title'] = []
for w in list1:
    #w = ''.join(ch for ch in w if w not in replace)
    w = w.strip()
    if w != '':
        list2.append(w)'''
content = ' '.join(doc['content']) 
content = re.sub(replace2,'',content)
out = io.open('test.txt','w')
out.write(content)
out.close()
ldamodel = gensim.models.ldamodel.LdaModel.load('lda.model')
dictionary = corpora.Dictionary.load('doc2bow.dict')
#f = io.open(filename,mode='r').read()
content = re.sub(replace2,'',content)
print(content)
bow = dictionary.doc2bow(content.split(' '))
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
