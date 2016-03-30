import numpy as np
import matplotlib.pyplot as plt
import pydot

def parseFile(bound=0,fname='/Users/bcummins/ProjectData/yeast/haase-fpkm-p1_yeast_s29_top25dljtk_lem_score_table.txt'):
    f=open(fname,'r')
    source=[]
    type_reg=[]
    target=[]
    lem_score=[]
    f.readline()
    f.readline()
    f.readline()
    for l in f.readlines():
        wordlist=l.split()
        if float(wordlist[5])>bound:
            target.append(wordlist[0])
            lem_score.append(float(wordlist[5]))
            two_words=wordlist[2].split('(')
            type_reg.append(two_words[0])
            source.append(two_words[1][:-1])
        else:
            break
    f.close()
    return source,target,type_reg,lem_score
