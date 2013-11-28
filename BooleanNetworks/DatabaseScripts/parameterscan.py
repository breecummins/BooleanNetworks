import numpy as np
import makeboxes
import itertools

def test4DExample1(A=np.arange(0.05,12.25,0.5),B=np.arange(0.05,12.25,0.5),C=np.arange(0.05,12.25,0.5),D=np.arange(0.05,12.25,0.5),E=np.arange(0.05,12.25,0.5),F=np.arange(0.05,1,0.25)):
    '''
    Create all parameter sets given as ranges in the arguments.

    '''
    # define the interactions between variables
    variables = ['x','y1','y2','z']
    affectedby = [['x','y2','z'],['x'],['y1'],['x']]
    # give the thresholds for each interaction
    thresholds = [[2,1,1],[3],[1],[1]]
    # give the maps and amplitudes of each interaction (upper and lower bounds for parameter search)
    maps = [[(0,0,0),(1,0,0),(0,1,0),(1,1,0),(0,0,1),(1,0,1),(0,1,1),(1,1,1)],[(0,),(1,)],[(0,),(1,)],[(0,),(1,)]]
    ampfunc = lambda a,b,c,d,e,f: [[0,e,a,a+e,0,f*e,f*a,(a+e)*f],[0,c],[0,d],[0,b]]
    # give the natural decay rates of the species (upper and lower bounds for parameter search)
    lowerdecayrates = [-1,-1,-1,-1]
    upperdecayrates = [-1,-1,-1,-1] #[-0.5,-0.5,-0.5]
    # give the endogenous production rates. 
    productionrates = [0.1,0.5,0.5,0.5] 
    # get upper and lower bounds
    bigamps = ampfunc(A[-1],B[-1],C[-1],D[-1],E[-1],F[-1])
    upperbounds = 1.1*((np.array([np.max(u) for u in bigamps]) + np.array(productionrates)) / np.abs(np.array(upperdecayrates))) 
    lowerbounds = np.zeros(upperbounds.shape)
    # make domains
    thresh,ainds,pr = makeboxes.makeParameterArrays(variables, affectedby, thresholds, productionrates)
    doms = makeboxes.getDomains(thresh,lowerbounds,upperbounds)
    numsets = len(A)*len(B)*len(C)*len(D)*len(E)*len(F)
    return ampfunc, doms, thresh,pr,ainds,maps,numsets

def getSigBox(sigs,doms):
    sigboxes = []
    for s in sigs:
        sig = np.array(s)
        for d in range(doms.shape[0]):
            if np.all(sig > doms[d,:,0]) and np.all(sig < doms[d,:,1]):
                sigboxes.append(d)
                break
    return tuple(sigboxes)

def getSigBoxNew(sigs,doms):
    sigboxes = []
    for s in sigs:
        sig = np.array(s)
        inds = np.nonzero(np.all((sig - doms[:,:,0])*(sig-doms[:,:,1]) < 0,1))[0]
        if len(inds)==1:
            sigboxes.append(inds[0])
        elif len(inds) == 0:
            return None
    return tuple(sigboxes)


def getSigBoxWorse(sigs,doms):
    sigboxes = []
    for sig in sigs:
        for d in range(doms.shape[0]):
             if sum([sig[j] > doms[d,j,0] and sig[j] < doms[d,j,1] for j in range(len(sig))]) == len(sig):
                sigboxes.append(d)
                break
    return tuple(sigboxes)

def paramScanNew(ampfunc, doms, thresh,pr,ainds,maps,A=None,B=None,C=None,D=None,E=None,F=None):
    '''
    Scan across all parameter sets and calculate the sigma values and the location (domain) 
    of each sigma value.

    '''
    params = []
    sigs = []
    sigboxes = []
    for p in itertools.product(A,B,C,D,E,F):
        amps = ampfunc(*p)
        lsigs,usigs = makeboxes.getSigmas(doms,thresh,amps,amps,pr,ainds,maps)
        sb = getSigBoxNew(usigs,doms)
        if sb not in sigboxes and sb: #sb could be None
            params.append(p)
            sigs.append(usigs)
            sigboxes.append(sb)
    return zip(params, sigs, sigboxes)

def paramScan(ampfunc, doms, thresh,pr,ainds,maps,A=None,B=None,C=None,D=None,E=None,F=None):
    '''
    Scan across all parameter sets and calculate the sigma values and the location (domain) 
    of each sigma value.

    '''
    paramsets = list(itertools.product(A,B,C,D,E,F))
    sigs = []
    sigboxes = []
    for p in paramsets:
        amps = ampfunc(*p)
        lsigs,usigs = makeboxes.getSigmas(doms,thresh,amps,amps,pr,ainds,maps)
        sigs.append(usigs)
        sigboxes.append(getSigBox(usigs,doms))
    return zip(paramsets, sigs, sigboxes)

def paramsWithUniqSigBoxes(params_sigboxes):
    '''
    Find all parameter sets corresponding to unique collections of sigma locations.

    '''
    usb = []
    usm = []
    ups = []
    for p,s,b in params_sigboxes:
        if b not in usb and b: # b could be None
            usb.append(b)
            usm.append(s)
            ups.append(p)
    return zip(ups, usm, usb)

def findMinimalParamSetsNew(model=test4DExample1,modelargs = {'A':np.arange(0.5,8.25,3),'B':np.arange(0.5,2.75,1),'C':np.arange(0.5,2.75,1),'D':np.arange(0.5,2.75,1),'E':np.arange(0.5,2.75,1),'F':np.arange(0.25,1,0.5)}):
    ampfunc, doms, thresh,pr,ainds,maps, numsets= model(**modelargs)
    return paramScanNew(ampfunc, doms, thresh,pr,ainds,maps,**modelargs), numsets

def findMinimalParamSets(model=test4DExample1,modelargs = {'A':np.arange(0.5,8.25,3),'B':np.arange(0.5,2.75,1),'C':np.arange(0.5,2.75,1),'D':np.arange(0.5,2.75,1),'E':np.arange(0.5,2.75,1),'F':np.arange(0.25,1,0.5)}):
    ampfunc, doms, thresh,pr,ainds,maps, numsets= model(**modelargs)
    params_sigboxes = paramScan(ampfunc, doms, thresh,pr,ainds,maps,**modelargs)
    uniqparamsets = paramsWithUniqSigBoxes(params_sigboxes)
    return uniqparamsets, numsets

if __name__ == '__main__':
    paramsets, numsets = findMinimalParamSets()
    for p, s, b in paramsets:
        print(p); print(b); print(s); print('       ')
    print('Total number of parameter sets with focal point collection in a unique set of domains: {0}'.format(len(paramsets)))
    print('Total number of parameter sets tested: {0}'.format(numsets))

    paramsetsnew, numsets = findMinimalParamSetsNew()
    for p, s, b in paramsetsnew:
        print(p); print(b); print(s); print('       ')
    print('Total number of parameter sets with focal point collection in a unique set of domains: {0}'.format(len(paramsetsnew)))
    print('Total number of parameter sets tested: {0}'.format(numsets))

    diffs = []
    for p in paramsets:
        if p not in paramsetsnew:
            diffs.append(p)

    for d in diffs:
        print(d[0])
    print('Total number of param sets in old but not new: {0}'.format(len(diffs)))







