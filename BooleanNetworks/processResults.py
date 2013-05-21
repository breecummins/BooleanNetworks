import numpy as np
import cPickle,glob, os, itertools

def postprocess(myfiles,maindir,numinits,fname=None):
    results = loadNSort(myfiles,numinits)
    N = results['numtracks']
    results['oneloopprops'] = np.array([float(ol)/N for ol in results['onelooptotal']])
    results['noloopprops'] = np.array([float(no)/N for no in results['nolooptotal']])
    results['perprops'] = np.array([float(pl)/N for pl in results['periodictotal']])
    results['broadperprops'] = np.array([float(bp)/N for bp in results['broadperiodictotal']])
    results['stuckloopprops'] = np.array([float(sl)/N for sl in results['stucklooptotal']])
    results['miscprops'] = np.array([float(ml)/N for ml in results['misctotal']])
    if fname:
        cPickle.dump(results,open(os.path.join(maindir,fname+'.pickle'),'w'))
    printme(results)
    combineParamsWithinModel(results)

def printme(results=None,fname=None):
    if fname:
        results = cPickle.load(open(fname,'r'))
    print('Number of good initial conditions')
    print(results['numtracks'])
    print('Number of unique good tracks')
    print(len(results['goodtracks']))
    print('Number of bad initial conditions')
    print(len(results['badinds']))
    print('Number of unique bad tracks')
    print(len(results['badtracks']))
    print('Number and prop of one-loop tracks; number of unique one loops')
    print((results['onelooptotal'],results['oneloopprops'],[len(ol) for ol in results['oneloops']]))
    # print(results['oneloops'][2])
    print('Number and prop of no-loop tracks; number of unique no loops')
    print((results['nolooptotal'],results['noloopprops'],[len(ol) for ol in results['noloops']]))
    print('Number and prop of periodic tracks; number of unique periodic tracks')
    print((results['periodictotal'],results['perprops'],[len(ol) for ol in results['periodic']]))
    print('Number and prop of (broadly) periodic tracks; number of unique (broadly) periodic tracks')
    print((results['broadperiodictotal'],results['broadperprops'],[len(ol) for ol in results['broadperiodic']]))
    print('Number and prop of stuck-in-a-loop tracks; number of unique stuck-in-a-loop tracks')
    print((results['stucklooptotal'],results['stuckloopprops'],[len(ol) for ol in results['stuckloops']]))
    # print(results['stuckloops'])
    print('Number and prop of misc tracks; number of unique misc tracks')
    print((results['misctotal'],results['miscprops'],[len(ol) for ol in results['misc']]))

def combineParamsWithinModel(results=None,fname=None):
    if fname:
        results = cPickle.load(open(fname,'r'))
    N = float(results['numtracks']*len(results['onelooptotal']))
    percentoneloops = sum(results['onelooptotal'])*100.0 / N
    percentnoloops = sum(results['nolooptotal'])*100.0 / N
    percentperiodic = (sum(results['periodictotal'])+sum(results['broadperiodictotal']))*100.0 / N  
    percentcrash = sum(results['stucklooptotal'])*100.0 / N
    print('Percentage of one loops')
    print("%0.2f %%" % percentoneloops)
    print('Percentage of no loops')
    print("%0.2f %%" % percentnoloops)
    print('Percentage of periodic loops')
    print("%0.2f %%" % percentperiodic)
    print('Percentage of crashes')  
    print("%0.2f %%" % percentcrash)

