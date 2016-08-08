# -*- coding: utf-8 -*-
"""
Created on Fri Jan 08 13:16:49 2016

@author: huihui
"""


import re
import codecs

#对于切分之后的[ ] 心情符号，将括号中的空格删除
#二次处理：分词之后存在标点未切分的情况需要再处理
def emotion(line):
    pattern1=re.compile(u'\[.*?\]')
    #pattern2=re.compile(u'【|】|\||#|~|-|～|~|！|')
    replecedstr=re.sub(pattern1,lambda m:' '+''.join(m.group(0).split())+' ',line)
 #   replecedstr=re.sub(pattern2,'',replecedstr)
    return replecedstr


def e(filename,outName):
    infile=codecs.open(filename,'r',encoding='utf-8')
    outfile=codecs.open(outName,'w',encoding='utf-8')
    
    for line in infile.readlines():
        if line:
            line=emotion(line)
            outfile.write(line)
    infile.close()
    outfile.close()
    
if __name__ == '__main__':
    e('train_quzao.txt_fenci','train_e')
#    e('weibo_quzao.txt_fenci','weibo_e.txt')
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    