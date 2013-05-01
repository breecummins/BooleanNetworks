import numpy as np
import os
import cPickle
from functools import partial
import modelNetworks as mN

def partitionOrthant(model=mN.model1,fname=os.path.expanduser('~/temp/model1tracks'),orthrange = np.arange(0.0,-2.1,-0.2),finaltime=5.0):
    tracks = []
    for i in orthrange:
        for j in orthrange:
            for k in orthrange:
                for l in orthrange:
                    init = np.array([1.0,i,j,k,l])
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
            mod5=partial(mN.model5,L0=L0,L4=L4)
            fname5=os.path.expanduser('~/temp/model5tracksA'+str(k)+'B'+str(j))
            partitionOrthant(mod5,fname5)
 
if __name__ == "__main__":
        alterParams()