def broadWaves(results=None,fname=None):
    if fname:
        results = cPickle.load(open(fname,'r'))
    broadwave = np.ones(4)
    uniqoneloopbroadwaves = []
    totaloneloopbroadwaves = 0
    for j,lol in enumerate(results['oneloops']):
        for k,ol in enumerate(lol):
            if np.any([np.all(step[:-1] == broadwave) for step in ol]):
                totaloneloopbroadwaves += results['oneloopnums'][j][k]
                if np.all([np.any(ol!=u) for u in uniqoneloopbroadwaves]):
                    uniqoneloopbroadwaves.append(ol)
    uniqperiodicbroadwaves = []
    totalperiodicbroadwaves = 0
    for j,lol in enumerate(results['periodic']):
        for k,ol in enumerate(lol):
            if np.any([np.all(step[:-1] == broadwave) for step in ol]):
                totalperiodicbroadwaves += results['periodicnums'][j][k]
                if np.all([np.any(ol!=u) for u in uniqperiodicbroadwaves]):
                    uniqperiodicbroadwaves.append(ol)
    for j,lol in enumerate(results['broadperiodic']):
        for k,ol in enumerate(lol):
            if np.any([np.all(step[:-1] == broadwave) for step in ol]):
                totalperiodicbroadwaves += results['broadperiodicnums'][j][k]
                if np.all([np.any(ol!=u) for u in uniqperiodicbroadwaves]):
                    uniqperiodicbroadwaves.append(ol)
    numparams = len(results['onelooptotal'])
    N = float(results['numtracks']*numparams)
    print('Number of unique one loop broad waves')
    print(len(uniqoneloopbroadwaves))
    print('Total number of one loop broad waves in the population of ' + str(int(N)) + ' good tracks')
    print(totaloneloopbroadwaves)
    print('Total number of one loops  in the population of ' + str(int(N)) + ' good tracks')
    numoneloop = float(sum([sum(results['oneloopnums'][j]) for j in range(numparams)]))
    print(int(numoneloop))
    print('Proportion of one loop broad waves in the population of ' + str(int(N)) + ' good tracks')
    print(totaloneloopbroadwaves/N)
    if numoneloop > 0:
        print('Proportion of one loop broad waves in the (good) one loop population')
        print(totaloneloopbroadwaves/numoneloop)
    print('Number of unique periodic broad waves')
    print(len(uniqperiodicbroadwaves))
    print('Total number of periodic broad waves in the population of ' + str(int(N)) + ' good tracks')
    print(totalperiodicbroadwaves)
    print('Total number of periodic waves  in the population of ' + str(int(N)) + ' good tracks')
    numperiodic = float(sum([sum(results['periodicnums'][j]) for j in range(numparams)])+sum([sum(results['broadperiodicnums'][j]) for j in range(numparams)]))
    print(int(numperiodic))
    print('Proportion of periodic broad waves in the population of ' + str(int(N)) + ' good tracks')
    print(totalperiodicbroadwaves/N)
    if numperiodic >0:
        print('Proportion of periodic broad waves in the (good) periodic population')
        print(totalperiodicbroadwaves/numperiodic)
 
