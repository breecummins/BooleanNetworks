import numpy as np
import makeboxes
import itertools, sys

def test4DExample1(A=np.arange(0.05,12.25,0.5),B=np.arange(0.05,12.25,0.5),C=np.arange(0.05,12.25,0.5),D=np.arange(0.05,12.25,0.5),E=np.arange(0.05,12.25,0.5),F=np.arange(0.05,1,0.25)):
    '''
    Create all parameter sets given as ranges in the arguments.
    **Assume equal decay rates of 1.**

    '''
    # define the interactions between variables
    variables = ['x','y1','y2','z']
    affectedby = [['x','y2','z'],['x'],['y1'],['x']]
    # give the thresholds for each interaction
    thresholds = [[2,1,1],[3],[1],[1]]
    # give the maps and amplitudes of each interaction (upper and lower bounds for parameter search)
    maps = [[(0,0,0),(1,0,0),(0,1,0),(1,1,0),(0,0,1),(1,0,1),(0,1,1),(1,1,1)],[(0,),(1,)],[(0,),(1,)],[(0,),(1,)]]
    ampfunc = lambda a,b,c,d,e,f: [[0,e,a,a+e,0,f*e,f*a,(a+e)*f],[0,c],[0,d],[0,b]]
    # give the endogenous production rates. 
    productionrates = [0.1,0.5,0.5,0.5] 
    # get upper and lower bounds
    bigamps = ampfunc(A[-1],B[-1],C[-1],D[-1],E[-1],F[-1])
    upperbounds = 1.1*( np.array([np.max(u) for u in bigamps]) + np.array(productionrates) ) 
    lowerbounds = np.zeros(upperbounds.shape)
    # make domains
    thresh,ainds,pr = makeboxes.makeParameterArrays(variables, affectedby, thresholds, productionrates)
    doms = makeboxes.getDomains(thresh,lowerbounds,upperbounds)
    numsets = len(A)*len(B)*len(C)*len(D)*len(E)*len(F)
    return ampfunc, doms, thresh,pr,ainds,maps,numsets

def getSigmas(doms,thresh,amp,pr,ainds,maps):
    '''
    Find the sigma bounds in each regular domain.

    '''
    sigs = []
    midpts = np.mean(doms,2)
    for i in range(doms.shape[0]):
        comp = (midpts[i,:] > thresh).astype(int) # compare domain midpts to thresholds
        s=[]
        for j,a in enumerate(ainds):
            bmap = tuple( comp[j][a] ) # get the binary map for target j
            for k,m in enumerate(maps[j]): # get the index of binary map; this method is slightly faster than k = maps[j].index(bmap)
                if m == bmap:
                    s.append(amp[j][k]+pr[j]) # calculate sigma (is the focal point also if decay rates are 1)
                    break
        sigs.append(s)
    return sigs

def getSigBox(sigs,doms):
    sigboxes = []
    for s in sigs:
        sig = np.array(s)
        inds = np.nonzero(np.all((sig - doms[:,:,0])*(sig-doms[:,:,1]) < 0,1))[0]
        if len(inds)==1:
            sigboxes.append(inds[0])
        elif len(inds) == 0:
            return None
    return tuple(sigboxes)

def paramScan(ampfunc, doms, thresh,pr,ainds,maps,A=None,B=None,C=None,D=None,E=None,F=None):
    '''
    Scan across all parameter sets and calculate the sigma values and the location (domain) 
    of each sigma value.

    '''
    params = []
    allsigs = []
    sigboxes = []
    for p in itertools.product(A,B,C,D,E,F):
        amps = ampfunc(*p)
        sigs = getSigmas(doms,thresh,amps,pr,ainds,maps)
        sb = getSigBox(sigs,doms)
        if sb not in sigboxes and sb: #sb could be None
            params.append(p)
            allsigs.append(sigs)
            sigboxes.append(sb)
    return zip(params, allsigs, sigboxes)

def findMinimalParamSets(model=test4DExample1,modelargs = {'A':np.arange(0.5,8.25,2),'B':np.arange(0.5,2.75,1),'C':np.arange(0.5,2.75,1),'D':np.arange(0.5,2.75,1),'E':np.arange(0.5,5,1),'F':np.arange(0.25,1,0.25)}):
    ampfunc, doms, thresh,pr,ainds,maps, numsets= model(**modelargs)
    return paramScan(ampfunc, doms, thresh,pr,ainds,maps,**modelargs), numsets

if __name__ == '__main__':
    paramsets, numsets = findMinimalParamSets()
    for p, s, b in paramsets:
        print(p); print(b); # print(s); print('       ')
    print('Total number of parameter sets with focal point collection in a unique set of domains: {0}'.format(len(paramsets)))
    print('Total number of parameter sets tested: {0}'.format(numsets))






