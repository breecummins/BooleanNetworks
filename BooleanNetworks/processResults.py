import numpy as np
import cPickle, glob, os, itertools, gc

def postprocess(myfiles,fname=None):
    results = loadNSort(myfiles)
    if fname:
        cPickle.dump(results,open(fname+'.pickle','w'))
    printme(results)

def printme(results=None,fname=None):
    if fname:
        results = cPickle.load(open(fname,'r'))
    Ng = float(len(results['allgoodtracks']))
    N = Ng + len(results['allbadtracks'])
    print('Total number of tracks across parameter space')
    print(int(N))
    print('Total number of good tracks')
    print(int(Ng))
    print('Number of unique good tracks')
    print(len(results['uniqgoodtracks']))
    print('Number of unique bad tracks')
    print(len(results['uniqbadtracks']))

    tbt = []
    empties = 0
    emptycount = 0
    for k,t in enumerate(results['translatedbadtracks']):
        tbt.extend(t)
        if t == []:
            empties += 1
            emptycount += results['badcounted'][k]
    utbt,_=countClass(tbt)
    print('Number of unique good tracks from translating bad tracks')
    print(len(utbt))
    print('Number of unique untranslated bad tracks')
    print(empties)
    print('Total number of untranslated bad tracks')
    print(emptycount)

    print('Number of unique sharp one loops')
    print(len(results['sharponeloop']))
    # print(results['sharponeloop'])
    print('Number of unique broad one-loops')
    print(len(results['oneloop']))
    print('Number of unique sharp periodic loops')
    print(len(results['sharpperiodic']))
    # print(results['sharpperiodic'])
    print('Number of unique broad periodic loops')
    print(len(results['periodic']))
    # print(results['periodic'])
    print('Number of unique no loops')
    print(len(results['noloop']))
    print('Number of unique overlapped loops')
    print(len(results['overlapped']))
    print('Number of unique tracks in a different equilibrium (stuck in a subloop or nonzero fixed point')
    print(len(results['diffequilib']))
    print('Number of unique unclassified loops')
    print(len(results['unclassified']))

    if len(results['sharponeloop']) > 0:
        print('Sharp one loops: # good tracks; prop in good tracks; # good + translated; prop in total')
        print((results['sharponeloopcount'],results['sharponeloopcount']/Ng,results['sharponeloopcountmodified'],results['sharponeloopcountmodified']/N))
    if len(results['oneloop']) > 0:
        print('Broad one loops: # good tracks; prop in good tracks; # good + translated; prop in total')
        print((results['oneloopcount'],results['oneloopcount']/Ng,results['oneloopcountmodified'],results['oneloopcountmodified']/N))
    if len(results['sharpperiodic']) > 0:
        print('Sharp periodic loops: # good tracks; prop in good tracks; # good + translated; prop in total')
        print((results['sharpperiodiccount'],results['sharpperiodiccount']/Ng,results['sharpperiodiccountmodified'],results['sharpperiodiccountmodified']/N))
    if len(results['periodic']) > 0:
        print('Broad periodic: : # good tracks; prop in good tracks; # good + translated; prop in total')
        print((results['periodiccount'],results['periodiccount']/Ng,results['periodiccountmodified'],results['periodiccountmodified']/N))
    if len(results['overlapped']) > 0:
        print('Overlapped waves: # good tracks; prop in good tracks; # good + translated; prop in total')
        print((results['overlappedcount'],results['overlappedcount']/Ng,results['overlappedcountmodified'],results['overlappedcountmodified']/N))
    if len(results['diffequilib']) > 0:
        print('Different equilibria (other fixed point or stuck in a subloop): # good tracks; prop in good tracks; # good + translated; prop in total')
        print((results['diffequilibcount'],results['diffequilibcount']/Ng,results['diffequilibcountmodified'],results['diffequilibcountmodified']/N))
    if len(results['noloop']) > 0:
        print('Incomplete loops: # good tracks; prop in good tracks; # good + translated; prop in total')
        print((results['noloopcount'],results['noloopcount']/Ng,results['noloopcountmodified'],results['noloopcountmodified']/N))
    if len(results['unclassified']) > 0:
        print('Unclassified loops: : # good tracks; prop in good tracks; # good + translated; prop in total')
        print((results['unclassifiedcount'],results['unclassifiedcount']/Ng,results['unclassifiedcountmodified'],results['unclassifiedcountmodified']/N))

