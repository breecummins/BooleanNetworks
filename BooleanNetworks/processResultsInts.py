import numpy as np
import cPickle, glob, os, itertools, gc
import modelNetworks as mN

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

def translateBadTrack(badtrack,goodtracks):
    '''
    Construct good tracks consistent with badtrack. 
    The minimal number of extra steps are added to badtrack
    to ensure only one bit flip per step. Only solutions also
    found in goodtracks are accepted.

    '''
    inds = []
    newchunks = []
    # find all locations where more than one bit flip occurs and calculate consistent intermediate steps to be inserted at each bad location
    for k in range(1,len(badtrack)):
        if not oneBitFlip(badtrack[k-1:k+1]):
            inds.append(k)
            adjxor = badtrack[k-1]^badtrack[k]
            vals = [ v for v in map(lambda x: x & adjxor,[16,8,4,2,1]) if v > 0 ]
            signedvals = [-v if v & badtrack[k-1] else v for v in vals]
            perms = itertools.permutations(signedvals)
            steps = [[badtrack[k-1]+sum(p[:j]) for j in range(1,len(p))] for p in perms]
            newchunks.append(steps)
    # cut the bad track into sections divided by the locations with > 1 bit flip
    goodchunks = []
    myinds = [0]+inds+[len(badtrack)]
    for k in range(len(myinds)-1):
        goodchunks.append(list(badtrack[myinds[k]:myinds[k+1]]))
    stepopts = [range(len(c)) for c in newchunks]
    newtracks = []
    goodinds = []
    testtoint = 10
    if len(goodchunks) < testtoint:
        # construct the candidate good tracks
        stepopts = [range(len(c)) for c in newchunks]
        combos=itertools.product(*stepopts)
        for c in combos:
            t = list(goodchunks[0])
            for k in range(len(newchunks)):
                steps = newchunks[k]
                t += steps[c[k]]
                t += goodchunks[k+1]
            tt = tuple(t)
            for i,g in enumerate(goodtracks):
                if tt == g:
                    newtracks.append(tt)
                    goodinds.append(i)
                    break
    else:
        def partialconstruction(tinds,newtracks,goodinds):
            # construct the candidate good tracks
            combos=itertools.product(*stepopts[tinds[0]:tinds[1]])
            goodcombos = []
            for c in combos:
                flag = 'b'
                t = list(goodchunks[0])
                for k in range(tinds):
                    steps = newchunks[k]
                    t += steps[c[k]]
                    t += goodchunks[k+1]
                    for g in goodtracks:
                        if g[:len(t)] == tuple(t):
                            flag = 'c'
                            break
                    if flag == 'c':
                        continue
                    elif flag == 'b':
                        break
                if flag == 'c' and testtoint < len(newchunks):
                    goodcombos.append
                    break
                elif flag == 'c' and testtoint == len(newchunks):  
                    tt = tuple(t)
                    for i,g in enumerate(goodtracks):
                        if tt == g:
                            print('Match found!')
                            newtracks.append(tt)
                            goodinds.append(i)
                            break
            return flag,newtracks,goodinds
        
        flag,newtracks,goodinds=partialconstruction([0,testtoint],newtracks,goodinds)
        while flag == 'c':
            print('**********************This track could have a match**********************    ')
            testtoint = min(testtoint + 5,len(newchunks))
            flag,newtracks,goodinds = partialconstruction(testtoint,newtracks,goodinds)
    return newtracks, goodinds

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
        if completedwave(subtrack,stfz,stno):
            return 'overlappedtwowaves'
        else:
            return 'overlapped'
    else:
        return 'unclassified'

def countClass(lot):
    '''
    lot is a list of tracks (tuples of ints).
    This function finds the unique tracks and counts 
    the number of each that there are in lot.

    '''
    ulot = sorted(list(set(lot))) #need this as a list because order is important to coordinate with counted
    counted = map(lambda u: lot.count(u),ulot)
    return ulot,counted

def oneBitFlip(track):
    '''
    xor between successive steps is 2^n if there
    is only one bit flip. xor between successive
    steps is always integer > 0 by translation to 
    orthants then binary numbers. An integer 
    x > 0 is a power of 2 iff x & (x-1) == 0. 

    '''
    for k in range(1,len(track)):
        adjxor = track[k]^track[k-1] 
        if (adjxor & (adjxor-1))!=0:
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