def eqClasses(results=None,fname=None):
    if fname:
        results = cPickle.load(open(fname,'r'))
    # pre-sort good tracks for comparison
    # gtracks = sorted(results['goodtracks'],key=len)
    glens = np.array(sorted(list(set([len(g) for g in results['goodtracks']]))))
    gtracks = [[g for g in results['goodtracks'] if len(g)==k] for k in glens]
    equivcls = []
    for b in results['badtracks']:
        inds = []
        steps = []
        # find where b is bad and calculate intermediate steps
        for k in range(1,b.shape[0]):
            diff = b[k,:]-b[k-1,:]
            localinds = np.nonzero(diff)[0]
            N = len(localinds)
            if N > 1:
                inds.append(k)
                perms = itertools.permutations(localinds)
                templist = []
                for p in perms:
                    temp = np.zeros((N-1,b.shape[1]))
                    temp += b[k-1,:] 
                    for i,j in enumerate(p[:-1]):
                        temp[i:,j] += diff[j]
                    # # remove disallowed tracks - can't go through equilibrium and can't go immediately back through the prior step
                    # # Now doing this by comparing to good tracks, which I have to do anyway 
                    # if np.all([np.any(temp[j,:] != 0) for j in range(temp.shape[0])]):
                    #     if k == 1 or np.any(temp[0,:] != b[k-2,:]):
                    #         if k == b.shape[0]-1 or np.any(temp[-1,:] != b[k+1,:]):
                    #             templist.append(temp)
                    templist.append(temp)
                steps.append(templist)
        # make a template for the equivalence classes of b
        newpts = [s[0].shape[0] for s in steps]
        template = np.zeros((b.shape[0]+sum(newpts),b.shape[1]))
        replinds = []
        for k in range(len(inds)):
            replinds.append((inds[k]+sum(newpts[:k]),inds[k]+sum(newpts[:k+1]))) 
        myinds = [0]+inds+[b.shape[0]]
        for k,i in enumerate(myinds[1:]):
            template[myinds[k]+sum(newpts[:k]):i+sum(newpts[:k]),:] = b[myinds[k]:i,:]
        # construct the equivalence classes for b and remove ones not in goodtracks
        gind = np.nonzero(glens == template.shape[0])[0]
        blist = []
        stepinds = [range(len(s)) for s in steps]
        combos=itertools.product(*stepinds)
        for c in combos:
            tp = template.copy()
            for k in range(len(replinds)):
                r = replinds[k]
                step = steps[k]
                tp[r[0]:r[1],:] = step[c[k]]
            if np.any([np.all(tp==g) for g in gtracks[gind]]):
                blist.append(tp)
        if len(inds) > 1:
            print('More than one bad step')
            print(b)
            # print(blist)
        if any([len(s) > 2 for s in steps]):
            print('More than two bit flips')
            print(b)  
            # print(blist)          
        equivcls.append(blist)
    return equivcls

def oneBitFlip(ol):
    for k in range(1,ol.shape[0]):
        if (np.abs(ol[k,:]-ol[k-1,:])).sum() > 1:
            return False
    return True

def sortTracks(lot):
    oneloops = []
    oneloopnums = []
    onelooptotal = 0
    noloops = []
    noloopnums = []
    nolooptotal = 0
    periodic = []
    periodicnums = []
    periodictotal = 0
    stuckloops = []
    stuckloopnums = []
    stucklooptotal = 0
    misc = []
    miscnums = []
    misctotal = 0
    broadperiodic = []
    broadperiodicnums = []
    broadperiodictotal = 0
    def addme(track,loop,nums,total):
        total += 1
        if np.all([np.any(track!=o) for o in loop]):
            loop.append(track)
            nums.append(1)
        else:
            for k,u in enumerate(loop):
                if np.all(track==u):
                    nums[k] += 1
                    break
        return loop,nums,total
    for track in lot:
        # if the last point in the track is equilibrium, if each of y1,y2,y3 were touched, and if x does not reinitiate, count the track as one loop
        if np.all(track[-1,:]==0) and np.any(track[:,1] ==1) and np.any(track[:,2] ==1) and np.any(track[:,3] ==1) and np.all(track[track[:,0].argmin():,0]==0):
            oneloops,oneloopnums,onelooptotal = addme(track,oneloops,oneloopnums,onelooptotal)
        # if not a single loop is completed, count as no loops
        elif np.all(track[track[:,0].argmin():,0]==0) and (np.all(track[:,1] ==0) or np.all(track[:,2] ==0) or np.all(track[:,3] ==0)):
            noloops,noloopnums,nolooptotal = addme(track,noloops,noloopnums,nolooptotal)
        # if the initial condition is reached again and if each of y1,y2,y3 were touched, count as periodic
        elif np.any(track[:,1] ==1) and np.any(track[:,2] ==1) and np.any(track[:,3] ==1) and np.any([np.all(t == np.array([1,0,0,0,0])) for t in track[track[:,0].argmin():,:]]):
            periodic,periodicnums,periodictotal = addme(track,periodic,periodicnums,periodictotal)
        # if x is reinitialized and if each of y1,y2,y3 were touched and the last point is at equilibrium, count as periodic (in a broad sense)
        elif np.any(track[:,1] ==1) and np.any(track[:,2] ==1) and np.any(track[:,3] ==1) and np.any(track[track[:,0].argmin():,0] == 1) and np.all(track[-1,:]==0):
            broadperiodic,broadperiodicnums,broadperiodictotal = addme(track,broadperiodic,broadperiodicnums,broadperiodictotal)
        # if the last time step is not at equilibrium, count as stuck in a subloop
        elif np.any(track[-1,:] != 0):
            stuckloops,stuckloopnums,stucklooptotal = addme(track,stuckloops,stuckloopnums,stucklooptotal)
        else:
            misc,miscnums,misctotal = addme(track,misc,miscnums,misctotal)
    return oneloops,oneloopnums,onelooptotal,noloops,noloopnums,nolooptotal,periodic,periodicnums,periodictotal,broadperiodic,broadperiodicnums,broadperiodictotal,stuckloops,stuckloopnums,stucklooptotal,misc,miscnums,misctotal

