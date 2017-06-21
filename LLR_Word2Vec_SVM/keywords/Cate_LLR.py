# encoding: utf-8
import io
import re
import string
from math import log
replace = r'\s[\.\!\/\-\>\<_,$%^*(+\"\'\:\?\]\[]+|[—！，。？、（）：」「)(【】╱；]+\s'
category = {}
termNum = 0
data = '../../train_8class.txt'
if __name__ == '__main__':
    f = io.open(data,mode='r').read()
    #read a line...
    documents = f.split('\n')
    docNum = 0
    print('Training Data: '+str(docNum))
    for line in documents:
        #裡面有個空白是u3000所以要去掉
        #line = line.replace(u'\u3000 ','')
        #remove the punctuations 
        #split the category and the context
        line_list = line.split('\t')
        if (len(line_list) > 1):
            line_list[1] = re.sub(replace,'',line_list[1])
            docNum += 1
            if line_list[0] not in category:
                cate_tmp = category[line_list[0]] = {}
                cate_tmp['tp'] = cate_tmp['fp'] = cate_tmp['fn'] = cate_tmp['docNum'] = 0
                cate_tmp['df'] = {}#caculate every frequencyi
                cate_tmp['score'] = {}
            else:
                cate_tmp = category[line_list[0]]
            term_tmp = set()
            #to count df
            for term in line_list[1].split(' '):
                if (len(term) == 1) | (term == ''):
                    continue
                if term not in cate_tmp['df']:
                    (cate_tmp['df'][term]) = 1
                elif term not in term_tmp:
                    (cate_tmp['df'][term]) += 1 
                term_tmp.add(term)
            (cate_tmp['docNum']) += 1
            docNum += 1
    #documents.clear()
    #caculate the score
    for cateName in category:
        cate_tmp = category[cateName]
        for term in cate_tmp['df']:
            n = cate_tmp['docNum']
            n11 = cate_tmp['df'][term]
            n10 = n - n11
            n01 = 0
            for cateName2 in category:
                if ((cateName2 != cateName) and (term in category[cateName2]['df'])):
                    n01 += category[cateName2]['df'][term]
            n00 = docNum - n - n01
            #print(cateName+':'+term+':'+str(n)+':'+str(n11)+':'+str(n10)+':'+str(n01)+':'+str(n00))
            tmpScore = (n11*(log(n11+n01) - log(docNum)))
            tmpScore += (n10*(log(docNum-n11-n01)-log(docNum)))
            tmpScore += (n01*(log(n11+n01)-log(docNum)))
            tmpScore += (n00*(log(docNum-n11-n01)-log(docNum)))
            tmpScore -= (n11*(log(n11)-log(n11+n10)))
            if n10 != 0:
                tmpScore -= n10*(log(n10)-log(n11+n10))
            if n01 != 0:
                tmpScore -= n01*(log(n01)-log(n01+n00))
            tmpScore -= (n00*(log(n01+n00-n01)-log(n01+n00)))
            cate_tmp['score'][term] = -2.0*tmpScore
            #cate_tmp['score'][term] = -2.0*((n11*(log(n11+n01) - log(docNum)))+(n10*(log(docNum-n11-n01)-log(docNum)))+(n01*(log(n11+n01)-log(docNum)))+(n00*(log(docNum-n11-n01)-log(docNum)))-(n11*(log(n11)-log(n11+n10)))-(n10*(log((n11+n10-n11)/(n11+n10))))-(n00*(log(n01+n00-n01)-log(n01+n00))))
    '''
    for cateName in category:
        print('category: '+cateName)
        #print(category[cateName])
        sortScore = (category[cateName]['score']).sort(reverse=True)
        rankNum = 10
        for term in sortScore:
            print(term + ':' + str(sortScore[term]))
            rankNum -= 1
            if rankNum <= 0:
                break
    '''
    for cateName in category:
        #print('==='+cateName+'===')
        out = open(cateName+'.txt','w')
        sorted_category = sorted(category[cateName]['score'].items() , key=lambda d:d[1],  reverse = True)
        rankNum = 100
        for j in sorted_category:
            #out.write(j[0]+':'+str(j[1])+'\n')
            out.write(str(category[cateName]['score'][j[0]])+'\t'+j[0]+'\n')
            rankNum -= 1
            if rankNum <= 0:
                break
        out.close()
