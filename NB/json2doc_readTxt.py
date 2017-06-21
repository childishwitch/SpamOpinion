import json
import jieba
import sys
import io
import re
import string
from math import log
jsonName = sys.argv[1]
replace = set([ch for ch in u'[abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789’!\"#$%&\\\'「」（）()*+,-./／:;<=>?@，,。?★、…【】《》？“”‘’！[\\\\]^_`{|}~\\n\\t]+'])
jieba.set_dictionary('dict.txt.big.txt')
#remove space
content = ''.join(io.open(jsonName,'r').read().split())
list1 = jieba.lcut(content)
content = []
for w in list1:
    w = ''.join(ch for ch in w if ch not in replace)
    w = ''.join(w.split())
    if w != '':
        content.append(w)
content = ' '.join(content) 
out = io.open('test.txt','w')
out.write(content)
out.close()

category = {}
termNum = 0
jsonName = 'category.json'
category = json.loads(io.open(jsonName,'r').read())

for cate_tmp in category:
    termNum += len(category[cate_tmp]['termf']) 

weightDic = {}
for cateName in category:
    weightDic[cateName] = 0 
for term in content.split(' '):
    if term == '':
        continue
    for cateName in category:
        if term in category[cateName]['termf']:
            weightDic[cateName] += log(((category[cateName]['termf'][term]+1)*(category[cateName]['doc_prob']))/((category[cateName]['termNum'])+termNum))
        else:
            weightDic[cateName] += log((category[cateName]['doc_prob'])/((category[cateName]['termNum'])+termNum))
                        
maxCate = max(weightDic.keys(), key=(lambda k: weightDic[k]))
print(weightDic)
print(maxCate)