def loadNSort(myfiles,numinits):
    numtracks = []
    goodinds = []
    goodtracks = []
    badinds = []
    badtracks = []
    oneloops = []
    oneloopnums = []
    onelooptotal = []
    noloops = []
    noloopnums = []
    nolooptotal = []
    periodic = []
    periodicnums = []
    periodictotal = []
    broadperiodic = []
    broadperiodicnums = []
    broadperiodictotal = []
    stuckloops = []
    stuckloopnums = []
    stucklooptotal = []
    misc = []
    miscnums = []
    misctotal = []
    alltracks = []
    print('Loading...')
    for f in glob.glob(myfiles):
        print(f)
        tracks = cPickle.load(open(f,'r'))
        alltracks.append(tracks)
        for t,track in enumerate(tracks):
            if not oneBitFlip(track):
                badinds.append(t)
                if np.all([np.any(track!=b) for b in badtracks]):
                    badtracks.append(track)
                continue
            else:
                if np.all([np.any(track!=g) for g in goodtracks]):
                    goodtracks.append(track)
    badinds = sorted(list(set(badinds)))
    goodinds = range(numinits)
    for b in badinds:
        goodinds.remove(b)
    badtracks = list(set([tuple(b.flatten()) for b in badtracks]))
    bt = [np.array(t).reshape(-1,5) for t in badtracks]
    badtracks = bt
    goodtracks = list(set([tuple(g.flatten()) for g in goodtracks]))
    gt = [np.array(t).reshape(-1,5) for t in goodtracks]
    goodtracks = gt
    numtracks = len(goodinds)
    print('Analyzing...')
    for tracks in alltracks:
        newtracks = [tracks[k] for k in goodinds]
        ol,oln,olt,nl,nln,nlt,pl,pln,plt,bp,bpn,bpt,sl,sln,slt,ml,mln,mlt = sortTracks(newtracks)
        oneloops.append(ol)
        oneloopnums.append(oln)
        onelooptotal.append(olt)
        noloops.append(nl)
        noloopnums.append(nln)
        nolooptotal.append(nlt)
        periodic.append(pl)
        periodicnums.append(pln)
        periodictotal.append(plt)
        broadperiodic.append(bp)
        broadperiodicnums.append(bpn)
        broadperiodictotal.append(bpt)
        stuckloops.append(sl)
        stuckloopnums.append(sln)
        stucklooptotal.append(slt)
        misc.append(ml)
        miscnums.append(mln)
        misctotal.append(mlt)
    results = {'oneloops':oneloops,'oneloopnums':oneloopnums,'onelooptotal':onelooptotal,'noloops':noloops,'noloopnums':noloopnums,'nolooptotal':nolooptotal,'periodic':periodic,'periodicnums':periodicnums,'periodictotal':periodictotal,'broadperiodic':broadperiodic,'broadperiodicnums':broadperiodicnums,'broadperiodictotal':broadperiodictotal,'stuckloops':stuckloops,'stuckloopnums':stuckloopnums,'stucklooptotal':stucklooptotal,'misc':misc,'miscnums':miscnums,'misctotal':misctotal,'numtracks':numtracks,'goodinds':goodinds,'goodtracks':goodtracks,'badinds':badinds,'badtracks':badtracks}
    return results