def eqClasses(badtrack):
    '''
    Construct good tracks consistent with badtrack. 
    The minimal number of extra steps are added to badtrack
    to ensure only one bit flip per step. Not all of these 
    tracks will be consistent with the ODE solution.

    '''
    inds = []
    steps = []
    # find all locations where more than one bit flip occurs and calculate consistent intermediate steps to be inserted at that location
    for k in range(1,badtrack.shape[0]):
        diff = badtrack[k,:]-badtrack[k-1,:]
        localinds = np.nonzero(diff)[0]
        N = len(localinds)
        if N > 1:
            inds.append(k)
            # make all possible permutations of the order of the single bit flips that need to be inserted immediately before index k
            perms = itertools.permutations(localinds)
            templist = []
            for p in perms:
                temp = np.zeros((N-1,badtrack.shape[1]))
                temp += badtrack[k-1,:] 
                for i,j in enumerate(p[:-1]):
                    temp[i:,j] += diff[j]
                templist.append(temp)
            steps.append(templist)
    # make a template for the equivalence classes of badtrack
    newpts = [s[0].shape[0] for s in steps]
    template = np.zeros((badtrack.shape[0]+sum(newpts),badtrack.shape[1]))
    myinds = [0]+inds+[badtrack.shape[0]]
    for k,i in enumerate(myinds[1:]):
        template[myinds[k]+sum(newpts[:k]):i+sum(newpts[:k]),:] = badtrack[myinds[k]:i,:]
    # save the indices where new steps must be inserted
    replinds = []
    for k in range(len(inds)):
        replinds.append((inds[k]+sum(newpts[:k]),inds[k]+sum(newpts[:k+1]))) 
    # make all possible combinations of insertions at the different locations
    stepinds = [range(len(s)) for s in steps]
    combos=itertools.product(*stepinds)
    # construct the candidate good tracks
    equivcls = []
    for c in combos:
        tp = template.copy()
        for k in range(len(replinds)):
            r = replinds[k]
            step = steps[k]
            tp[r[0]:r[1],:] = step[c[k]]
        equivcls.append(tp)
        del(tp)
        gc.collect()
    # if len(inds) > 1:
    #     print('More than one bad step')
    #     print(b)
    # if any([len(s) > 2 for s in steps]):
    #     print('More than two bit flips')
    #     print(b)  
    return equivcls

def oneBitFlip(ol):
    for k in range(1,ol.shape[0]):
        if (np.abs(ol[k,:]-ol[k-1,:])).sum() > 1:
            return False
    return True

def classifyTrack(track):
    # if the last point in the track is equilibrium, if each of y1,y2,y3 were touched, and if x does not reinitiate, count the track as one loop
    if np.all(track[-1,:]==0) and np.any(track[:,1] ==1) and np.any(track[:,2] ==1) and np.any(track[:,3] ==1) and np.all(track[track[:,0].argmin():,0]==0):
        # if the wave is sharp, record it
        if np.all(np.sum(track[:,:-1],1) < 3):
            return 'sharponeloop'
        else:    
            return 'oneloop'
    # if not a single loop is completed, count as no loops
    elif np.all(track[track[:,0].argmin():,0]==0) and (np.all(track[:,1] ==0) or np.all(track[:,2] ==0) or np.all(track[:,3] ==0)):
        return 'noloop'
    # if the initial condition is reached again and if each of y1,y2,y3 were touched, count as periodic
    elif np.any(track[:,1] ==1) and np.any(track[:,2] ==1) and np.any(track[:,3] ==1) and np.any([np.all(t == np.array([1,0,0,0,0])) for t in track[track[:,0].argmin():,:]]):
        # if the wave is sharp, record it
        if np.all(np.sum(track[:,:-1],1) < 3):
            return 'sharpperiodic'
        else:    
            return 'periodic'
    # if x is reinitialized and if each of y1,y2,y3 were touched and the last point is at equilibrium, count as overlapping wave (last wave didn't finish before new one began)
    elif np.any(track[:,1] ==1) and np.any(track[:,2] ==1) and np.any(track[:,3] ==1) and np.any(track[track[:,0].argmin():,0] == 1) and np.all(track[-1,:]==0):
        return 'overlapped'
    # if the last time step is not at [0,0,0,0,0] and the track is not periodic, then the track is either stuck in a subloop (unstable limit cycle) or is at a different fixed pt
    elif np.any(track[-1,:] != 0):
        return 'diffequilib'
    else:
        return 'unclassified'

