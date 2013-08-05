import numpy as np
import BooleanMapForDB as BDB
import itertools

def makeHyperplanes(thresh,maxvals,eps=0.0):
    '''
    Construct all hyperplanes, where xi equals one of its 
    threshold values and no other xj is at threshold. 
    Assume N variables total. Then each hyperplane will be 
    rectangular in N-1 dimensional space with side lengths 
    w1 by w2 by ... by wi-1 by wi+1 by ... by wN. 

    Make a compact box inside each hyperplane that is bounded 
    away from the threshold values at the boundaries by eps*wj,
    where eps is a user-supplied value between 0 and 1,
    usually very small, and wj is the length of the side of
    the box associated with the jth variable.

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
        lens = maxs - mins
        mins = mins + eps*lens
        maxs = maxs - eps*lens
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

def constructBoxes(hyperplanes):
    hpboxes = []
    for hp in hyperplanes:
        ind = [h[0]==h[1] for h in hp].index(1) #find which var is at a thresh
        subinds = range(len(hp))
        subinds.remove(ind)
        vertices = []
        for p in itertools.product([0,1],repeat=len(subinds)):
            pt = np.empty(len(subinds)+1)
            pt.fill(np.nan) #much faster than np.nan*np.ones(len(subinds)+1), using nan's to make bugs easier to catch
            pt[ind] = hp[ind][0] #fill in threshold value
            for i,k in enumerate(p):
                pt[i] = hp[i][k] #fill either max or min for every other var in the hyperplane
            vertices.append(pt) 
        hpboxes.append(vertices) #save all pts in one hyperplane into one box
    return hpboxes

def getDomainsAndFocalPoints(thresh,amp,rep,dr,maxvals):
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
    # FIXME: add constant production rates
    fps = []
    prev = np.zeros(thresh[0,:].shape)
    for i in range(doms.shape[0]):
        fps.append( BDB.getFocalPoint(doms[i,:],thresh,amp,rep,dr,prev) )
    # return the midpoints of each domain and the focal points for the domains
    return doms, fps

def identifyWhiteWalls(hyperplanes,doms,fps,dr):
    # For each hyperplane, determine which domains are on either side,
    # then figure out if the focal points are the same on both sides.
    # If so, make the focal point of the hyperplane the same as the 
    # domains.
    # If not, identify if there is a white wall. (Can't handle black
    # walls yet.)
    whitewalls = []
    unidirectional = []
    unidirfps = []
    for h in hyperplanes:
        # shift indices by 1 since 0 will mean failure
        possdoms = np.arange(1,doms.shape[0]+1) 
        hind = np.Inf
        for j,c in enumerate(h):
            if c[0] != c[1]:
                inds = np.logical_and( (doms[:,j]-c[0])>0, (c[1]-doms[:,j])>0 )
                possdoms = possdoms*inds
            elif c[0] == c[1]:
                hind = j
        # shift indices back so that the first entry (index=0) can be identified when needed
        possdoms -= 1 
        # get rid of all the domains that can't flank the hyperplane
        possdoms = possdoms[possdoms > -1] 
        # identify the threshold value
        th = h[hind][0] 
        # find the domain values that flank the threshold
        tdomvals = np.unique(doms[:,hind])
        lowerdom = np.max( tdomvals[(th-tdomvals) > 0] )
        upperdom = np.min( tdomvals[(tdomvals-th) > 0] )
        lofp = np.Inf
        hifp = np.Inf
        for i in possdoms:
            if doms[i,hind] == lowerdom:
                if lofp < np.Inf:
                    raise ValueError('FIXME: Every hyperplane has exactly two adjacent regular domains. There must be a bug.')
                lofp = fps[i]
            elif doms[i,hind] == upperdom:
                if hifp < np.Inf:
                    raise ValueError('FIXME: Every hyperplane has exactly two adjacent regular domains. There must be a bug.')
                hifp = fps[i]
        loflow = -dr[hind]*th + lofp[hind]
        hiflow = -dr[hind]*th + hifp[hind]
        if loflow < 0 and hiflow <= 0:
            #flow is unidirectional toward lower domain
            unidirectional.append( h )
            unidirfps.append( lofp )
        elif loflow >= 0 and hiflow > 0:
            #flow is unidirectional toward upper domain
            unidirectional.append( h )
            unidirfps.append( hifp )
        elif loflow < 0 and hiflow > 0:
            #we have a white wall
            whitewalls.append( h )
        # elif loflow == 0 and hiflow == 0:
        #     # We have a black wall and the flow will never leave.
        #     blackwalls.append( h )
        #     # Assign the focal point/steady point to be the average of the focal points on either side
        #     blackfps.append( np.mean([lofp,hifp]) )
        else:
            raise ValueError("FIXME: The parameters of the system returned a black wall and we can't handle that yet.")
    return unidirectional, unidirfps, whitewalls  

def getNextThresholds(unidirectional, unidirfps, thresh):
    next_threshs = []
    for k,fp in enumerate(unidirfps):
        # get possible thresholds
        h = unidirectional[k]
        hpt = [np.mean(p) for p in h]
        pt = ( (hpt-thresh)*(fp-thresh) < 0 )*thresh
        # get the closest threshold to each coordinate
        nt = np.zeros(fp.shape)
        for k in range(len(hpt)):
            if hpt[k] > fp[k]:
                nt[k] = pt[:,k].max()
            elif hpt[k] < fp[k] and np.any(pt[:,k]):
                nt[k] = pt[pt[:,k]>0,k].min()
        next_threshs.append( nt )
    return next_threshs


def getMinsMaxs(mappedpts,thresh):
    pass

def outerApprox(mins,maxs,boxes):
    pass

def subdivideBoxes(boxes):
    pass

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
    return expminusT

def mapOnePointToMultipleHyperplanes(pt,fp,next_threshs,dr):
    expminusT = getTraversalTimes(pt,fp,next_threshs,dr)
    allnextsteps = []
    for eT in expminusT:
        allnextsteps.append( fp + (pt-fp)*(eT**dr) )
    ind = np.nonzero(expminusT == min(expminusT))[0]
    shorteststep = allnextsteps[ind]
    return shorteststep, allnextsteps


def mapManyPointsToMultipleHyperplanes(vertices,thresh,amp,rep,dr,previous):
    '''
    vertices is a list of numpy arrays of points in 
    N-dimensional space denoting current location.
    previous is a list of numpy arrays of points in 
    N-dimensional space denoting the location of each
    vertex on the previous hyperplane. The other inputs 
    are model parameter arrays produced by makeModel.

    Each point in vertices is on a hyperplane where
    one of the variables is fixed at a threshold value.
    This function maps each vertex from its current
    hyperplane to the next hyperplane where a 
    variable has achieved threshold according to 
    an underlying dynamical system model.

    For details of the computation, see BooleanMapForDB.takeAStep.

    '''
    mappedpts = []
    for k,v in enumerate(vertices):
        mappedpts.append( BDB.takeAStep(v,thresh,amp,rep,dr,previous[k]) )
    return mappedpts

def runModel(thresh,amp,rep,dr,maxvals):
    hp = makeHyperplanes(thresh,maxvals)
    initboxes = constructBoxes(hp)
    s = initboxes[0][0].shape
    previous1 = [np.zeros(s) for _ in range(len(initboxes[0]))] 
    M = max(maxvals)
    previous2 = [p+M for p in previous1] 
    boxes = []
    for b in initboxes:
        mappedpts = mapManyPoints(b,thresh,amp,rep,dr,previous1) #start below thresh
    #now translate into outer approx
    #then decide where we should subdivide

def makeModel(sources,targets,thresholds,amplitudes,decayrates,repressors):
    '''
    See documentation for BooleanMapForDB.modelTrajectory.

    '''
    dr = np.array(decayrates)
    thresh,amp,rep = BDB.makeParameterArrays(sources,targets,thresholds,amplitudes,repressors)
    return thresh,amp,rep,dr


if __name__ == '__main__':
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
    # unidirectional, unidirfps, blackwalls, blackfps, whitewalls = identifyBlackWhiteWalls(hyperplanes,doms,fps,dr)
    # print(unidirectional)
    # print(blackwalls)
    # print(whitewalls)
    # 3D example
    sources = ['x','y','z']
    targets = [['x','y','z'],['x','z'],['x']]
    thresholds = [[0.25,0.5,0.75],[0.5,0.5],[0.5]]
    amplitudes = [[0.6,1.0,1.0],[1.0,1.0],[1.0]]
    decayrates = [1.0,0.5,0.5]
    repressors = [('z','x')]
    thresh,amp,rep,dr = makeModel(sources,targets,thresholds,amplitudes,decayrates,repressors)
    maxvals = [2.0,3.0,4.0]
    doms, fps = getDomainsAndFocalPoints(thresh,amp,rep,dr,maxvals)
    print(len(doms))
    # print(doms)
    # print(fp)
    hyperplanes = makeHyperplanes(thresh,maxvals)
    print(len(hyperplanes))
    # for h in hyperplanes:
    #     formattedh = ['({0:.3f}, {1:.3f})'.format(tup[0],tup[1]) for tup in h]
    #     print(str(formattedh).translate(None, "'"))
    unidirectional, unidirfps, whitewalls = identifyWhiteWalls(hyperplanes,doms,fps,dr)
    next_threshs = getNextThresholds(unidirectional, unidirfps, thresh)
    print("White walls: {0}".format(whitewalls))
    for k,u in enumerate(unidirectional):
        formattedh = ['({0:.3f}, {1:.3f})'.format(tup[0],tup[1]) for tup in u]
        print(str(formattedh).translate(None, "'"))
        print("Focal point: {0}".format(unidirfps[k]))
        print("Next hyperplanes: {0}".format(next_threshs[k]))
    specpt = np.array([0.4,0.5,0.7])
    fp = unidirfps[14]
    nt = next_threshs[14]
    shortest, allsteps = mapOnePointToMultipleHyperplanes(specpt,fp,nt,dr)
    print(shortest)
    print(allsteps)