if __name__ == "__main__":
    maindir = os.path.expanduser('~/SimulationResults/BooleanNetworks/dataset_randinits_biggerx/')
    # idict=cPickle.load(open(os.path.join(maindir,'inits.pickle'),'r'))
    # numinits = idict['inits'].shape[0]
    # maindir = os.path.expanduser('~/SimulationResults/BooleanNetworks/dataset_perdt/')
    # numinits = 14641
    # postprocess(maindir + 'model1tracks*',maindir,numinits,'model1Results')
    # postprocess(maindir + 'model2tracks*',maindir,numinits,'model2Results')    
    # postprocess(maindir + 'model3tracks*',maindir,numinits,'model3Results')    
    # postprocess(maindir + 'model4tracks*',maindir,numinits,'model4Results')
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
    # print('#########################################################')
    # print('Model 1')
    # combineParamsWithinModel(fname=maindir + 'model1Results.pickle')
    # print('#########################################################')
    # print('Model 2')
    # combineParamsWithinModel(fname=maindir + 'model2Results.pickle')
    # print('#########################################################')
    # print('Model 3')
    # combineParamsWithinModel(fname=maindir + 'model3Results.pickle')
    # print('#########################################################')
    # print('Model 4')
    # combineParamsWithinModel(fname=maindir + 'model4Results.pickle')
    # print('#########################################################')
    # print('Model 1')
    # broadWaves(fname=maindir + 'model1Results.pickle')
    # print('#########################################################')
    # print('Model 2')
    # broadWaves(fname=maindir + 'model2Results.pickle')
    # print('#########################################################')
    # print('Model 3')
    # broadWaves(fname=maindir + 'model3Results.pickle')
    # print('#########################################################')
    # print('Model 4')
    # broadWaves(fname=maindir + 'model4Results.pickle')
    # print('#########################################################')
    # print('Model 1')
    # results = cPickle.load(open(maindir + 'model1Results.pickle','r'))
    # eqc = eqClasses(results)
    # print('All corrected tracks')
    # for k in range(len(eqc)):
    #     print(results['badtracks'][k])
    #     print(eqc[k])
    # print('#########################################################')
    # print('Model 2')
    # results = cPickle.load(open(maindir + 'model2Results.pickle','r'))
    # eqc = eqClasses(results)
    # print('All corrected tracks')
    # for k in range(len(eqc)):
    #     print(results['badtracks'][k])
    #     print(eqc[k])
    print('#########################################################')
    print('Model 3')
    results = cPickle.load(open(maindir + 'model3Results.pickle','r'))
    eqc = eqClasses(results)
    print('All corrected tracks')
    ingoodtracks = [np.zeros(len(eqc[k])) for k in range(len(eqc))]
    for k in range(len(eqc)):
        print(results['badtracks'][k])
        print(eqc[k])
    #     for j,e in enumerate(eqc[k]):
    #         if np.any([np.all(e == g) for g in results['goodtracks']]):
    #             ingoodtracks[k][j] += 1
    # print(ingoodtracks)
    # print('#########################################################')
    # print('Model 4')
    # results = cPickle.load(open(maindir + 'model4Results.pickle','r'))
    # eqc = eqClasses(results)
    # print('All corrected tracks')
    # for k in range(len(eqc)):
    #     print(results['badtracks'][k])
    #     print(eqc[k])
    # 