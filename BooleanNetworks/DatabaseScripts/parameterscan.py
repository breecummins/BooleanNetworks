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
    # make parameter sets
    paramsets = list(itertools.product(A,B,C,D,E,F))
    print('Total number of parameter sets to be tested: {0}'.format(len(paramsets)))
    return paramsets, ampfunc, doms, thresh,pr,ainds,maps

def getSigBox(sigs,doms):
    sigboxes = []
    for s in sigs:
        sig = np.array(s)
        for d in range(doms.shape[0]):
            if np.all(sig > doms[d,:,0]) and np.all(sig < doms[d,:,1]):
                sigboxes.append(d)
                break
    return tuple(sigboxes)

def paramScan(paramsets, ampfunc, doms, thresh,pr,ainds,maps):
    '''
    Scan across all parameter sets and calculate the sigma values and the location (domain) 
    of each sigma value.

    '''
    params_sigboxes = []
    for p in paramsets:
        amps = ampfunc(*p)
        lsigs,usigs = makeboxes.getSigmas(doms,thresh,amps,amps,pr,ainds,maps)
        params_sigboxes.append((p,getSigBox(usigs,doms)))
    return params_sigboxes

def paramsWithUniqSigBoxes(params_sigboxes):
    '''
    Find all parameter sets corresponding to unique collections of sigma locations.

    '''
    usb = []
    ups = []
    for p,b in params_sigboxes:
        if b not in usb:
            usb.append(b)
            ups.append(p)
    return ups

def findMinimalParamSets(model=test4DExample1,modelargs = {'A':np.arange(0.5,8.25,1),'B':np.arange(0.5,2.75,1),'C':np.arange(0.5,2.75,1),'D':np.arange(0.5,2.75,1),'E':np.arange(0.5,5,1),'F':np.arange(0.25,1,0.25)}):
    paramsets, ampfunc, doms, thresh,pr,ainds,maps = model(**modelargs)
    params_sigboxes = paramScan(paramsets, ampfunc, doms, thresh,pr,ainds,maps)
    uniqparamsets = paramsWithUniqSigBoxes(params_sigboxes)
    return uniqparamsets

if __name__ == '__main__':
    uniqparamsets = findMinimalParamSets()
    print(uniqparamsets)
    print('Total number of parameter sets with focal point collection in a unique set of domains: {0}'.format(len(uniqparamsets)))







