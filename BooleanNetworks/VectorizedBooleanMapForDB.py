import numpy as np
import BooleanMapForDB as BDB
import itertools

def makeHyperplanes(thresh,maxvals,eps=0.01):
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
            # combine with threshold values into hyperplane discretizations
            for xt in u:
                hpxt = list(hp)
                hpxt[k] = (xt,xt)
                hyperplanes.append( hpxt )                        
    return hyperplanes

def subdivideBox(N,minval,maxval):
    pass

def mapManyPoints(vertices,thresh,amp,rep,dr,previous):
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

def makeModel(sources,targets,thresholds,amplitudes,decayrates,repressors):
    '''
    See documentation for BooleanMapForDB.modelTrajectory.

    '''
    dr = np.array(decayrates)
    thresh,amp,rep = BDB.makeParameterArrays(sources,targets,thresholds,amplitudes,repressors)
    return thresh,amp,rep,dr

if __name__ == '__main__':
    sources = ['x','y1','y2','z']
    targets = [['x','y1','z'],['y2'],['x','z'],['x']]
    thresholds = [[0.25,0.5,0.75],[0.5],[0.5,0.5],[0.5]]
    amplitudes = [[0.5,1.0,1.0],[1.0],[1.0,1.0],[1.0]]
    decayrates = [1.0,0.5,0.5,0.5]
    repressors = [('z','x')]
    thresh,amp,rep,dr = makeModel(sources,targets,thresholds,amplitudes,decayrates,repressors)
    maxvals = [1.0]*len(sources)
    hyperplanes = makeHyperplanes(thresh,maxvals)
    print(len(hyperplanes))
    for h in hyperplanes:
        formattedh = ['({0:.3f}, {1:.3f})'.format(tup[0],tup[1]) for tup in h]
        print(str(formattedh).translate(None, "'"))