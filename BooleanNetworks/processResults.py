import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D 
import cPickle,glob, os

def postprocess(myfiles,maindir,fname=None):
    oneloops,numtracks,uoneloops,uoneloopnums,utracks,bitchanges,badtrackinds = loadNSort(myfiles)
    props = np.array([float(oneloops[k])/numtracks[k] for k in range(len(oneloops))])
    print('Number of tracks')
    print(numtracks)
    print('Number of one-loop tracks')
    print(oneloops)
    print('Proportions of one-loops')
    print(props)
    print('Number of unique tracks')
    print([len(u) for u in utracks])
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
    print('Indices of problem initial conditions')
    print(badtrackinds)
    print('Unique indices of problem initial conditions')
    idict = cPickle.load(open(os.path.join(maindir,'inits.pickle'),'r'))
    inits=idict['inits']
    badinds = sorted(list(set([k for j in range(len(badtrackinds)) for k in badtrackinds[j]])))
    print(badinds)
    print('Problem initial conditions')
    print([inits[k,:] for k in badinds])
    return props

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
    for t,track in enumerate(lot):
        # if the last point in the track is equilibrium, if each of y1,y2,y3 were touched, and if x does not reinitiate, count the track as one loop
        if np.all(track[-1,:]==0) and np.any(track[:,1] ==1) and np.any(track[:,2] ==1) and np.any(track[:,3] ==1) and np.all(track[track[:,0].argmin():,0]==0):
            oneloop += 1
            if not oneBitFlip(track):
                badtrackinds.append(t)
            if np.all([np.any(track!=u) for u in uniqoneloops]):
                uniqoneloops.append(track)
                uniqoneloopnums.append(1)
            else:
                for k,u in enumerate(uniqoneloops):
                    if np.all(track==u):
                        uniqoneloopnums[k] += 1
    return oneloop,numtracks,uniqoneloops,uniqoneloopnums,uniqtracks,badtrackinds

def loadNSort(myfiles):
    oneloops = []
    numtracks = []
    uoneloops = []
    uoneloopnums = []
    utracks = []
    bitchanges = []
    badtrackinds = []
    for f in glob.glob(myfiles):
        print(f)
        tracks = cPickle.load(open(f,'r'))
        ol,nt,uol,uoln,ut,bti = sortTracks(tracks)
        bc = testBitChanges(uol)
        oneloops.append(ol)
        numtracks.append(nt)
        uoneloops.append(uol)
        uoneloopnums.append(uoln)
        utracks.append(ut)
        bitchanges.append(bc)
        badtrackinds.append(bti)
    return oneloops,numtracks,uoneloops,uoneloopnums,utracks,bitchanges,badtrackinds

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
    # postprocess(maindir + 'model1tracks*',maindir,'model1Results')
    postprocess(maindir + 'model2tracks*',maindir,'model2Results')
    # postprocess(maindir + 'model3tracks*',maindir, 'model3Results')
    # postprocess(maindir + 'model4tracks*',maindir,'model4Results')
