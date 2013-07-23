import numpy as np

def makeParameterArrays(sources,targets,thresholds,amplitudes,repressors):
    '''
    INPUTS:
    See modelTrajectory.

    OUTPUTS:
    thresh, amp, and rep are len(sources) x len(sources)
    arrays with sources associated with  the column indices and 
    targets associated with the row indices. Threshold values,
    amplitudes, and repressor identity are filled in between
    the appropriate source-target interactions. All other array 
    values are zero.

    '''
    N = len(sources)
    thresh = np.zeros((N,N))
    amp = np.zeros((N,N))
    for j,targ in enumerate(targets):
        for k,t in enumerate(targ):
            i = sources.index(t)
            thresh[i,j] = thresholds[j][k]
            amp[i,j] = amplitudes[j][k]
    rep = np.zeros((N,N))
    for r in repressors:
        j = sources.index(r[0])
        i = sources.index(r[1])
        rep[i,j] = 1
    return thresh, amp, rep.astype(int)

def getState(steps,thresh):
    state = []
    for j,s in enumerate(steps):
        st = []
        for k,i in enumerate(s):
            count = 0
            for t in np.unique(thresh[:,k])[1:]:
                if i>t:
                    count += 1
                elif i==t and j > 0 and steps[j-1][k] < s[k]:
                    count += 1
            st.append(count)
        state.append(st)
    return state

def getTraversalTime(init,fp,next_threshs,dr):
    '''
    One of the set of thresholds next_threshs must be crossed first.
    Calculate the times exp(-t*) of every crossing and pick the maximal
    value. Return the index of this value.

    '''
    expminusT = []
    for k,i in enumerate(init):
        xT = next_threshs[k]
        r = dr[k]
        if xT > 0:
            expminusT.append( (( xT - fp[k] ) / ( i - fp[k] ))**(1./r) )
    #remove the times that are 1.0 due to a variable already on the threshold
    for k,t in enumerate(expminusT):
        if t == 1.0:
            expminusT[k] = 0
    return max(expminusT)

def getFocalPoint(init,thresh,amp,rep,dr,previous=None):
    up = (init > thresh)
    if previous != None:
        for k,i in enumerate(init):
            if i > previous[k]:
                up[:,k] += (i == thresh[:,k])
    A = amp*(up ^ rep)
    return A.sum(1)/dr


def takeAStep(init,thresh,amp,rep,dr,previous=None):
    '''
    Given an initial point init and the parameter arrays of the 
    model, find the focal point toward which the dynamical system 
    is evolving, and then calculate which hyperplane is intersected 
    on the way there. 

    Return the exact point on the hyperplane where the init condition 
    hits.

    If there is no next hyperplane due to the existence of a steady
    state, return the steady point and a message indicating the 
    trajectory is finished.

    '''
    #get focal point
    fp = getFocalPoint(init,thresh,amp,rep,dr,previous)
    print('Focal point: {0}'.format(fp))
    #find thresholds between init and focal point
    dif = init-thresh
    possible_threshs = dif*(fp-thresh) < 0
    #correct for the places where init[k] is right at threshold
    #then fp has to be at least one more threshold away
    for k in range(len(init)):
        q = np.nonzero(dif[:,k] == 0)[0]
        possible_threshs[q,k] = False
    pt = possible_threshs*thresh
    # print('Possible thresholds: {0}'.format(pt))
    #get the closest threshold to each coordinate
    next_threshs = np.zeros(fp.shape)
    for k in range(len(init)):
        if init[k] > fp[k]:
            next_threshs[k] = pt[:,k].max()
        elif init[k] < fp[k] and np.any(pt[:,k]):
            next_threshs[k] = pt[pt[:,k]>0,k].min()
    # print('Next thresholds: {0}'.format(next_threshs))
    #if there are no intervening thresholds, then the focal point is a steady state
    #return the focal point in state form
    if np.all(next_threshs == 0):
        return fp, 'Steady state reached! {0}'.format(fp)
    #otherwise calculate the shortest traversal times to the thresholds and
    #get the next point on the next hyperplane 
    expminusT = getTraversalTime(init,fp,next_threshs,dr)
    # print('Time: {0}'.format(expminusT))
    nextstep = fp + (init-fp)*(expminusT**dr)
    print('Hyperplane step: {0}'.format(nextstep))
    return (nextstep,)


def modelTrajectory(init,sources,targets,thresholds,amplitudes,repressors,decayrates):
    '''
    INPUTS:
    init is an initial condition for all the variables in
    sources

    sources is the list of variable names. The index of each
    source is associated with a list of parameters in several
    different parameter lists:

    targets is a list of lists of variable names of the vars
    affected by source[k] 

    thresholds is a list of lists of the threshold values
    by which sources[k] affects the list of variables in 
    targets[k]

    amplitudes is a list of lists of the magnitude of the 
    effects of sources[k] on targets[k]

    repressors is the list of tuples of variable names 
    consisting of (source, target) that are repressing instead 
    of activating interactions

    decayrates is a list containing the decay rates of each
    variable in sources

    OUTPUTS:
    The trajectory in integer state space starting at the initial
    condition and ending at a steady point. If the trajectory 
    hasn't reached a steady point after 1000 steps, the simulation 
    is stopped.

    '''
    init = np.array(init)
    dr = np.array(decayrates)
    thresh,amp,rep = makeParameterArrays(sources,targets,thresholds,amplitudes,repressors)
    print('Initial condition: {0}'.format(init))
    nextstep = takeAStep(init,thresh,amp,rep,dr)
    traj = [init,nextstep[0]]
    while len(nextstep) < 2 and len(traj) < 1000:
        nextstep = takeAStep(nextstep[0],thresh,amp,rep,dr,traj[-2])
        traj.append(nextstep[0])
    if len(nextstep) == 2:
        print(nextstep[1])
    state = getState(traj,thresh)
    return traj,state

if __name__ == '__main__':
    sources = ['x','y1','y2','z']
    targets = [['x','y1','z'],['y2'],['x','z'],['x']]
    thresholds = [[0.25,0.5,0.75],[0.5],[0.5,0.5],[0.5]]
    amplitudes = [[0.5,1.0,1.0],[1.0],[1.0,1.0],[1.0]]
    decayrates = [1.0,0.5,0.5,0.5]
    repressors = [('z','x')]
    # thresh, amp, rep = makeParameterArrays(sources,targets,thresholds,amplitudes,repressors)
    # print(thresh)
    # print(amp)
    # print(rep)
    # init = [0.6,0.4,0.25,0.2] #Steady state with no white wall
    # init = [0.8,0.4,0.25,0.2] #This init condition gives me a white wall, I think. x bounces off the 0.75 threshold
    init = [0.7,0.6,0.25,0.2]
    # init = [0.3,0.7,0.4,0.4]
    traj,state = modelTrajectory(init,sources,targets,thresholds,amplitudes,repressors,decayrates)
    # print(traj)
    print(state)
    #############
    # init = np.array(init)
    # dr = np.array(decayrates)
    # thresh,amp,rep = makeParameterArrays(sources,targets,thresholds,amplitudes,repressors)
    # print(init)
    # nextstep = takeAStep(init,thresh,amp,rep,dr)
    ##############