def separateBadTracks(myfiles):
    '''
    myfiles is a glob expression representing several
    files. Each file is loaded and the tracks extracted.
    This function separates the good tracks and bad
    tracks, where good tracks have exactly one bit flip 
    per step. Bad tracks have more than one bit flip on
    at least one step. Bad tracks are separated
    out for further processing before classification.

    '''
    allgoodtracks = []
    allbadtracks = []
    for f in glob.glob(myfiles):
        print(f)
        of = open(f,'r')
        tracks = cPickle.load(of)
        of.close()
        for track in tracks:
            if not oneBitFlip(track):
                allbadtracks.append(track)
            else:
                allgoodtracks.append(track)
    return allgoodtracks, allbadtracks

def countClass(lot):
    '''
    lot is a list of tracks (numpy nx5 arrays).
    This function finds the unique tracks and counts 
    the number of each that there are in lot.

    '''
    # need tuples because a list of arrays doesn't work with count
    tuplot = [tuple(b.flatten()) for b in lot]
    ulot = list(set(tuplot))
    counted = []
    for u in ulot:
        counted.append(tuplot.count(u))
    return [np.array(t).reshape(-1,5) for t in ulot],counted

def loadNSort(myfiles):
    # load files and separate good from bad tracks
    print('Loading...')
    allgoodtracks,allbadtracks = separateBadTracks(myfiles)
    print('Analyzing...')
    uniqgoodtracks,goodcounted = countClass(allgoodtracks)
    uniqbadtracks,badcounted = countClass(allbadtracks)
    # separate unique bad tracks into equivalence classes, weed out ones not in uniqgoodtracks, and add fractional numbers to good counted
    translatedbadtracks = []
    modifiedgoodcounted = list(goodcounted)
    longestgoodtrack = max([len(g) for g in uniqgoodtracks])
    for k,b in enumerate(uniqbadtracks):
        if b.shape[0] >= min(longestgoodtrack,400):
            translatedbadtracks.append([])
            continue
        eqtracks = eqClasses(b)
        neweq = []
        ginds = []
        for t in eqtracks:
            for i,u in enumerate(uniqgoodtracks):
                # only keep the reconstructed tracks that are good tracks
                if np.all(t==u):
                    neweq.append(t)
                    ginds.append(i)
                    break
        # save the acceptable tracks
        translatedbadtracks.append(neweq)
        # equally distribute count across allowable tracks
        if len(neweq) > 0:
            prop = 1.0 / len(neweq)
            for i in ginds:
                modifiedgoodcounted[i] += prop*badcounted[k]
    # create dict to store results
    results = {'allgoodtracks':allgoodtracks,'allbadtracks':allbadtracks,'uniqgoodtracks':uniqgoodtracks,'uniqbadtracks':uniqbadtracks,'translatedbadtracks':translatedbadtracks,'goodcounted':goodcounted,'modifiedgoodcounted':modifiedgoodcounted,'badcounted':badcounted,'oneloop': [],'oneloopcount': 0,'oneloopcountmodified': 0,'sharponeloop': [],'sharponeloopcount': 0,'sharponeloopcountmodified': 0,'noloop': [],'noloopcount': 0,'noloopcountmodified': 0,'periodic': [],'periodiccount': 0,'periodiccountmodified': 0,'sharpperiodic': [],'sharpperiodiccount': 0,'sharpperiodiccountmodified': 0,'overlapped': [],'overlappedcount': 0,'overlappedcountmodified': 0,'diffequilib':[],'diffequilibcount': 0,'diffequilibcountmodified': 0,'unclassified': [],'unclassifiedcount': 0,'unclassifiedcountmodified': 0}
    # only classify unique good tracks
    for k,track in enumerate(uniqgoodtracks):
        classstr = classifyTrack(track)
        results[classstr].append(track)
        results[classstr+'count'] += goodcounted[k]
        results[classstr+'countmodified'] += modifiedgoodcounted[k]
    return results

if __name__ == "__main__":
    maindir = os.path.expanduser('~/SimulationResults/BooleanNetworks/dataset_randinits_biggerx/')
    # maindir = os.path.expanduser('~/SimulationResults/BooleanNetworks/dataset_perdt/')
    postprocess(maindir+'model1tracks*',maindir+'model1Results')
    # postprocess(maindir+'model2tracks*',maindir+'model2Results')    
    # postprocess(maindir+'model3tracks*',maindir+'model3Results')    
    # postprocess(maindir+'model4tracks*',maindir+'model4Results')
    # print('#########################################################')
    # print('Model 1')
    # printme(fname=maindir + 'model1Results.pickle')
    # print('#########################################################')
    # print('Model 2')
    # printme(fname=maindir + 'model2Results.pickle')
    # print('#########################################################')
    # print('Model 3')
    # printme(fname=maindir + 'model3Results.pickle')
    # print('#########################################################')
    # print('Model 4')
    # printme(fname=maindir + 'model4Results.pickle')
