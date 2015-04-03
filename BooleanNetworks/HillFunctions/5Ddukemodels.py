import numpy as np
from scipy.integrate import ode
import integratehillfunctions as ihf
import constructhillfunctions as chf

def RHS5pt1(t,x):
    xdot=np.zeros(x.shape)
    xdot[0] = 0.1 - 0.06*x[0] + chf.negHillFunctionForDuke(50,400,4,x[3])
    xdot[1] = 0.1 - 0.06*x[1] + chf.posHillFunctionForDuke(50,400,4,x[0])
    xdot[2] = 0.1 - 0.06*x[2] + chf.posHillFunctionForDuke(25,300,4,x[1]) + chf.posHillFunctionForDuke(25,300,4,x[0])
    xdot[3] = 0.1 - 0.06*x[3] + chf.posHillFunctionForDuke(25,300,4,x[2]) + chf.posHillFunctionForDuke(25,300,4,x[1])
    xdot[4] = 0.1 - 0.06*x[4] + chf.posHillFunctionForDuke(50,400,4,x[3])
    return xdot

def simulate(RHS,y0,t0=0,t1=200,dt=0.01):
    r = ode(RHS).set_integrator('vode', method='bdf')
    r.set_initial_value(y0,t0)
    return ihf.integrate(r,y0,t0,t1,dt)

def run5pt1():
    y0=np.array([198,162,321,503,638])
    # y0=np.array([1,1,1,1,1])
    t,y=simulate(RHS5pt1,y0)
    ihf.plotResults(t,y)

if __name__=='__main__':
    run5pt1()

