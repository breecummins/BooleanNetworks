import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D 
import cPickle,glob, os

def postprocess(myfiles,maindir,fname=None):
    oneloops,numtracks,uoneloops,uoneloopnums,utracks,bitchanges,badoneloopinds,badtrackinds,badtracks = loadNSort(myfiles)
    props = np.array([float(oneloops[k])/numtracks[k] for k in range(len(oneloops))])
    print('Number of tracks')
    print(numtracks)
    print('Number of one-loop tracks')
    print(oneloops)
    print('Proportions of one-loops')
    print(props)
    print('Number of unique tracks (including one loops)')
    print([len(u) for u in utracks])
    print('Number of unique bad tracks (including one loops)')
    olinds=[len(j) for j in bitchanges]
    btinds=[len(j) for j in badtracks]
    print((len(olinds),len(btinds)))
    numbaddies = [olinds[k] + btinds[k] for k in range(len(olinds))]
    print(numbaddies)
    print('Number of unique one-loops')
    print([len(u) for u in uoneloops])
    print('Number of tracks for each unique one-loop')
    print(uoneloopnums)
    print('Index of problem unique one-loops')
    print(bitchanges)
    print('Problem unique one loops')
    for j in range(len(uoneloops)):
        print([uoneloops[j][bitchanges[j][k]] for k in range(len(bitchanges[j]))])
    if fname:
        cPickle.dump({'oneloops':oneloops,'numtracks':numtracks,'props':props,'uoneloops':uoneloops,'uoneloopnums':uoneloopnums,'utracks':utracks},open(os.path.join(maindir,fname+'.pickle'),'w'))
    print('Indices of problem initial conditions in one loops')
    print(badoneloopinds)
    print('Unique indices of problem initial conditions')
    idict = cPickle.load(open(os.path.join(maindir,'inits.pickle'),'r'))
    inits=idict['inits']
    badinds = sorted(list(set([k for j in range(len(badtrackinds)) for k in badtrackinds[j]])))
    print(badinds)
    print('Problem initial conditions')
    print([inits[k,:] for k in badinds])
    return props

def postprocessThrowOut(myfiles,maindir,fname=None):
    oneloops,numtracks,uoneloops,uoneloopnums,goodinds,utracks,badinds,badtracks = loadNSortThrowOut(myfiles)
    props = np.array([float(oneloops[k])/numtracks[k] for k in range(len(oneloops))])
    print('Number of good tracks')
    print(numtracks)
    print('Number of good one-loop tracks')
    print(oneloops)
    print('Proportions of good one-loops')
    print(props)
    print('Number of unique good tracks')
    print([len(u) for u in utracks])
    print('Number of unique bad tracks')
    print([len(b) for b in badtracks])
    print('Number of unique one-loops')
    print([len(u) for u in uoneloops])
    print('Number of tracks for each unique one-loop')
    print(uoneloopnums)
    # print('Bad track inds')
    # print(badinds)
    # # print('Good one-loop tracks')
    # print(uoneloops)
    # print('Good tracks')
    # print(utracks)
    # print('Bad tracks')
    # print(badtracks)
    return props

def postprocessThrowOutCombineParams(myfiles,maindir,numinits,fname=None):
    numtracks,goodinds,goodtracks,badinds,badtracks,oneloops,oneloopnums,onelooptotal,noloops,noloopnums,nolooptotal,periodic,periodicnums,periodictotal,broadperiodic,broadperiodicnums,broadperiodictotal,stuckloops,stuckloopnums,stucklooptotal,misc,miscnums,misctotal = loadNSortThrowOutCombineParams(myfiles,numinits)
    olprops = np.array([float(ol)/numtracks for ol in onelooptotal])
    noprops = np.array([float(no)/numtracks for no in nolooptotal])
    plprops = np.array([float(pl)/numtracks for pl in periodictotal])
    bpprops = np.array([float(bp)/numtracks for bp in broadperiodictotal])
    slprops = np.array([float(sl)/numtracks for sl in stucklooptotal])
    mlprops = np.array([float(ml)/numtracks for ml in misctotal])
    print('Number of good tracks')
    print(numtracks)
    print('Number of bad tracks')
    print(len(badinds))
    print('Number and prop of one-loop tracks; number of unique one loops')
    print((onelooptotal,olprops,[len(ol) for ol in oneloops]))
    print(oneloops)
    print('Number and prop of no-loop tracks; number of unique no loops')
    print((nolooptotal,noprops,[len(ol) for ol in noloops]))
    print('Number and prop of periodic tracks; number of unique periodic tracks')
    print((periodictotal,plprops,[len(ol) for ol in periodic]))
    print('Number and prop of (broadly) periodic tracks; number of unique (broadly) periodic tracks')
    print((broadperiodictotal,bpprops,[len(ol) for ol in broadperiodic]))
    # print(broadperiodic)
    print('Number and prop of stuck-in-a-loop tracks; number of unique stuck-in-a-loop tracks')
    print((stucklooptotal,slprops,[len(ol) for ol in stuckloops]))
    # print(stuckloops)
    print('Number and prop of misc tracks; number of unique misc tracks')
    print((misctotal,mlprops,[len(ol) for ol in misc]))
    # print(misc)

