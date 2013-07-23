import numpy as np
import BooleanMapForDB as BDB

def makeHyperplaneGrids(res,thresh,maxvals):
    '''
    Create a cell-centered grid of resolution res for each
    hyperplane that exists when a variable is at threshold.
    thresh is the parameter array containing the thresholds.
    maxvals is a user-supplied list of the maximum value 
    allowed for each variable.

    The output is a list of hyperplanes, the number of which
    is determined by the dimension of thresh and the number
    of unique threshold values in each column.
    
    Each hyperplane will have one variable that is
    constant at a threshold. The other variables will be 
    bounded between two of their threshold values, or between
    zero and their lowest threshold, or between their highest
    threshold and maxvals[k]. 

    Cell-centered means that the returned vertices fall in the 
    middle of the grid cells. For example, for a square box with
    every variable between 0 and 1 and resolution h, the first 
    grid point is (h/2, h/2, ...) and the last vertex is 
    (1 - h/2, 1 - h/2, ...), with the appropriate threshold value
    entered at the threshold coordinate i.

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
    # discretize the chunks between thresholds for each var
    chunks = []
    for k,u in enumerate(uniqthresh):
        mins = np.concatenate((np.array([0]), u))
        maxs = np.concatenate((u, np.array([maxvals[k]])))
        npts = np.floor((maxs - mins)/res)
        slop = (maxs-mins) - npts*res
        cu = []
        for j,m in enumerate(mins):
            cu.append( np.arange(m + slop[j]/2 + res/2, maxs[j], res) )
        chunks.append( cu )
    # assemble chunks into hyperplanes
    hyperplanes = []
    for k,u in enumerate(uniqthresh):
        for j,xt in enumerate(u):
            #make combinations for i != k of the chunks and combine with np.array([xt]) to get hyperplane
            pass
            # for i in range(len(chunks)):
            #     if i != k: 
            #         for c in chunks[i]:
                        



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