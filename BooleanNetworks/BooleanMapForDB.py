import numpy as np

def makeParameterArrays(sources,targets,thresholds,amplitudes,repressors):
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

def getTraversalTime(init,fp,next_threshs,dr):
    '''
    Find and return the time exp(-t*) to the next threshold in next_threshs 
    that is crossed _first_ when traveling from init to the focal point fp. 
    
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
    return max(expminusT)

def getFocalPoint(init,thresh,amp,rep,dr,previous):
    '''
    Calculate the focal point of the dynamical system
    when the last step was previous and the current
    location is init.

    First, find in what coordinates init is strictly 
    above threshold. This means the coordinate will 
    influence others. This will also happen if the
    coordinate is now at threshold, but was previously 
    below threshold. So second, add in those effects.

    Third, calculate the amplitude of all coordinates 
    above threshold, and scale by the decay rates of
    each coordinate. This is the focal point return
    value. Note that to calculate amplitude, every
    repressor has to be bit-swapped, because its 
    amplitude is on when the repressor is off.

    '''
    up = (init > thresh) #first
    for k,i in enumerate(init): #second
        if i > previous[k]:
            up[:,k] += (i == thresh[:,k])
    A = amp*(up ^ rep) #third
    return A.sum(1)/dr


def takeAStep(init,thresh,amp,rep,dr,previous):
    '''
    Given an initial point (init), the previous point in the 
    trajectory (previous), and the parameter arrays of the 
    model (thresh, amp, rep, dr), find the focal point toward 
    which the dynamical system is evolving, and then calculate 
    which hyperplane is intersected first on the way there. 

    Return the exact point on the hyperplane where the init condition 
    hits. If there is no next hyperplane due to the existence of a steady
    state, return the steady point and a message indicating the 
    trajectory is finished.

    '''
    #get focal point
    fp = getFocalPoint(init,thresh,amp,rep,dr,previous)
    #find thresholds between init and focal point
    possible_threshs = (init-thresh)*(fp-thresh) < 0
    pt = possible_threshs*thresh
    #get the closest threshold to each coordinate
    next_threshs = np.zeros(fp.shape)
    for k in range(len(init)):
        if init[k] > fp[k]:
            next_threshs[k] = pt[:,k].max()
        elif init[k] < fp[k] and np.any(pt[:,k]):
            next_threshs[k] = pt[pt[:,k]>0,k].min()
    #if there are no intervening thresholds, then the focal point is a steady state
    if np.all(next_threshs == 0):
        return fp, 'Steady state reached! {0}'.format(fp)
    #otherwise get the next point on the next hyperplane 
    expminusT = getTraversalTime(init,fp,next_threshs,dr)
    nextstep = fp + (init-fp)*(expminusT**dr)
    # #debugging print statements
    # print('Focal point: {0}'.format(fp))
    # print('Possible thresholds: {0}'.format(pt))
    # print('Next thresholds: {0}'.format(next_threshs))
    # print('Time: {0}'.format(expminusT))
    print('Hyperplane step: {0}'.format(nextstep))
    return (nextstep,)

def getState(steps,thresh):
    '''
    Take a real-valued trajectory and return the 
    discrete state function. Each variable will have
    states = 0,1,...,nt, where nt is the number of 
    thresholds for that variable.

    '''
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

def modelTrajectory(init,sources,targets,thresholds,amplitudes,decayrates,repressors):
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

        decayrates is a list containing the decay rates of 
        source[k]

    repressors is a list of tuples of variable names 
    consisting of (source, target) that are repressing instead 
    of activating interactions


    OUTPUTS:
    The trajectory is returned in both real values (traj) and in integer 
    state space (state) starting at the initial condition and ending at 
    a steady point. If the trajectory hasn't reached a steady point after 
    1000 steps, the simulation is stopped.

    '''
    init = np.array(init)
    dr = np.array(decayrates)
    thresh,amp,rep = makeParameterArrays(sources,targets,thresholds,amplitudes,repressors)
    print('')
    print('Init condition:  {0}'.format(init))
    print('')
    nextstep = takeAStep(init,thresh,amp,rep,dr,init)
    traj = [init,nextstep[0]]
    while len(nextstep) < 2 and len(traj) < 1000:
        nextstep = takeAStep(nextstep[0],thresh,amp,rep,dr,traj[-2])
        traj.append(nextstep[0])
    if len(nextstep) == 2:
        print('')
        print(nextstep[1])
        print('')
    state = getState(traj[:-1],thresh)
    return traj, state

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
    # init = [0.6,0.4,0.25,0.2] 
    # init = [0.8,0.4,0.25,0.2] 
    init = [0.7,0.6,0.25,0.2]
    # init = [0.3,0.7,0.4,0.4]
    traj,state = modelTrajectory(init,sources,targets,thresholds,amplitudes,decayrates,repressors)
    # print(traj)
    print(state)
    #############
    # init = np.array(init)
    # dr = np.array(decayrates)
    # thresh,amp,rep = makeParameterArrays(sources,targets,thresholds,amplitudes,repressors)
    # print(init)
    # nextstep = takeAStep(init,thresh,amp,rep,dr)
    ##############