def testBitChanges(uol):
    bitchanges=[]
    for j,u in enumerate(uol):
        if not oneBitFlip(u):
            bitchanges.append(j)
    return bitchanges

def oneBitFlip(ol):
    for k in range(1,ol.shape[0]):
        if (np.abs(ol[k,:]-ol[k-1,:])).sum() > 1:
            return False
    return True


def sortTracks(lot):
    numtracks = len(lot)
    uniqtracks = list(set([tuple(l.flatten()) for l in lot]))
    uniqoneloops = []
    uniqoneloopnums = []
    oneloop = 0
    badtrackinds = []
    badtracks = []
    badoneloopinds = []
    for t,track in enumerate(lot):
        # if the last point in the track is equilibrium, if each of y1,y2,y3 were touched, and if x does not reinitiate, count the track as one loop
        if np.all(track[-1,:]==0) and np.any(track[:,1] ==1) and np.any(track[:,2] ==1) and np.any(track[:,3] ==1) and np.all(track[track[:,0].argmin():,0]==0):
            oneloop += 1
            if not oneBitFlip(track):
                badoneloopinds.append(t)
            if np.all([np.any(track!=u) for u in uniqoneloops]):
                uniqoneloops.append(track)
                uniqoneloopnums.append(1)
            else:
                for k,u in enumerate(uniqoneloops):
                    if np.all(track==u):
                        uniqoneloopnums[k] += 1
        elif not oneBitFlip(track):
            badtrackinds.append(t)
            if np.all([np.any(track!=b) for b in badtracks]):
                badtracks.append(track)
    return oneloop,numtracks,uniqoneloops,uniqoneloopnums,uniqtracks,badoneloopinds,badtrackinds, badtracks

def throwMeOut(lot):
    uniqtracks = []
    goodtrackinds = []
    badtrackinds = []
    badtracks = []
    uniqoneloops = []
    uniqoneloopnums = []
    oneloop = 0
    for t,track in enumerate(lot):
        # if the track has more than one binary flip per change, throw it out
        if not oneBitFlip(track):
            badtrackinds.append(t)
            if np.all([np.any(track!=b) for b in badtracks]):
                badtracks.append(track)
            continue
        else:
            goodtrackinds.append(t)
            if np.all([np.any(track!=u) for u in uniqtracks]):
                uniqtracks.append(track)
        # if the last point in the track is equilibrium, if each of y1,y2,y3 were touched, and if x does not reinitiate, count the track as one loop
        if np.all(track[-1,:]==0) and np.any(track[:,1] ==1) and np.any(track[:,2] ==1) and np.any(track[:,3] ==1) and np.all(track[track[:,0].argmin():,0]==0):
            oneloop += 1
            if np.all([np.any(track!=u) for u in uniqoneloops]):
                uniqoneloops.append(track)
                uniqoneloopnums.append(1)
            else:
                for k,u in enumerate(uniqoneloops):
                    if np.all(track==u):
                        uniqoneloopnums[k] += 1
    numtracks = len(goodtrackinds)
    return oneloop,numtracks,uniqoneloops,uniqoneloopnums,goodtrackinds,uniqtracks,badtrackinds,badtracks

def throwMeOutCombineParams(lot):
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

def loadNSortThrowOut(myfiles):
    oneloops = []
    numtracks = []
    uoneloops = []
    uoneloopnums = []
    goodinds = []
    utracks = []
    badinds = []
    badtracks = []
    for f in glob.glob(myfiles):
        print(f)
        tracks = cPickle.load(open(f,'r'))
        ol,nt,uol,uoln,gti,ut,bti,bt = throwMeOut(tracks)
        oneloops.append(ol)
        numtracks.append(nt)
        uoneloops.append(uol)
        uoneloopnums.append(uoln)
        goodinds.append(gti)
        utracks.append(ut)
        badinds.append(bti)
        badtracks.append(bt)
    return oneloops,numtracks,uoneloops,uoneloopnums,goodinds,utracks,badinds,badtracks

