import numpy as np
import itertools

def makeWalls(thresh,maxvals):
    '''
    Construct all hyperplanes, where xi equals one of its 
    threshold values and no other xj is at threshold. 
    Assume N variables total. Then each hyperplane will be 
    rectangular in N-1 dimensional space with side lengths 
    w1 by w2 by ... by wi-1 by wi+1 by ... by wN. 

    thresh is the NxN parameter array containing the thresholds.
    maxvals is a user-supplied list of length N of the maximum 
    value allowed for each variable. Each value in maxvals should
    exceed the highest threshold for the corresponding variable.

    The output is the list of compact boxes inside the 
    hyperplanes, the number of which is determined by the 
    dimension of thresh and the number of unique threshold 
    values in each column.
    
    Each hyperplane will have one variable that is
    constant at a threshold. The other variables will be 
    bounded between two of their threshold values, or between
    zero and their lowest threshold, or between their highest
    threshold and maxvals[k]. 

    '''
    N = thresh.shape[0]
    # Find unique thresholds. The first threshold for each
    # variable will almost always be the placeholder 0, but
    # that's not guaranteed. I am removing it as a design choice,
    # even though some calculations need it. This is because
    # other calculations _don't_ need it, so I either have to
    # add it and remove it later, or remove it and add it 
    # later, or check if it's there in both calculations.
    uniqthresh = []
    for k in range(N):
        u = np.unique(thresh[:,k])
        if u[0] == 0:
            uniqthresh.append( u[1:] )
        else:
            uniqthresh.append( u )
    # make the chunks for the boxes 
    chunks = []
    for k,u in enumerate(uniqthresh):
        mins = np.concatenate((np.array([0]), u))
        maxs = np.concatenate((u, np.array([maxvals[k]])))
        chunks.append( [(m,maxs[k]) for k,m in enumerate(mins)])
    # assemble chunks into hyperplane boxes
    indices = [range(len(_c)) for _c in chunks]
    hyperplanes = []
    for k,u in enumerate(uniqthresh):
        # excise var at threshold
        lessk = range(N)
        lessk.remove(k)
        subinds = indices[:k] + indices[k+1:]
        # make all combinations of remaining chunks
        for p in itertools.product(*subinds):
            hp = [0]*N
            for j,i in enumerate(p):
                hp[lessk[j]] = chunks[lessk[j]][i]
            # combine with threshold values into hyperplane boxes
            for xt in u:
                hpxt = list(hp)
                hpxt[k] = (xt,xt)
                hyperplanes.append( hpxt )                        
    return hyperplanes

def getDomainsAndFocalPoints(thresh,amp,rep,dr,pr,maxvals):
    # for each source, collect all the halfway points 
    # between thresholds, including below the first and 
    # above the last thresholds
    dp = []
    for j in range(thresh.shape[1]):
        tl = list(np.unique(thresh[:,j])) + [maxvals[j]]
        if tl[0] != 0:
            tl = [0] + tl
        dp.append( [np.mean(tl[k:k+2]) for k in range(len(tl[:-1]))] )
    # find the midpoints of each domain
    doms = np.array(list(itertools.product(*dp)))
    # get the focal point for the midpoint of each domain
    fps = []
    for i in range(doms.shape[0]):
        up = (doms[i,:] > thresh)  #this is focal point code from BooleanMapForDB 
        A = amp*(up ^ rep) # without look-ahead because we're in a regular domain   
        fps.append( (A.sum(1) + pr)/dr ) # with the addition of constant production rates
    # return the midpoints of each domain and the focal points for the domains
    return doms, fps

def identifyWhiteWalls(walls,doms,fps,dr):
    # For each hyperplane, determine which domains are on either side,
    # then figure out if the focal points are the same on both sides.
    # If so, make the focal point of the hyperplane the same as the 
    # domains.
    # If not, identify if there is a white wall. (Can't handle black
    # walls yet.)
    whitewalls = []
    unidirwalls = []
    unidirfps = []
    for w in walls:
        # shift indices by 1 since 0 will mean failure
        possdoms = np.arange(1,doms.shape[0]+1) 
        tind = np.Inf
        for j,c in enumerate(w):
            if c[0] != c[1]:
                inds = np.logical_and( (doms[:,j]-c[0])>0, (c[1]-doms[:,j])>0 )
                possdoms = possdoms*inds
            elif c[0] == c[1]:
                tind = j
        # shift indices back so that the first entry (index=0) can be identified when needed
        possdoms -= 1 
        # get rid of all the domains that can't flank the hyperplane
        possdoms = possdoms[possdoms > -1] 
        # identify the threshold value
        th = w[tind][0] 
        # find the domain values that flank the threshold
        tdomvals = np.unique(doms[:,tind])
        lowerdom = np.max( tdomvals[(th-tdomvals) > 0] )
        upperdom = np.min( tdomvals[(tdomvals-th) > 0] )
        lofp = np.Inf
        hifp = np.Inf
        for i in possdoms:
            if doms[i,tind] == lowerdom:
                if lofp < np.Inf:
                    raise ValueError('FIXME: Every hyperplane has exactly two adjacent regular domains. There must be a bug.')
                lofp = fps[i]
            elif doms[i,tind] == upperdom:
                if hifp < np.Inf:
                    raise ValueError('FIXME: Every hyperplane has exactly two adjacent regular domains. There must be a bug.')
                hifp = fps[i]
        loflow = -dr[tind]*th + lofp[tind]
        hiflow = -dr[tind]*th + hifp[tind]
        if loflow < 0 and hiflow <= 0:
            #flow is unidirwalls toward lower domain
            unidirwalls.append( w )
            unidirfps.append( lofp )
        elif loflow >= 0 and hiflow > 0:
            #flow is unidirwalls toward upper domain
            unidirwalls.append( w )
            unidirfps.append( hifp )
        elif loflow < 0 and hiflow > 0:
            #we have a white wall
            whitewalls.append( w )
        else:
            raise ValueError("FIXME: The parameters of the system returned a black wall and we can't handle that yet.")
    return unidirwalls, unidirfps, whitewalls  

