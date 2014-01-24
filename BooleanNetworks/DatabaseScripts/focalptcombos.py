import numpy as np, itertools, inspect

def example3D():
    # define the interactions between variables
    variables = ['x','y','z']
    affectedby = [['x','y','z'],['x'],['x']]
    # give the thresholds for each interaction
    thresholds = [[2,1,1],[3],[1]]
    # give the maps and amplitudes of each interaction (upper and lower bounds for parameter search)
    maps = [[(0,0,0),(0,0,1),(0,1,0),(0,1,1),(1,0,0),(1,0,1),(1,1,0),(1,1,1)],[(0,),(1,)],[(0,),(1,)]]    
    ampfunc = lambda f1,f2,f3,f4,f6,f7,f8,f9: [[f1,f2,f3,f3*f2/f1,f4,f4*f2/f1,f3+f4-f1,(f3+f4-f1)*f2/f1],[f6,f7],[f8,f9]]
    indepparams = [5,2,2]
    # fix upper and lower bounds
    upperbounds = [10.,5.,5.] 
    lowerbounds = -.25*np.ones(3)
    # Make constraints. the numbers below are thresholds: f2 < min(f1,Txx), f5 > Txx, f6 < Ty, f7 > Ty, f8 < Tz, f9 > Tz
    constraints = (lambda f1,f2,f3,f4,f5: f2 < min(f1,2) and f1 < min(f3,f4) and f5 > max(2,max(f3,f4)), lambda f6,f7: f6 < 1 and f7 > 1, lambda f8,f9: f8 < 1 and f9 > 1)
    return variables, affectedby, thresholds, maps, ampfunc, lowerbounds, upperbounds, constraints,indepparams


def makeParameterArrays(variables, affectedby, thresholds):
    '''
    Put model parameters into square arrays, where the column 
    index indicates the source variable and the row index 
    indicates the target variable.

    The outputs thresh, lamp, uamp, and rep are len(variables) x len(variables)
    arrays with threshold values, amplitudes, and repressor 
    identities filled in between the appropriate source-target 
    interactions. All other array values are zero. 

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
    return thresh, ainds

def getDomains(thresh,lowerbounds,upperbounds):
    '''
    Find the domain bounds for each 
    regular domain (area between thresholds).
    Find the midpt way between each pair of 
    thresholds.

    '''
    dp = []
    fpvals = []
    for j in range(thresh.shape[1]):
        tl = list(np.unique(thresh[:,j])) + [upperbounds[j]]
        if tl[0] != 0:
            tl = [0] + tl
        tl[0] = tl[0] + lowerbounds[j]
        dp.append( [tl[k:k+2] for k in range(len(tl[:-1]))] )
        fpvals.append([np.mean([tl[i],tl[i+1]]) for i in range(len(tl)-1)])
    # return the bounds for each regular domain and the threshold midpts
    return np.array(list(itertools.product(*dp))), fpvals

def getfpinds(doms,thresh,ainds,maps):
    '''
    Get the domain index for each focal point.

    '''
    fpinds = []
    for i in range(doms.shape[0]):
        fps = []
        for j,a in enumerate(ainds):
            bmap = tuple( (np.mean(doms[i,:,:],1) > thresh[j,:]).astype(int)[a] ) # get the binary map for target j
            for k,m in enumerate(maps[j]):
                if m == bmap:
                    fps.append(k)
                    break
        fpinds.append(fps)
    return fpinds

def getFocalPtCombos(inputfunc=example3D):  
    # get inputs
    variables, affectedby, thresholds, maps, ampfunc, lowerbounds, upperbounds, constraints, indepparams = inputfunc()
    # make domains
    thresh,ainds = makeParameterArrays(variables, affectedby, thresholds)
    doms, fpvals = getDomains(thresh,lowerbounds,upperbounds)
    # make focal point permutations with replacement
    fpcombos=[]
    for j,f in enumerate(fpvals):
        fp=[]
        for c in itertools.combinations_with_replacement(f,indepparams[j]):
            for p in itertools.permutations(c,len(c)):
                if constraints[j](*p):
                    fp.append(p)
        fpcombos.append(list(set(fp)))
    # make all products of acceptable focal point permutations
    fpparams = list(itertools.product(*fpcombos))
    # check the dependent focal points
    ptup = tuple()
    for f in fpparams:
        for v in f:
            ptup += v
    amps = ampfunc(*ptup)
    print(amps)
    return fpparams


if __name__ == '__main__':
    fpparams = getFocalPtCombos()
    print(fpparams)
