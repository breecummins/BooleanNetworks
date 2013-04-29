import rk4
import numpy as np
from functools import partial

def L1(x,A1=1.0,B1=1.0):
    if x > 0:
        return A1
    else:
        return -B1

def L0(y,z,A0=1.0,B0=0.5,C0=0.75,D0=1.0):
    if y >0 and z <=0:
        return A0
    elif y <=0 and z<=0:
        return -B0
    elif y>0 and z>0:
        return -C0
    else:
        return -D0

def model1(t,y,L0=L0, L1=L1, L2=L1, L3=L1, L4=L1):
    dy = -y
    dy[0] += L0(y[3],y[4])
    dy[1] += L1(y[0])
    dy[2] += L2(y[1])
    dy[3] += L3(y[2])
    dy[4] += L4(y[0])
    return dy

def solveModel1(init,finaltime,dt=0.01):
    times = np.arange(0,finaltime,dt)
    timeseries = np.zeros((len(times),len(init)))
    timeseries[0,:] = init
    for k,ti in enumerate(times[:-1]):
        timeseries[k+1,:] = rk4.solverp(ti,timeseries[k,:],dt,model1)
    return timeseries

def translateToOrthants(timeseries):
    trajectory = (timeseries > 0).astype(int)
    short = trajectory[0,:].reshape((1,timeseries.shape[1]))
    for k in range(1,timeseries.shape[0]):
        if np.any(trajectory[k,:] != short[-1,:]):
            short = np.vstack([short,trajectory[k,:]])
    return short

if __name__=='__main__':
    init = np.array([1.0,0.0,0.0,0.0,0.0])
    finaltime = 5.0
    ts = solveModel1(init,finaltime)
    print(ts)
    s = translateToOrthants(ts)
    print(s)
