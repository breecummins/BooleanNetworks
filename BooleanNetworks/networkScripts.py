import numpy as np
import os, random, cPickle, importlib
from functools import partial
import translations as trans
import modelNetworks5D as mod5D
import modelNetworks4D as mod4D
import rk4

def solveModel(init,finaltime,model,dt=0.01,stoppingcriteria=[None]):
    times = np.arange(0,finaltime,dt)
    timeseries = [np.array(init)]
    if stoppingcriteria[0] != None:
        for k,ti in enumerate(times[:-1]):
            timeseries.append(rk4.solver(ti,timeseries[k],dt,model))
            if np.mod(k,50) == 0 and np.any([tuple(np.int8(timeseries[-1] > 0)) == sc for sc in stoppingcriteria]):
                print('Reached equilibrium orthant. Stopping time integration at {0:0.02f}.'.format(ti))
                break
    else:
        for k,ti in enumerate(times[:-1]):
            timeseries.append(rk4.solver(ti,timeseries[k],dt,model))        
    return np.array(timeseries)

def solveAndSave(inits,model,fname,dt=0.01,finaltime=5.0,stoppingcriteria=[None]):    
    tracks = []
    for k in range(inits.shape[0]):
        ts = solveModel(inits[k,:],finaltime,model,dt,stoppingcriteria)
        t = trans.translateToOrthants(ts)
        tracks.append(trans.encodeInts(t))
    fname += '.pickle'
    cPickle.dump(tracks,open(fname, 'w'))

def makeParamSets(maindir,module=mod5D,numinits=20000,dt=0.01,finaltime=5.0,stoppingcriteria=[None]):
    if 'inits.pickle' not in os.listdir(maindir):
        print('Generating new initial conditions...')
        inits = -2.1 + 2*np.random.random((numinits,5))
        inits[:,0] = 10.0 - 9*np.random.random((numinits,))
        cPickle.dump(inits,open(os.path.join(maindir,'inits.pickle'), 'w'))
    else:
        print('Using existing initial conditions file...')
        inits=cPickle.load(open(os.path.join(maindir,'inits.pickle'),'r'))
    # make paramchanges
    # make list of models using module
    for i,params in enumerate(paramchanges):
        for k,model in enumerate(models):
        #construct param dict
            print('Model {0}, parameter set {1} of {2}'.format(k,i,len(paramchanges)))
            fname=os.path.join(maindir,'model{0}tracks{1:02d}'.format(k,i))
            solveAndSave(inits,partial(model,**params),fname,dt=dt,finaltime=finaltime,stoppingcriteria=stoppingcriteria)

if __name__ == "__main__":
    pass