import findmorsegraph as fmg
import patternmatch as pm
from itertools import permutations
from subprocess import call
import useDSGRN
import sys


# def getAllParams(fname="networks/5D_Malaria_20hr.txt",smallestparam=0,largestparam=8640000,getMorseSet=fmg.is_FP_clock):
#     params=fmg.scan(fname,smallestparam,largestparam,getMorseSet,firstonly=False)
#     f=open('storeparams.txt','w')
#     f.write(str(params))
#     f.close()
#     return params

# def parseParams(fname="storeparams.txt",format=1):
#     f=open(fname,'r')
#     if format==1:
#         params=eval(f.readline())
#     else:
#         params=[]
#         for r in f.readlines():
#             if r != '\n':
#                 params.append((int(r),0))
#     f.close()
#     return params

def setPattern():
    f=open('patterns.txt','w')
    for s1 in permutations(['x3 max','x5 max','x1 max', 'x4 max']):
        patternstr1=', '.join(s1) + ', x2 max, '
        for s2 in permutations(['x1 min', 'x3 min','x5  min', 'x2 min','x4 min']):
            patternstr2=patternstr1 + ', '.join(s2) + ', ' + s1[0] + '\n'
            f.write(patternstr2)
    f.close()

def patternSearch(morseset=0,specfile="networks/5D_Malaria_20hr.txt",paramfile="5D_Malaria_2015_FCParams.txt",resultsfile="results_5Dmalaria_20hr.txt"):
    setPattern()
    useDSGRN.patternSearch(morseset,specfile,paramfile,resultsfile,printparam=1)


if __name__=='__main__':
    setPattern()
    parameter=116014
    useDSGRN.patternSearchSingle(parameter,specfile="networks/5D_Malaria_20hr.txt",resultsfile='results_malaria_param{}.txt'.format(parameter))
    # patternSearch()



