import numpy as np
import itertools
from functools import partial
from BooleanNetworks.networkScripts import solveModel
import StateSpace.fileops as fileops
import StateSpace.StateSpaceReconstructionPlots as SSRPlots

def model(t,y,A=0,B=0,C=0,D=0,E=0,F=0):
    # y = x, y1, y2, z
    dy = -y + 0.1
    xamp = E*(y[0] > 2)*(y[2] < 1)*(y[3] < 1) + A*(y[0] < 2)*(y[2] > 1)*(y[3] < 1) + (A+E)*(y[0] > 2)*(y[2] > 1)*(y[3] < 1) + E*F*(y[0] > 2)*(y[2] < 1)*(y[3] > 1) + A*F*(y[0] < 2)*(y[2] > 1)*(y[3] > 1) + (A+E)*F*(y[0] > 2)*(y[2] > 1)*(y[3] > 1)
    dy[0] += xamp
    dy[1] += B*(y[0] > 3)
    dy[2] += C*(y[1] > 1)
    dy[3] += D*(y[0] > 1)
    return dy

def runModel():
    initx = np.arange(3.1,3.9,.3)
    init = np.arange(0.6,1.4,.3)
    finaltime = 20.0
    TS = []
    for i in [[2.4,1.7,6.0,0]]:#itertools.product(initx,init,init,[0]):
        ts = solveModel(i,finaltime,partial(model,A=3.1,B=0.75,C=0.75,D=0.75,E=1.555,F=0.3),dt=0.05)
        TS.append(ts)
    fileops.dumpPickle({'TS':TS},'/Users/bcummins/Desktop/odesForTomas')

def vizTraj(inds=None):
    d = fileops.loadPickle('/Users/bcummins/Desktop/odesForTomas')
    if inds is None:
        inds = range(len(d['TS']))
    for k in inds:
        ts = d['TS'][k]
        s = ts.shape
        print(ts[0,:])
        SSRPlots.plotManifold(ts[:,:3],show=1)


if __name__ == '__main__':
    # runModel()
    vizTraj()
