#encoding: utf-8
import io
import re
import string
from math import log
import json
replace = r'\s[\.\!\/_,$%^*(+\"\'\:\?\]\[]+|[—！，。？、（）：」「)(【】╱；]+\s'
category = {}
termNum = 0
jsonName = 'category.json'
inFile = 'test.txt'
if __name__ == '__main__':
    category = json.loads(io.open(jsonName,'r').read())

    for cate_tmp in category:
        termNum += len(category[cate_tmp]['termf']) 

    f = io.open(inFile,mode='r').read()
    weightDic = {}
    for cateName in category:
        weightDic[cateName] = 0 
    for term in f.split(' '):
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
