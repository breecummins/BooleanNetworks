import numpy as np
import itertools

def makeParameterArrays(variables, affectedby, thresholds, productionrates):
    '''
    Put model parameters into square arrays, where the column 
    index indicates the source variable and the row index 
    indicates the target variable.

    The outputs thresh, lamp, uamp, and rep are len(variables) x len(variables)
    arrays with threshold values, amplitudes, and repressor 
    identities filled in between the appropriate source-target 
    interactions. All other array values are zero. The output
    pr is simply the list productionrates converted to an array.

    '''
    N = len(variables)
    thresh = np.zeros((N,N))
    ainds = []
    for j,a in enumerate(affectedby): #j is index of target
        at = []
        for k,t in enumerate(a):
            i =  variables.index(t) #i is index of source
            at.append(i)
            thresh[j,i] = thresholds[j][k]
        ainds.append(at)
    pr = np.array(productionrates)
    return thresh, ainds, pr

def getDomains(thresh,lowerbounds,upperbounds):
    '''
    Find the domain bounds for each 
    regular domain (area between thresholds).

    '''
    dp = []
    for j in range(thresh.shape[1]):
        tl = list(np.unique(thresh[:,j])) + [upperbounds[j]]
        if tl[0] != 0:
            tl = [0] + tl
        tl[0] = tl[0] + lowerbounds[j]
        dp.append( [tl[k:k+2] for k in range(len(tl[:-1]))] )
    # return the bounds for each regular domain 
    return np.array(list(itertools.product(*dp)))

def getSigmas(doms,thresh,lamp,uamp,pr,ainds,maps):
    '''
    Find the sigma bounds in each regular domain. Note that sigma is *not* dependent on decay rate. 
    Sigma is the same as the focal point if the decay rates are all 1.

    '''
    lsigs = []
    usigs = []
    for i in range(doms.shape[0]):
        ls=[]
        us=[]
        for j,a in enumerate(ainds):
            bmap = tuple( (np.mean(doms[i,:,:],1) > thresh[j,:]).astype(int)[a] ) # get the binary map for target j
            for k,m in enumerate(maps[j]):
                if m == bmap:
                    ls.append(lamp[j][k]+pr[j])
                    us.append(uamp[j][k]+pr[j])
                    break
        lsigs.append(ls)
        usigs.append(us)
    return lsigs,usigs

