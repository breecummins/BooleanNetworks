import numpy as np
import cPickle, glob, os, itertools, gc

def postprocess(myfiles,fname=None):
    results = loadNSort(myfiles)
    if fname:
        with open(fname, 'w') as of:
            cPickle.dump(results,of)
    printme(results)

def printme(results=None,fname=None):
    if fname:
        with open(fname, 'r') as of:
            results = cPickle.load(of)
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

    Keys = ['sharponeloop','oneloop','sharpperiodictwowaves','sharpperiodic','periodictwowaves','periodic','overlappedtwowaves','overlapped','diffequilibwithwave','diffequilib','noloop','unclassified']

    for k in Keys:
        if 'count' not in k and 'note' not in k:
            print('Number of unique ' + results['classes'][k + 'note'])
            print(len(results['classes'][k]))
            # if k == 'diffequilibwithwave':
            #     print(results['classes'][k])

    for k in Keys:
        if 'count' not in k and 'note' not in k and len(results['classes'][k]) > 0:
            print(results['classes'][k + 'note'] + ': # good tracks; prop in good tracks; # good + translated; prop in total')
            print((results['classes'][k+'count'],results['classes'][k+'count']/Ng,results['classes'][k + 'countmodified'],results['classes'][k + 'countmodified']/(N-emptycount)))

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

def classifyTrack(track):
    # find index of x's first zero (if there are no zeros, firstzero = 0) and first reinitialization of x (if it doesn't occur, nextone = firstzero)
    firstzero = track[:,0].argmin()
    nextone = firstzero + track[firstzero:,0].argmax()
    # define a function that can identify a completed wave
    def completedwave(track=track, firstzero=firstzero, nextone=nextone):
        # x has to turn off
        if firstzero == 0:
            return False
        # y1, y2, and y3 have to turn on
        if np.any(track[firstzero:nextone,1] == 1) and np.any(track[firstzero:nextone,2] == 1) and np.any(track[firstzero:nextone,3] == 1):
            return True
        else:
            return False
    # function to identify sharp waves (no more than two of x,y1,y2,y3 are activated at a time)
    def issharp(track):
        if np.all(np.sum(track[:,:-1],1) < 3):
            return True
        else:
            return False
    ###### Now classify the track ######
    # if not a single loop is completed, count as no loops 
    if not completedwave(nextone=track.shape[0]):
        return 'noloop'
    # if the last time step is not at [0,0,0,0,0], then the track is either stuck in a subloop (unstable limit cycle) or is at a different fixed pt (I assume sufficient simulation time)
    elif np.any(track[-1,:] != 0):
        # if there is a completed wave at the beginning, record it
        if completedwave():
            return 'diffequilibwithwave'
        else:
            return 'diffequilib'
    # if x does not reinitiate, count the track as one loop
    elif nextone == firstzero:
        # if the wave is sharp, record it
        if issharp(track):
            return 'sharponeloop'
        else:    
            return 'oneloop'
    # if the initial condition is reached after first wave, count as periodic
    elif np.all(track[nextone+1,:] == np.array([1,0,0,0,0])):
        # if there are at least two completed loops, record it
        subtrack = track[nextone+1:,:]
        stfz = subtrack.argmin()
        stno = stfz + subtrack[stfz:,0].argmax()
        if stno == stfz:
            stno = track.shape[0]
        if completedwave(subtrack,stfz,stno):
            # if the wave is sharp, record it
            if issharp(track):
                return 'sharpperiodictwowaves'
            else:    
                return 'periodictwowaves'
        else:
            # if the wave is sharp, record it
            if issharp(track):
                return 'sharpperiodic'
            else:    
                return 'periodic'
    # if x is reinitialized but initial condition does not recur immediately after the first wave, count as overlapping wave (last wave didn't finish before new one began)
    elif np.any(track[firstzero:,0]) == 1:
        # if there are at least two completed loops, record it
        subtrack = track[nextone+1:,:]
        stfz = subtrack.argmin()
        stno = stfz + subtrack[stfz:,0].argmax()
        if stno == stfz:
            stno = track.shape[0]
        if completedwave(subtrack,stfz,stno):
            return 'overlappedtwowaves'
        else:
            return 'overlapped'
    else:
        return 'unclassified'

