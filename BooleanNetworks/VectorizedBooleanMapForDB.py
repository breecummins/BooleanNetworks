import numpy as np
import itertools

def makeWalls(thresh,maxvals):
    '''
    Construct all walls, where xi equals one of its threshold 
    values and all other xj are between thresholds, or between
    zero and their smallest threshold, or between their largest
    threshold and maxvals[j]. If there are N variables total, 
    then each wall will be rectangular in N-1 dimensional space. 

    thresh is the NxN parameter array containing the thresholds
    for each variable.
    maxvals is a user-supplied list of length N of the maximum 
    value allowed for each variable. Each value in maxvals should
    exceed the highest threshold and highest steady state value
    for the corresponding variable.

    The output is the list of walls, the number of which is 
    determined by the dimension of thresh and the number of unique 
    threshold values in each column. Each wall is a list of 
    (min,max) tuples containing the minimum and maximum value of 
    each coordinate on that particular wall. The coordinate at 
    threshold will have the same min and max value. The other 
    coordinates will have a min value of one of their thresholds 
    (or zero) and a max value of another of their thresholds (or
    the user-supplied maximum value for that coordinate in maxvals).

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
    # find the regions between thresholds for each variable 
    chunks = []
    for k,u in enumerate(uniqthresh):
        mins = np.concatenate((np.array([0]), u))
        maxs = np.concatenate((u, np.array([maxvals[k]])))
        chunks.append( [(m,maxs[k]) for k,m in enumerate(mins)])
    # assemble chunks into walls
    indices = [range(len(_c)) for _c in chunks]
    walls = []
    for k,u in enumerate(uniqthresh):
        # excise var at threshold
        lessk = range(N)
        lessk.remove(k)
        subinds = indices[:k] + indices[k+1:]
        # make all combinations of nonthreshold chunks
        for p in itertools.product(*subinds):
            w = [0]*N
            for j,i in enumerate(p):
                w[lessk[j]] = chunks[lessk[j]][i]
            # combine with threshold values into walls
            for xt in u:
                wxt = list(w)
                wxt[k] = (xt,xt)
                walls.append( wxt )                        
    return walls

def getDomainsAndFocalPoints(thresh,amp,rep,dr,pr,maxvals):
    '''
    Find the midpoint and focal (target) point of each 
    regular domain (area between thresholds).

    '''
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
    return doms, fps

def identifyWhiteWalls(walls,doms,fps,dr):
    '''
    For each wall, determine which domains are on either side,
    then use the focal points on both sides to calculate the 
    direction of flow across the wall.
    
    If the flow is unidirectional, make the focal point of the 
    wall the same as downstream.

    If the flow is not unidirectional, then there is either a 
    white wall (which can be ignored) or a black wall. White 
    walls are returned in a list, and black walls throw an error.

    FIXME: We can handle black walls when there is no negative 
    self-regulation.

    '''
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
                possdoms = possdoms*inds # mask indices of possible flanking domains
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
                # if lofp < np.Inf:
                #     raise ValueError('FIXME: Every hyperplane has exactly two adjacent regular domains. There must be a bug.')
                lofp = fps[i]
            elif doms[i,tind] == upperdom:
                # if hifp < np.Inf:
                #     raise ValueError('FIXME: Every hyperplane has exactly two adjacent regular domains. There must be a bug.')
                hifp = fps[i]
        # calculate direction of flow on both sides of the wall
        loflow = -dr[tind]*th + lofp[tind]
        hiflow = -dr[tind]*th + hifp[tind]
        if loflow < 0 and hiflow < 0:
            #flow is unidirectional toward lower domain
            unidirwalls.append( w )
            unidirfps.append( lofp )
        elif loflow > 0 and hiflow > 0:
            #flow is unidirectional toward upper domain
            unidirwalls.append( w )
            unidirfps.append( hifp )
        elif loflow < 0 and hiflow > 0:
            #we have a white wall
            whitewalls.append( w )
        else:
            raise ValueError("FIXME: The parameters of the system returned a black wall and we can't handle that yet.")
    return unidirwalls, unidirfps, whitewalls  

def getNextThresholdsAndSteadyStates(unidirwalls, unidirfps, thresh):
    '''
    Identify the hyperplanes that each wall can map to. 
    The output next_threshs is a list of lists, with each 
    internal list consisting of the possible hyperplane 
    maps for that wall. 

    For example, next_threshs[j] = [0, 0, 1, 0.5] means that 
    the j-th wall can map to the hyperplane where the third 
    coordinate is at a threshold value of 1, or where the 
    fourth coordinate is at 0.5. Values of zero mean that 
    there is no map from wall j to hyperplanes of the first or 
    second coordinates. 

    Additionally, identify all the steady states of the system.
    The output steadypts is a list of lists, with each internal
    list indicating an asymptotically stable point in N-dimensional 
    space.

    '''
    allz = [0]*unidirfps[0].shape[0]
    next_threshs = []
    steadypts = []
    for k,fp in enumerate(unidirfps):
        # get the midpoint of the wall (the midpoint is representative of
        # the whole wall because the focal point is constant on the wall)
        w = unidirwalls[k]
        midpt = [np.mean(p) for p in w]
        # figure out which coordinates of the focal point and midpoint 
        # flank threshold values, use those thresholds as possibilities
        possth = ( (midpt-thresh)*(fp-thresh) < 0 )*thresh
        # get the closest threshold to each coordinate
        nt = [0]*len(allz)
        for k in range(len(midpt)):
            # choose the max thresh between the midpt and the fp if the midpt exceeds the fp
            if midpt[k] > fp[k]:
                nt[k] = possth[:,k].max() 
            # choose the min thresh > 0 between the midpt and the fp if the fp exceeds the midpt
            elif midpt[k] < fp[k] and np.any(possth[:,k]):
                nt[k] = possth[possth[:,k]>0,k].min()
        next_threshs.append( nt )
        # if no thresholds met the criteria, the focal point is a steady state
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
    Find and return all times exp(-T) to the next thresholds in next_threshs
    crossing using the solution to the linear ODEs x' = -dr*x + A, which is
    x_thresh = fp + (init - fp)*exp(-dr*T), where fp = A/dr.
    
    next_threshs contains the thresholds closest to (but not equal to) each 
    coordinate of init which must be crossed to reach the corresponding 
    coordinate of fp. A value of 0 in next_threshs is a placeholder that 
    means no such intervening threshold exists. In this case we set exp(-T)=0
    in the output, indicating infinite travel time.

    '''
    expminusT = []
    for k,i in enumerate(init):
        xT = next_threshs[k]
        if xT > 0:
            expminusT.append( (( xT - fp[k] ) / ( i - fp[k] ))**(1./dr[k]) )
        else:
            expminusT.append( 0 )
    return expminusT

