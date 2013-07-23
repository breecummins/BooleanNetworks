import numpy as np
import BooleanMapForDB as BDB
import itertools

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
                hpxt[k] = np.array([xt])
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
    res = 0.1
    maxvals = [1.0]*len(sources)
    hyperplanes = makeHyperplaneGrids(res,thresh,maxvals)
    print(len(hyperplanes))
    print(hyperplanes)