def loadNSort(myfiles):
    # load files and separate good from bad tracks
    print('Loading...')
    allgoodtracks,allbadtracks = separateBadTracks(myfiles)
    print('Analyzing...')
    uniqgoodtracks,goodcounted = countClass(allgoodtracks)
    uniqbadtracks,badcounted = countClass(allbadtracks)
    # print(len(uniqgoodtracks))
    # print(len(uniqbadtracks))
    # print(goodcounted)
    # print(uniqbadtracks)
    # print(badcounted)
    # return uniqgoodtracks, goodcounted, uniqbadtracks, badcounted
    # separate unique bad tracks into equivalence classes, weed out ones not in uniqgoodtracks, and add fractional numbers to good counted
    translatedbadtracks = []
    modifiedgoodcounted = list(goodcounted) #this points to a new list
    longestgoodtrack = max([len(g) for g in uniqgoodtracks])
    uniqgoodtracksdecoded = [mN.decodeInts(g) for g in uniqgoodtracks]
    for k,b in enumerate(uniqbadtracks):
        if len(b) >= longestgoodtrack:
            print('Bad track of length ' + str(len(b)) + ' is too long. Skipping track ' + str(k) + '.')
            translatedbadtracks.append([])
            continue
        gtracks = [(i,g) for i,g in enumerate(uniqgoodtracks) if len(g) > len(b)]
        goodtracks = [g[1] for g in gtracks]
        goodinds = [g[0] for g in gtracks]
        newtracks,ginds = translateBadTrack(b,goodtracks)
        # save the acceptable tracks
        translatedbadtracks.append(newtracks)
        if newtracks ==[]:
            pass
            print('No good tracks found for bad track ' + str(k) + '.')
            if len(b) < 30:
                print(b)
            # print(len(goodtracks))
        else:
            # equally distribute count across allowable tracks
            realgoodinds = [goodinds[j] for j in ginds]
            prop = 1.0 / len(newtracks)
            for i in realgoodinds:
                modifiedgoodcounted[i] += prop*badcounted[k]
    # create dict to store results
    results = {'allgoodtracks':allgoodtracks,'allbadtracks':allbadtracks,'uniqgoodtracks':uniqgoodtracks,'uniqbadtracks':uniqbadtracks,'translatedbadtracks':translatedbadtracks,'goodcounted':goodcounted,'modifiedgoodcounted':modifiedgoodcounted,'badcounted':badcounted,'classes':{'oneloop': [],'oneloopcount': 0,'oneloopcountmodified': 0,'oneloopnote':'Broad One Loops', 'sharponeloop': [],'sharponeloopcount': 0,'sharponeloopcountmodified': 0,'sharponeloopnote':'Sharp One Loops','noloop': [],'noloopcount': 0,'noloopcountmodified': 0,'noloopnote':'Incomplete Loops','periodic': [],'periodiccount': 0,'periodiccountmodified': 0,'periodicnote':'Broad Periodic Loops with < 2 waves','sharpperiodic': [],'sharpperiodiccount': 0,'sharpperiodiccountmodified': 0,'sharpperiodicnote':'Sharp Periodic Loops with < 2 waves','periodictwowaves': [],'periodictwowavescount': 0,'periodictwowavescountmodified': 0,'periodictwowavesnote':'Broad Periodic Loops with >= 2 waves','sharpperiodictwowaves': [],'sharpperiodictwowavescount': 0,'sharpperiodictwowavescountmodified': 0,'sharpperiodictwowavesnote':'Sharp Periodic Loops with >= 2 waves','overlapped': [],'overlappedcount': 0,'overlappedcountmodified': 0,'overlappednote':'Periodic Loops that overlap (double bump waves) with < 2 waves','overlappedtwowaves': [],'overlappedtwowavescount': 0,'overlappedtwowavescountmodified': 0,'overlappedtwowavesnote':'Periodic Loops that overlap (double bump waves) with >= 2 waves','diffequilib':[],'diffequilibcount': 0,'diffequilibcountmodified': 0,'diffequilibnote':'Different Equilibria (stuck in a subloop or at a different fixed pt) with < 1 wave','diffequilibwithwave':[],'diffequilibwithwavecount': 0,'diffequilibwithwavecountmodified': 0,'diffequilibwithwavenote':'Different Equilibria (stuck in a subloop or at a different fixed pt) with >= 1 wave','unclassified': [],'unclassifiedcount': 0,'unclassifiedcountmodified': 0,'unclassifiednote':'Unclassified Tracks'}}
    # only classify unique good tracks
    for k,track in enumerate(uniqgoodtracksdecoded):
        classstr = classifyTrack(track)
        results['classes'][classstr].append(track)
        results['classes'][classstr+'count'] += goodcounted[k]
        results['classes'][classstr+'countmodified'] += modifiedgoodcounted[k]
    return results

def postprocess(myfiles,fname=None):
    results = loadNSort(myfiles)
    if fname:
        cPickle.dump(results,open(fname+'.pickle','w'))
    printme(results)

def cast2Ints(myfile,fname):
    print(myfile)
    of = open(myfile,'r')
    tracks = cPickle.load(of)
    of.close()
    newtracks = []
    for track in tracks:
        track = mN.encodeInts(track)
        newtracks.append(track)
    nf = open(fname,'w')
    cPickle.dump(newtracks,nf)
    nf.close()

def changeFileNames(maindir):
    for f in glob.glob(maindir+'model*tracks*.pickle'):
        if 'int' in f or 'array' in f:
            continue
        else:
            os.rename(f,f[:-7]+'_arrays.pickle')


if __name__ == "__main__":
    maindir = os.path.expanduser('~/SimulationResults/BooleanNetworks/dataset_randinits_biggerx/')
    # for f in glob.glob(maindir+'model*tracks*'):
    #     cast2Ints(f,f[:-7]+'_ints.pickle')
    # changeFileNames(maindir)
    # maindir = os.path.expanduser('~/SimulationResults/BooleanNetworks/dataset_perdt/')
    postprocess(maindir+'model1tracks*_ints.pickle',maindir+'model1Results_ints')
    # postprocess(maindir+'model2tracks*_ints.pickle',maindir+'model2Results_ints')    
    # postprocess(maindir+'model3tracks*_ints.pickle',maindir+'model3Results_ints')    
    # postprocess(maindir+'model4tracks*_ints.pickle',maindir+'model4Results_ints')
    # print('#########################################################')
    # print('Model 1')
    # printme(fname=maindir + 'model1Results_ints.pickle')
    # print('#########################################################')
    # print('Model 2')
    # printme(fname=maindir + 'model2Results_ints.pickle')
    # print('#########################################################')
    # print('Model 3')
    # printme(fname=maindir + 'model3Results_ints.pickle')
    # print('#########################################################')
    # print('Model 4')
    # printme(fname=maindir + 'model4Results_ints.pickle')
