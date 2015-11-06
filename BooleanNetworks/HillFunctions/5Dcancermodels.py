import numpy as np
from scipy.integrate import ode
import integratehillfunctions as ihf
import constructhillfunctions as chf

def RHS_5D_2015_10_21(t,x,n):
    xdot=np.zeros(x.shape)
    xdot[0] = -x[0] + (chf.posHillFunction(7./8,7./32,3./4,n[0][0],x[2]) + chf.posHillFunction(7./8,7./32,1./4,n[0][1],x[1]))*chf.negHillFunction(7./8,21./32,1.0,n[0][2],x[4])
    xdot[1] = -x[1] + chf.negHillFunction(1.0,1./8,0.5,n[1][0],x[3])
    xdot[2] = -x[2] + chf.posHillFunction(1.0,0.5,0.5,n[2][0],x[1])*chf.negHillFunction(1.0,0.5,2.0,n[2][1],x[3])
    xdot[3] = -x[3] + chf.posHillFunction(1.0,0.25,539./512,n[3][0],x[0])
    xdot[4] = -x[4] + chf.posHillFunction(2,0.5,1127./1024,n[4][0],x[0])
    return xdot

def simulate(RHS,y0,t0=0,t1=200,dt=0.01,hillexp=10):
    r = ode(RHS).set_integrator('vode', method='bdf').set_f_params(hillexp)
    r.set_initial_value(y0,t0)
    return ihf.integrate(r,y0,t0,t1,dt)

def runme(RHS=RHS_5D_2015_10_21,t1=200,hillexp=10,plotoptions={},legendoptions={},figuresize=(15,10)):
    y0=np.array([1,1,1,1,1])
    t,y=simulate(RHS,y0,t1=t1,hillexp=hillexp)
    ihf.plotResults(t,y,plotoptions,legendoptions,figuresize)

if __name__=='__main__':
    runme(t1=50,hillexp=((2,2,2),(10,),(10,2),(10,),(2,)), plotoptions={'linewidth':2,'label':['p53','ATM','Chk2','Wip1','Mdm2']},legendoptions={'fontsize':24,'loc':'upper left', 'bbox_to_anchor':(1, 1)})

    runme(t1=50,hillexp=((3,3,3),(8,),(8,3),(8,),(3,)), plotoptions={'linewidth':2,'label':['p53','ATM','Chk2','Wip1','Mdm2']},legendoptions={'fontsize':24,'loc':'upper left', 'bbox_to_anchor':(1, 1)})
