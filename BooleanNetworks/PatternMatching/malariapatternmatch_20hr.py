import findmorsegraph as fmg
import patternmatch as pm
from itertools import permutations
from subprocess import call
import sys


def getAllParams(fname="networks/5D_Malaria_20hr.txt",smallestparam=0,largestparam=8640000,getMorseSet=fmg.is_FP_clock):
    params=fmg.scan(fname,smallestparam,largestparam,getMorseSet,firstonly=False)
    f=open('storeparams.txt','w')
    f.write(str(params))
    f.close()
    return params

def parseParams(fname="storeparams.txt",format=1):
    f=open(fname,'r')
    if format==1:
        params=eval(f.readline())
    else:
        params=[]
        for r in f.readlines():
            if r != '\n':
                params.append((int(r),0))
    f.close()
    return params

def setPattern():
    f=open('patterns.txt','w')
    for s1 in permutations(['x3 max','x5 max','x1 max', 'x4 max']):
        patternstr1=', '.join(s1) + ', x2 max, '
        for s2 in permutations(['x1 min', 'x3 min','x5  min', 'x2 min','x4 min']):
            patternstr2=patternstr1 + ', '.join(s2) + ', ' + s1[0] + '\n'
            f.write(patternstr2)
    f.close()

def patternSearch(fname="networks/5D_Malaria_20hr.txt",smallestparam=100000,largestparam=200000,getMorseSet=fmg.is_FP_clock,paramsstored=1,paramformat=1):
    setPattern()
    if paramsstored:
        if paramformat==1:
            params = parseParams("storeparams.txt",paramformat)
        else:
            params = parseParams("storedparams1.txt",paramformat)
    else:
        params = getAllParams(fname,smallestparam,largestparam,getMorseSet)
        f=open("storeparams.txt",'w')
        f.write(str(params))
        f.close()
    N=len(params)
    f=open('malariaresults_20hr.txt','w')
    for k,(p,m) in enumerate(params):
        print "Parameter {} of {}".format(k+1,N)
        if type(m) is tuple:
            for n in m:
                call(["dsgrn network {} analyze morseset {} {} >dsgrn_output.json".format(fname,n,p)],shell=True)
                patterns,matches=pm.callPatternMatch(writetofile=0,returnmatches=1)
                for q,c in zip(patterns,matches):
                    f.write("Parameter: {}, Morseset: {}".format(p,n)+'\n')
                    f.write("Pattern: {}".format(q)+'\n')
                    f.write("Results: {}".format(c)+'\n')
        else:
            call(["dsgrn network {} analyze morseset {} {} >dsgrn_output.json".format(fname,m,p)],shell=True)
            patterns,matches=pm.callPatternMatch(writetofile=0,returnmatches=1)
            for q,c in zip(patterns,matches):
                f.write("Parameter: {}, Morseset: {}".format(p,m)+'\n')
                f.write("Pattern: {}".format(q)+'\n')
                f.write("Results: {}".format(c)+'\n')
    f.close()


if __name__=='__main__':
    # setPattern()
    patternSearch(paramsstored=0)



