import numpy as np
import cPickle, glob, os, itertools
import modelNetworks as mN

#Note: This code might run into problems between little-endian and big-endian architectures. I haven't noticed any issues so far.

def countme(results):
    Ngood = float(len(results['allgoodtracks']))
    Ntotal = Ngood + len(results['allbadtracks'])
    tbt = []
    uniquntranslatedcount = 0
    totaluntranslatedcount = 0
    for k,t in enumerate(results['translatedbadtracks']):
        tbt.extend(t)
        if t == []:
            uniquntranslatedcount += 1
            totaluntranslatedcount += results['badcounted'][k]
    Ntotalmodified = Ntotal - totaluntranslatedcount
    utbt,_=countClass(tbt)
    uniqbad2goodtranslatedcount = len(utbt)
    return uniqbad2goodtranslatedcount,uniquntranslatedcount,totaluntranslatedcount,Ntotal,Ngood,Ntotalmodified


def printme(results=None,fname=None):
    if fname:
        results = cPickle.load(open(fname, 'r'))
    uniqbad2goodtranslatedcount,uniquntranslatedcount,totaluntranslatedcount,Ntotal,Ngood,Ntotalmodified = countme(results)
    print('Total number of tracks across parameter space')
    print(int(Ntotal))
    print('Total number of good tracks')
    print(int(Ngood))
    print('Number of unique good tracks')
    print(len(results['uniqgoodtracks']))
    print('Number of unique bad tracks')
    print(len(results['uniqbadtracks']))
    print('Number of unique good tracks from translating bad tracks')
    print(uniqbad2goodtranslatedcount)
    print('Number of unique untranslated bad tracks')
    print(uniquntranslatedcount)
    print('Total number of untranslated bad tracks')
    print(totaluntranslatedcount)
    print('Modified number of total tracks across parameter space')
    print(Ntotalmodified)
    
    Keys = ['sharponeloop','oneloop','sharpperiodictwowaves','sharpperiodic','periodictwowaves','periodic','overlappedtwowaves','overlapped','diffequilibwithwave','diffequilib','noloop','unclassified']

    for k in Keys:
        if 'count' not in k and 'note' not in k:
            print('Number of unique ' + results['classes'][k + 'note'])
            print(len(results['classes'][k]))
            if len(results['classes'][k]) > 0:
                ex = int(np.floor(len(results['classes'][k])*np.random.rand()))
                print('Example: ' + str(results['classes'][k][ex]))
            # if k == 'diffequilibwithwave':
            #     for x in results['classes'][k]:
            #         print(x)
            #     # print([mN.decodeInts(x) for x in results['classes'][k]])

    for k in Keys:
        if 'count' not in k and 'note' not in k and len(results['classes'][k]) > 0:
            print(results['classes'][k + 'note'] + ': # good tracks; prop in good tracks; # good + translated; prop in total')
            print((results['classes'][k+'count'],results['classes'][k+'count']/Ngood,results['classes'][k + 'countmodified'],results['classes'][k + 'countmodified']/Ntotalmodified))

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
            vals = [ x & adjxor for x in [16,8,4,2,1] if x & adjxor > 0 ]
            signedvals = [-v if v & badtrack[k-1] else v for v in vals]
            perms = itertools.permutations(signedvals)
            steps = [[badtrack[k-1]+sum(p[:j]) for j in range(1,len(p))] for p in perms]
            newchunks.append(steps)
    # cut the bad track into sections divided by the locations with > 1 bit flip
    goodchunks = []
    myinds = [0]+inds+[len(badtrack)]
    for k in range(len(myinds)-1):
        goodchunks.append(list(badtrack[myinds[k]:myinds[k+1]]))
    # construct the candidate good tracks chunk by chunk and match to good tracks or quit
    chunkinds = range(0,len(newchunks),2) + [len(newchunks)]
    cands = [list(goodchunks[0])]
    newtracks = []
    goodinds = []
    for k,i in enumerate(chunkinds[1:]):
        newcands = []
        subchunks = newchunks[chunkinds[k]:i]
        stepopts = [range(len(c)) for c in subchunks]
        combos=itertools.product(*stepopts)
        for c in combos:
            for poss in cands:
                t = list(poss)
                for j in range(len(subchunks)):
                    steps = subchunks[j]
                    t += steps[c[j]]
                    t += goodchunks[chunkinds[k]+j+1]
                tt = tuple(t)
                for gi,g in enumerate(goodtracks):
                    if i < len(newchunks) and tt == g[:len(tt)]:
                        newcands.append(t)
                        break
                    elif i == len(newchunks) and tt == g:
                        newtracks.append(tt)
                        goodinds.append(gi)
                        break
        if newcands == []:
            break
        else:
            cands = list(newcands)
    return newtracks, goodinds


