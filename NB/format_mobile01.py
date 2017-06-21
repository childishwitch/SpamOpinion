import json
import jieba
import sys
import io
import re
import string
from math import log
jsonName = sys.argv[1]
replace = set([ch for ch in u'[abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789’!\"#$%&\\\'「」（）()*+,-./／:;<=>?@，,。?★、…【】《》？“”‘’！[\\\\]^_`{|}~\\n\\t]+'])
replace2 = r'\s[\.\!\/_,$%^*(+\"\'\:\?\]\[]+|[—！，。？、（）：」「)(【】╱；]+\s'
replace.update(ch for ch in replace2)
jieba.set_dictionary('dict.txt.big.txt')
docList = json.loads(io.open(jsonName,'r').read())
out = io.open('format.txt','w')
for doc in docList:
    content = ''.join(doc['content'].split())
    list1 = jieba.lcut(content)
    #print('|'.join(list1))
    list2 = doc['content'] = []
    for w in list1:
        w = ''.join(ch for ch in w if ch not in replace)
        w = ''.join(w.split())
        if w != '':
            list2.append(w)
    content = ' '.join(doc['content'])
    tag = doc['is_spam']
    if (tag):
        tag = 'true'
    else:
        tag = 'false'
    out.write(tag+'\t'+content+'\n')
out.close()
