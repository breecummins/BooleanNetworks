import numpy as np
from scipy.integrate import ode
import matplotlib.pyplot as plt
import hillparsers as hp
import constructhillfunctions as chf

def RHS(t,x,eqns):
    xdot = [e(x) for e in eqns]
    return np.array(xdot)

def simulateHillModel(n,y0,t0=0,t1=10,dt=0.01):
    eqnstr,varnames=hp.parseEqns()
    params,vals=hp.parseSamples(varnames)
    eqns=chf.makeHillEqns(eqnstr,params,vals,n)
    r = ode(RHS).set_integrator('vode', method='bdf')
    r.set_initial_value(y0,t0).set_f_params(eqns)
    return integrate(r,y0,t0,t1,dt)

def integrate(r,y0,t0,t1,dt):
    times=[t0]
    funcvals=[y0]
    while r.successful() and r.t < t1:
        r.integrate(r.t+dt)
        times.append(r.t)
        funcvals.append(r.y)
    return times,funcvals

def plotResults(times,funcvals,plotoptions={}):
    funcvals=np.array(funcvals)
    if 'label' in plotoptions.keys():
        labels=plotoptions['label']
        del plotoptions['label']
        for k in range(funcvals.shape[1]):
            plt.plot(times,funcvals[:,k],label=labels[k],**plotoptions)
        plt.legend()
    else:
        plt.plot(times,funcvals,**plotoptions)
    plt.show()

        