def classifyTrack(track):
    # define a function to find index of x's first zero and first reinitialization of x 
    def findzeroone(track=track):
        try:
            firstzero = [16 & x for x in track].index(0) 
        except:
            firstzero = None
        try:
            nextone = firstzero + [16 & x for x in track[firstzero:]].index(16)
        except:
            nextone = None
        return firstzero, nextone
    ###### Find first x zero and first x reinitialization if they exist #######
    firstzero, nextone = findzeroone()
    # define a function that can identify a completed wave
    def completedwave(track=track, firstzero=firstzero, nextone=nextone):
        # x has to turn off
        if firstzero == None:
            return False
        # y1, y2, and y3 have to turn on
        if any([8 & x for x in track[firstzero:nextone]]) and any([4 & x for x in track[firstzero:nextone]]) and any([2 & x for x in track[firstzero:nextone]]):
            return True
        else:
            return False
    # function to identify sharp waves (no more than two of x,y1,y2,y3 are activated at a time)
    def issharp(track=track):
        # Note that 13 and 11 are not checked because they are double-bump waves
        newtrack = [ x >> 1 for x in track] #bit shift to remove z
        if any([x & 14 == 14 for x in newtrack]): #x,y1,y2
            return False
        elif any([x & 7 == 7 for x in newtrack]): #y1,y2,y3
            return False
        else:
            return True
    ###### Now classify the track ######
    # if not a single loop is completed, count as no loops 
    if not completedwave(nextone=len(track)):
        return 'noloop'
    # if the last track step is not at [0,0,0,0,0], then the track is either stuck in a subloop (unstable limit cycle) or is at a different fixed pt (I assume sufficient simulation time)
    elif track[-1] != 0:
        # if there is a completed wave at the beginning, record it
        if completedwave():
            return 'diffequilibwithwave'
        else:
            return 'diffequilib'
    # if x does not reinitiate, count the track as one loop
    elif nextone == None:
        # if the wave is sharp, record it
        if issharp():
            return 'sharponeloop'
        else:    
            return 'oneloop'
    # if the initial condition is reached after first wave, count as periodic
    elif track[nextone+1] == 16:
        # if there are at least two completed loops, record it
        subtrack = track[nextone+1:]
        stfz,stno= findzeroone(subtrack)
        if completedwave(subtrack,stfz,stno):
            # if the wave is sharp, record it
            if issharp():
                return 'sharpperiodictwowaves'
            else:    
                return 'periodictwowaves'
        else:
            # if the wave is sharp, record it
            if issharp():
                return 'sharpperiodic'
            else:    
                return 'periodic'
    # if x is reinitialized but initial condition does not recur immediately after the first wave, count as overlapping wave (last wave didn't finish before new one began)
    elif any([x & 16 for x in track[firstzero:]]):
        # if there are at least two completed loops, record it
        subtrack = track[nextone+1:]
        stfz,stno= findzeroone(subtrack)
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
    try:
        tracks = cPickle.load(open(myfiles,'r'))
        print(myfiles)
        for track in tracks:
            if not oneBitFlip(track):
                allbadtracks.append(track)
            else:
                allgoodtracks.append(track)
    except:     
        for f in glob.glob(myfiles):
            print(f)
            tracks = cPickle.load(open(f,'r'))
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
    translatedbadtracks = []
    modifiedgoodcounted = list(goodcounted) #this points to a new list
    longestgoodtrack = max([len(g) for g in uniqgoodtracks])
    for k,b in enumerate(uniqbadtracks):
        if len(b) >= longestgoodtrack:
            # print('Bad track of length ' + str(len(b)) + ' is too long. Skipping track ' + str(k) + '.')
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
            # print('No good tracks found for bad track ' + str(k) + '.')
            # if len(b) < 30:
            #     print(b)
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
    for k,track in enumerate(uniqgoodtracks):
        classstr = classifyTrack(track)
        results['classes'][classstr].append(track)
        results['classes'][classstr+'count'] += goodcounted[k]
        results['classes'][classstr+'countmodified'] += modifiedgoodcounted[k]
    return results

def postprocess(myfiles,fname=None):
    results = loadNSort(myfiles)
    if fname:
        cPickle.dump(results,open(fname,'w'))
    printme(results)

def cast2Ints(myfile,fname):
    print(myfile)
    tracks = cPickle.load(open(myfile,'r'))
    newtracks = []
    for track in tracks:
        track = mN.encodeInts(track)
        newtracks.append(track)
    cPickle.dump(newtracks,open(fname,'w'))

def changeFileNames(maindir):
    for f in glob.glob(maindir+'model*tracks*.pickle'):
        if 'int' in f or 'array' in f:
            continue
        else:
            os.rename(f,f[:-7]+'_arrays.pickle')


if __name__ == "__main__":
    maindir = os.path.expanduser('~/SimulationResults/BooleanNetworks/dataset_randinits_x1to10/')
    for k in range(1,5):
        for myfile in glob.glob(maindir+'model{0!s}tracks*.pickle'.format(k)):
            if '_results' != myfile:
                savefile = myfile[:-7] + '_results'
                postprocess(myfile,savefile)

    # # for f in glob.glob(maindir+'model*tracks*'):
    # #     cast2Ints(f,f[:-7]+'_ints.pickle')
    # # changeFileNames(maindir)
    # # maindir = os.path.expanduser('~/SimulationResults/BooleanNetworks/dataset_perdt/')
    # # postprocess(maindir+'model1tracks*.pickle',maindir+'model1Results')
    # # postprocess(maindir+'model2tracks*.pickle',maindir+'model2Results')    
    # # postprocess(maindir+'model3tracks*.pickle',maindir+'model3Results')    
    # # postprocess(maindir+'model4tracks*.pickle',maindir+'model4Results')
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