def getNextThresholdsAndSteadyStates(unidirwalls, unidirfps, thresh):
    allz = [0]*unidirfps[0].shape[0]
    next_threshs = []
    steadypts = []
    for k,fp in enumerate(unidirfps):
        # get possible thresholds
        h = unidirwalls[k]
        hpt = [np.mean(p) for p in h]
        possth = ( (hpt-thresh)*(fp-thresh) < 0 )*thresh
        # get the closest threshold to each coordinate
        nt = [0]*len(allz)
        for k in range(len(hpt)):
            if hpt[k] > fp[k]:
                nt[k] = possth[:,k].max()
            elif hpt[k] < fp[k] and np.any(possth[:,k]):
                nt[k] = possth[possth[:,k]>0,k].min()
        next_threshs.append( nt )
        if (nt == allz) and (list(fp) not in steadypts):
            steadypts.append( list(fp) )
    return next_threshs, steadypts

def constructVertices(unidirwalls,eps=0.001):
    '''
    Make a compact box inside each hyperplane that is bounded 
    away from the threshold values at the boundaries by eps*wj,
    where eps is a user-supplied value between 0 and 1,
    usually very small, and wj is the length of the side of
    the box associated with the jth variable.

    '''
    wallvertices = []
    for hp in unidirwalls:
        ind = [h[0]==h[1] for h in hp].index(1) #find which var is at a thresh
        subinds = range(len(hp))
        subinds.remove(ind)
        lens = []
        for s in subinds:
            lens.append( hp[s][1] - hp[s][0] )
        vertices = []
        for p in itertools.product([0,1],repeat=len(subinds)):
            pt = np.empty(len(subinds)+1)
            pt.fill(np.nan) #much faster than np.nan*np.ones(len(subinds)+1), using nan's to make bugs easier to catch
            pt[ind] = hp[ind][0] #fill in threshold value
            for i,k in enumerate(p):
                pt[subinds[i]] = hp[subinds[i]][k] + lens[i]*eps*((-1)**(k)) #fill either max or min adjusted by eps for every other var in the wall
            vertices.append(pt) 
        wallvertices.append(vertices) #save all pts in one hyperplane into one box
    return wallvertices

def getTraversalTimes(init,fp,next_threshs,dr):
    '''
    Find and return all times exp(-t*) to the next threshold in next_threshs. 
    
    next_threshs contains the thresholds closest to (but not equal to) each 
    coordinate of init which must be crossed to reach the corresponding 
    coordinate of fp. A value of 0 in next_threshs is a placeholder that 
    means no such intervening threshold exists. The zeros are skipped in the 
    following algorithm, as they yield meaningless (complex) traversal times.

    Calculate the times exp(-t*) of every potential threshold crossing using 
    the solution to the linear ODEs x' = -dr*x + fp. The smallest time t* has 
    the maximal exp(-t*), which is the return value. 

    '''
    expminusT = []
    for k,i in enumerate(init):
        xT = next_threshs[k]
        if xT > 0:
            expminusT.append( (( xT - fp[k] ) / ( i - fp[k] ))**(1./dr[k]) )
    if expminusT == []:
        return np.array([0])  # handle steady states
    else:
        return expminusT

def mapOnePointToMultipleHyperplanes(pt,fp,next_threshs,dr):
    expminusT = getTraversalTimes(pt,fp,next_threshs,dr)
    allnextsteps = []
    for eT in expminusT:
        allnextsteps.append( fp + (pt-fp)*(eT**dr) )
    ind = np.nonzero(expminusT == max(expminusT))[0][0]
    shorteststep = allnextsteps[ind]
    return shorteststep, allnextsteps

