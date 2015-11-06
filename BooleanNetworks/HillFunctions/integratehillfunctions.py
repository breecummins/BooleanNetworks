import numpy as np
from scipy.integrate import ode
import matplotlib.pyplot as plt
import matplotlib
import hillparsers as hp
import constructhillfunctions as chf

font = {'family' : 'normal',
        'size'   : 22}

matplotlib.rc('font', **font)


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

def plainIntegrate(eqns,y0,t0=0,t1=10,dt=0.01):
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

def plotResults(times,funcvals,plotoptions={},legendoptions={},figuresize=()):
    if figuresize:
        plt.figure(figsize=figuresize)
    funcvals=np.array(funcvals)
    if 'label' in plotoptions.keys():
        labels=plotoptions['label']
        del plotoptions['label']
        for k in range(funcvals.shape[1]):
            plt.plot(times,funcvals[:,k],label=labels[k],**plotoptions)
        plt.legend(**legendoptions)
    else:
        plt.plot(times,funcvals,**plotoptions)
    plt.axis('tight')
    plt.show()

        