def oneBitFlip(ol):
    for k in range(1,ol.shape[0]):
        if (np.abs(ol[k,:]-ol[k-1,:])).sum() > 1:
            return False
    return True

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
        # print(f)
        with open(f, 'r') as of:
            tracks = cPickle.load(of)
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
    # import modelNetworks as mN
    # ugt = [mN.encodeInts(g) for g in uniqgoodtracks]
    # ubt = [mN.encodeInts(b) for b in uniqbadtracks]
    # print(ugt)
    # print(goodcounted)
    # print(ubt)
    # print(badcounted)
    # return ugt, goodcounted, ubt, badcounted
    # separate unique bad tracks into equivalence classes, weed out ones not in uniqgoodtracks, and add fractional numbers to good counted
    translatedbadtracks = []
    modifiedgoodcounted = list(goodcounted)
    longestgoodtrack = max([len(g) for g in uniqgoodtracks])
    for k,b in enumerate(uniqbadtracks):
        if b.shape[0] >= longestgoodtrack:
            # print('Bad track of length ' + str(b.shape[0]) + ' is too long. Skipping track ' + str(k) + '.')
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
        # if neweq ==[]:
        #     print('No good tracks found for bad track ' + str(k) + '.')
        #     if b.shape[0] < 30:
        #         print(b)
        # save the acceptable tracks
        translatedbadtracks.append(neweq)
        # equally distribute count across allowable tracks
        if len(neweq) > 0:
            prop = 1.0 / len(neweq)
            for i in ginds:
                modifiedgoodcounted[i] += prop*badcounted[k]
    # create dict to store results
    results = {'allgoodtracks':allgoodtracks,'allbadtracks':allbadtracks,'uniqgoodtracks':uniqgoodtracks,'uniqbadtracks':uniqbadtracks,'translatedbadtracks':translatedbadtracks,'goodcounted':goodcounted,'modifiedgoodcounted':modifiedgoodcounted,'badcounted':badcounted,'classes':{'oneloop': [],'oneloopcount': 0,'oneloopcountmodified': 0,'oneloopnote':'Broad One Loops', 'sharponeloop': [],'sharponeloopcount': 0,'sharponeloopcountmodified': 0,'sharponeloopnote':'Sharp One Loops','noloop': [],'noloopcount': 0,'noloopcountmodified': 0,'noloopnote':'Incomplete Loops','periodic': [],'periodiccount': 0,'periodiccountmodified': 0,'periodicnote':'Broad Periodic Loops with < 2 waves','sharpperiodic': [],'sharpperiodiccount': 0,'sharpperiodiccountmodified': 0,'sharpperiodicnote':'Sharp Periodic Loops with < 2 waves','periodictwowaves': [],'periodictwowavescount': 0,'periodictwowavescountmodified': 0,'periodictwowavesnote':'Broad Periodic Loops with >= 2 waves','sharpperiodictwowaves': [],'sharpperiodictwowavescount': 0,'sharpperiodictwowavescountmodified': 0,'sharpperiodictwowavesnote':'Sharp Periodic Loops with >= 2 waves','overlapped': [],'overlappedcount': 0,'overlappedcountmodified': 0,'overlappednote':'Periodic Loops that overlap (double bump waves) with < 2 waves','overlappedtwowaves': [],'overlappedtwowavescount': 0,'overlappedtwowavescountmodified': 0,'overlappedtwowavesnote':'Periodic Loops that overlap (double bump waves) with >= 2 waves','diffequilib':[],'diffequilibcount': 0,'diffequilibcountmodified': 0,'diffequilibnote':'Different Equilibria (stuck in a subloop or at a different fixed pt) with < 1 wave','diffequilibwithwave':[],'diffequilibwithwavecount': 0,'diffequilibwithwavecountmodified': 0,'diffequilibwithwavenote':'Different Equilibria (stuck in a subloop or at a different fixed pt) with >= 1 wave','unclassified': [],'unclassifiedcount': 0,'unclassifiedcountmodified': 0,'unclassifiednote':'Unclassified Tracks'}}
    # only classify unique good tracks
    for k,track in enumerate(uniqgoodtracks):
        classstr = classifyTrack(track)
        results['classes'][classstr].append(track)
        results['classes'][classstr+'count'] += goodcounted[k]
        results['classes'][classstr+'countmodified'] += modifiedgoodcounted[k]
    return results

if __name__ == "__main__":
    maindir = os.path.expanduser('~/SimulationResults/BooleanNetworks/dataset_randinits_biggerx/')
    # maindir = os.path.expanduser('~/SimulationResults/BooleanNetworks/dataset_perdt/')
    # postprocess(maindir+'model1tracks*',maindir+'model1Results')
    postprocess(maindir+'model2tracks*_arrays.pickle',maindir+'model2Results')    
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
