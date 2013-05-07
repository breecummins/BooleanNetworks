import numpy as np
import os, glob, random, cPickle
from functools import partial
import modelNetworks as mN

def partitionOrthant(model=mN.model1,fname=os.path.expanduser('~/temp/model1tracks'),orthrange = np.arange(0.1,-2.2,-0.2),finaltime=5.0):
    per=[0.0,0.005,0.01,0.015]
    tracks = []
    for i in orthrange:
        for j in orthrange:
            for k in orthrange:
                for l in orthrange:
                    random.shuffle(per)
                    init = np.array([1.0,i+per[0],j+per[1],k+per[2],l+per[3]])
                    ts = mN.solveModel(init,finaltime,model)
                    tracks.append(mN.translateToOrthants(ts))
    fname += '.pickle'
    cPickle.dump(tracks,open(fname,'w'))

def alterParams(Alist=[0.5,1.0,1.5,2.0],Blist=[-0.5,-1.0,-2.0]):
    for k,A in enumerate(Alist):
        L0 = partial(mN.L0,A0=A)
        fname1=os.path.expanduser('~/temp/model1tracksA'+str(k))
        mod1 = partial(mN.model1,L0=L0)
        partitionOrthant(mod1,fname1)
        for j,B in enumerate(Blist):
            L4 =partial(mN.L0,A0=1.0,B0=B,C0=2.0,D0=1.0)
            fname2=os.path.expanduser('~/temp/model2tracksA'+str(k)+'B'+str(j))
            mod2=partial(mN.model2,L0=L0,L4=L4)
            partitionOrthant(mod2,fname2)
            mod3=partial(mN.model3,L0=L0,L4=L4)
            fname3=os.path.expanduser('~/temp/model3tracksA'+str(k)+'B'+str(j))
            partitionOrthant(mod3,fname3)
            newL4=partial(mN.L4,B0=B)
            mod4=partial(mN.model4,L0=L0,L4=newL4)
            fname4=os.path.expanduser('~/temp/model4tracksA'+str(k)+'B'+str(j))
            partitionOrthant(mod4,fname4)

def sortTracks(lot):
    numtracks = len(lot)
    uniqtracks = list(set([tuple(l.flatten()) for l in lot]))
    uniqoneloops = []
    oneloop = 0
    for track in lot:
        # if the last point in the track is equilibrium, if each of y1,y2,y3 were touched, and if x does not reinitiate, count the track as one loop
        if np.all(track[-1,:]==0) and np.any(track[:,1] ==1) and np.any(track[:,2] ==1) and np.any(track[:,3] ==1) and np.all(track[track[:,0].argmin():,0]==0):
            oneloop += 1
            if np.all([np.any(track!=u) for u in uniqoneloops]):
                uniqoneloops.append(track)
    return oneloop,numtracks,uniqoneloops,uniqtracks

def loadNSort(myfiles):
    oneloops = []
    numtracks = []
    uoneloops = []
    utracks = []
    for f in glob.glob(myfiles):
        print(f)
        tracks = cPickle.load(open(f,'r'))
        ol,nt,uol,ut = sortTracks(tracks)
        oneloops.append(ol)
        numtracks.append(nt)
        uoneloops.append(uol)
        utracks.append(ut)
    return oneloops,numtracks,uoneloops,utracks

if __name__ == "__main__":
        alterParams()