def loadNSort(myfiles):
    oneloops = []
    numtracks = []
    uoneloops = []
    uoneloopnums = []
    utracks = []
    bitchanges = []
    badoneloopinds = []
    badtrackinds = []
    badtracks = []
    for f in glob.glob(myfiles):
        print(f)
        tracks = cPickle.load(open(f,'r'))
        ol,nt,uol,uoln,ut,boli,bti,bt = sortTracks(tracks)
        bc = testBitChanges(uol)
        oneloops.append(ol)
        numtracks.append(nt)
        uoneloops.append(uol)
        uoneloopnums.append(uoln)
        utracks.append(ut)
        bitchanges.append(bc)
        badoneloopinds.append(boli)
        badtrackinds.append(bti)
        badtracks.append(bt)
    return oneloops,numtracks,uoneloops,uoneloopnums,utracks,bitchanges,badoneloopinds,badtrackinds,badtracks

def loadNSortThrowOutCombineParams(myfiles,numinits):
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
    goodtracks = list(set([tuple(g.flatten()) for g in goodtracks]))
    numtracks = len(goodinds)
    print('Analyzing...')
    for tracks in alltracks:
        newtracks = [tracks[k] for k in goodinds]
        ol,oln,olt,nl,nln,nlt,pl,pln,plt,bp,bpn,bpt,sl,sln,slt,ml,mln,mlt = throwMeOutCombineParams(newtracks)
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
    return numtracks,goodinds,goodtracks,badinds,badtracks,oneloops,oneloopnums,onelooptotal,noloops,noloopnums,nolooptotal,periodic,periodicnums,periodictotal,broadperiodic,broadperiodicnums,broadperiodictotal,stuckloops,stuckloopnums,stucklooptotal,misc,miscnums,misctotal

def plot2D(Alist,myfiles,titlestr='Model 1',xlabel='A',ylabel='proportion of single loops'):
    props = postprocess(myfiles)
    plt.figure()
    plt.plot(np.array(Alist),props)
    plt.title(titlestr)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.show()


def plot3D(Alist,Blist,myfiles,titlestr='Model 2',xlabel='A',ylabel='B',zlabel='proportion of single loops'):
    props = postprocess(myfiles)
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    # make sure order is preserved with glob
    newB = Blist*len(Alist)
    newA = []
    for k in range(len(Alist)):
        newA.extend([Alist[k]]*len(Blist))
    ax.plot(np.array(newA),np.array(newB),props)
    plt.title(titlestr)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    ax.set_zlabel(zlabel)
    plt.show()

if __name__ == "__main__":
    # make sure order is preserved with glob
    import os
    # myfiles = os.path.expanduser('~/SimulationResults/BooleanNetworks/dataset1/model1*')
    # plot2D([0.5,1.0,1.5,2.0],myfiles)
    # myfiles = os.path.expanduser('~/SimulationResults/BooleanNetworks/dataset1/model2*')
    # plot3D([0.5,1.0,1.5,2.0],[-0.5,-1.0,-2.0],myfiles)
    # myfiles = os.path.expanduser('~/SimulationResults/BooleanNetworks/dataset1/model3*')
    # plot3D([0.5,1.0,1.5,2.0],[-0.5,-1.0,-2.0],myfiles,'Model 3')
    maindir = os.path.expanduser('~/SimulationResults/BooleanNetworks/dataset_randinits/')
    idict=cPickle.load(open(os.path.join(maindir,'inits.pickle'),'r'))
    numinits = idict['inits'].shape[0]
    # postprocess(maindir + 'model1tracks*',maindir,'model1Results')
    # postprocess(maindir + 'model2tracks*',maindir,'model2Results')
    # postprocess(maindir + 'model3tracks*',maindir, 'model3Results')
    # postprocess(maindir + 'model4tracks*',maindir,'model4Results')
    # postprocessThrowOut(maindir + 'model1tracks*',maindir,'model1Results')
    # postprocessThrowOut(maindir + 'model2tracks*',maindir,'model2Results')
    # postprocessThrowOut(maindir + 'model3tracks*',maindir,'model3Results')
    # postprocessThrowOut(maindir + 'model4tracks*',maindir,'model4Results')
    # postprocessThrowOutCombineParams(maindir + 'model1tracks*',maindir,numinits,'model1Results')
    # postprocessThrowOutCombineParams(maindir + 'model2tracks*',maindir,numinits,'model2Results')    
    postprocessThrowOutCombineParams(maindir + 'model3tracks*',maindir,numinits,'model3Results')    
    # postprocessThrowOutCombineParams(maindir + 'model4tracks*',maindir,numinits,'model4Results')