def mapOnePointToMultipleHyperplanes(pt,fp,next_threshs,dr,wallsandsteadypts):
    '''
    Map the point pt to all possible hyperplanes indicated in next_threshs.
    Return the shortest step (the true step), any other steps that arise
    because there is more than one possible map, and the indices of the 
    walls that are mapped to. This last is important because some points
    exist on more than one wall. 

    On rare occasions, a point will map to two hyperplanes simultaneously.
    In this case, there is still one shortest step, but there will be two
    or more wall indices for the mapped point.

    '''
    allnextsteps = []
    expminusT = getTraversalTimes(pt,fp,next_threshs,dr)
    for eT in expminusT:
        allnextsteps.append( fp + (pt-fp)*(eT**dr) )
    ind = np.nonzero(expminusT == max(expminusT))[0]
    shorteststep = allnextsteps.pop(ind[0])
    for k in range(1,len(ind)):
        allnextsteps.remove(ind[k]) #remove duplicate mapped points
    print("")
    print(pt)
    print(shorteststep)
    print(next_threshs)
    print(expminusT)
    print(ind)
    whichwall = getWallIndex(shorteststep,next_threshs,ind,wallsandsteadypts,pt)
    print(whichwall)
    return shorteststep, allnextsteps, whichwall

def getWallIndex(next_step,next_threshs,coords,wallsandsteadypts,previous):
    '''
    Find the index of the wall that next_step is on. If the point lies
    on the intersection of two or more walls due to a simultaneous arrival,
    then the indices of all the walls will be returned.

    '''
    inds = []
    for c in coords:
        inds.extend([_i for _i,_w in enumerate(wallsandsteadypts) if _w[c][0] == _w[c][1] and _w[c][0] == next_threshs[c]])
    mywall = []
    # find all indices where next_step is in the closure of the wall
    # if there is only one such index, we're done
    for i in sorted(inds):
        w = wallsandsteadypts[i]
        if all( [ ns >= w[c][0] and ns <= w[c][1] for c,ns in enumerate(next_step)] ):
            mywall.append( i )
    # if there's more than one index, we need to take the direction of flow into 
    # account, because now 2 or more variables are at threshold
    if len(mywall) != 1:
        jnds = [j for j in range(len(next_threshs)) if any( [wallsandsteadypts[i][j][0] == wallsandsteadypts[i][j][0] for i in mywall] )  ]
        mynewwall = []
        signs = (next_step - previous > 0)
        for i in mywall:
            w = wallsandsteadypts[i]
            truthtable = []
            for j in jnds:
                if next_step[j] == w[j][0] and (w[j][0] == w[j][1] or signs[j]):
                    truthtable.append( 1 )
                elif next_step[j] == w[j][1] and not signs[j]:
                    truthtable.append( 1 )
                else:
                    truthtable.append( 0 )
            if not np.all(truthtable):
                mynewwall.append( i )
        mywall = mynewwall
    return mywall

def mapManyPointsToMultipleHyperplanes(wallverts,fp,next_threshs,dr,wallsandsteadypts):
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
    whichwall = []
    mappedptsallsteps = []
    for v in wallverts:
        s,a,ww = mapOnePointToMultipleHyperplanes(v,fp,next_threshs,dr,wallsandsteadypts)
        mappedpts.append( s )
        mappedptsallsteps.append( a )
        whichwall.append( ww )
    return mappedpts, whichwall, mappedptsallsteps

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
    wallsandsteadypts = unidirwalls
    wallsandsteadypts.extend([[(s,s) for s in sp] for sp in steadypts])
    mappedvertices = []
    wallidentifier = []
    othervertsteps = []
    for k,w in enumerate(wallvertices):
        mp, wid, mpa = mapManyPointsToMultipleHyperplanes(w,unidirfps[k],next_threshs[k],dr,wallsandsteadypts)
        mappedvertices.append( mp )
        wallidentifier.append( wid )
        othervertsteps.append( mpa )
    return wallsandsteadypts, wallvertices, mappedvertices, wallidentifier, othervertsteps