def mapManyPointsToMultipleHyperplanes(wallverts,fp,next_threshs,dr):
    '''
    wallverts is a list of numpy arrays of the vertices in 
    N-dimensional space denoting points on one wall.
    As such, they all have the same possibilities for the
    next threshold (next_threshs array) and they
    all have the same focal point (in fp).
    dr is the array of decay rates for each coordinate.

    This function maps each vertex in wallverts from its 
    current location to all of the nonzero threshold 
    hyperplanes in next_threshs according to an underlying 
    dynamical system model.

    For details of the computation, see BooleanMapForDB.takeAStep.

    '''
    mappedpts = []
    mappedptsallsteps = []
    for w in wallverts:
        s,a = mapOnePointToMultipleHyperplanes(w,fp,next_threshs,dr)
        mappedpts.append( s )
        mappedptsallsteps.append( a )
    return mappedpts, mappedptsallsteps

def makeParameterArrays(sources,targets,thresholds,amplitudes,productionrates,decayrates,repressors):
    '''
    Put model parameters into square arrays, where the column 
    index indicates the source variable and the row index 
    indicates the target variable.

    The outputs thresh, amp, and rep are len(sources) x len(sources)
    arrays with threshold values, amplitudes, and repressor 
    identities filled in between the appropriate source-target 
    interactions. All other array values are zero.

    '''
    N = len(sources)
    thresh = np.zeros((N,N))
    amp = np.zeros((N,N))
    for j,targ in enumerate(targets): #j is index of source
        for k,t in enumerate(targ):
            i = sources.index(t) #i is index of target
            thresh[i,j] = thresholds[j][k]
            amp[i,j] = amplitudes[j][k]
    rep = np.zeros((N,N))
    for r in repressors:
        j = sources.index(r[0])
        i = sources.index(r[1])
        rep[i,j] = 1
    dr = np.array(decayrates)
    pr = np.array(productionrates)
    return thresh, amp, rep.astype(int), dr, pr

def runModel(thresh,amp,rep,dr,pr,maxvals):
    walls = makeWalls(thresh,maxvals)
    domains, focalpts = getDomainsAndFocalPoints(thresh,amp,rep,dr,pr,maxvals)
    unidirwalls, unidirfps, whitewalls = identifyWhiteWalls(walls,domains,focalpts,dr)
    next_threshs, steadypts = getNextThresholdsAndSteadyStates(unidirwalls, unidirfps, thresh)
    wallvertices = constructVertices(unidirwalls)
    mappedpts = []
    allsteps = []
    for k,w in enumerate(wallvertices):
        mp, mpa = mapManyPointsToMultipleHyperplanes(w,unidirfps[k],next_threshs[k],dr)
        mappedpts.append( mp )
        allsteps.append( mpa )
    return mappedpts, allsteps

if __name__ == '__main__':
    pass
    # # Bridget's example
    # sources = ['x','y1','y2','z']
    # targets = [['x','y1','z'],['y2'],['x','z'],['x']]
    # thresholds = [[0.25,0.5,0.75],[0.5],[0.5,0.5],[0.5]]
    # amplitudes = [[0.5,1.0,1.0],[1.0],[1.0,1.0],[1.0]]
    # decayrates = [1.0,0.5,0.5,0.5]
    # repressors = [('z','x')]
    # thresh,amp,rep,dr = makeModel(sources,targets,thresholds,amplitudes,decayrates,repressors)
    # maxvals = [1.0]*len(sources)
    # doms, fps = getDomainsAndFocalPoints(thresh,amp,rep,dr,maxvals)
    # print(len(doms))
    # # print(doms)
    # # print(fp)
    # hyperplanes = makeHyperplanes(thresh,maxvals)
    # print(len(hyperplanes))
    # # for h in hyperplanes:
    # #     formattedh = ['({0:.3f}, {1:.3f})'.format(tup[0],tup[1]) for tup in h]
    # #     print(str(formattedh).translate(None, "'"))
    # # 2D example
    # sources = ['x','z']
    # targets = [['x','z'],['x']]
    # thresholds = [[0.5,0.75],[0.5]]
    # amplitudes = [[1,0.5],[0.25]]
    # decayrates = [1.0,1.0]
    # repressors = [('z','x')]
    # thresh,amp,rep,dr = makeModel(sources,targets,thresholds,amplitudes,decayrates,repressors)
    # maxvals = [1.0]*len(sources)
    # doms, fps = getDomainsAndFocalPoints(thresh,amp,rep,dr,maxvals)
    # # print(len(doms))
    # # print(doms)
    # # print(fp)
    # hyperplanes = makeHyperplanes(thresh,maxvals)
    # # print(len(hyperplanes))
    # # for h in hyperplanes:
    # #     formattedh = ['({0:.3f}, {1:.3f})'.format(tup[0],tup[1]) for tup in h]
    # #     print(str(formattedh).translate(None, "'"))
    # unidirwalls, unidirfps, blackwalls, blackfps, whitewalls = identifyBlackWhiteWalls(hyperplanes,doms,fps,dr)
    # print(unidirwalls)
    # print(blackwalls)
    # print(whitewalls)
