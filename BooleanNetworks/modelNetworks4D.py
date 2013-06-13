import rk4
import numpy as np
from functools import partial
import translations as trans
import HeavisideFunctions as HF

L1=partial(HF.Activate,alpha=20.0,K=4.0)
L2=partial(HF.Activate,alpha=20.0,K=10.0)
L0R=partial(HF.Repress,beta=20.0,K=4.0)
L0AR=partial(HF.ActivatePlusRepress,alpha=10.0,beta=20.0,K=4.0)
L3A=partial(HF.Activate,alpha=10.0,K=4.0)
L3AA=partial(HF.ActivatePlusActivate,alpha1=10.0,alpha2=10.0,K=4.0)

def model1(t,y,L0=L0R, L1=L1, L2=L2, L3=L3AA):
    dy = -y
    dy[0] += L0(y[3])
    dy[1] += L1(y[0])
    dy[2] += L2(y[1])
    dy[3] += L3(y[0],y[2])
    return dy

def model1dot5(t,y,L0=L0AR, L1=L1, L2=L2, L3=L3A):
    dy = -y
    dy[0] += L0(y[2],y[3])
    dy[1] += L1(y[0])
    dy[2] += L2(y[1])
    dy[3] += L3(y[0])
    return dy

def model2(t,y,L0=L0AR, L1=L1, L2=L2, L3=L3AA):
    dy = -y
    dy[0] += L0(y[2],y[3])
    dy[1] += L1(y[0])
    dy[2] += L2(y[1])
    dy[3] += L3(y[0],y[2])
    return dy

def solveModel(init,finaltime,model,dt=0.01,stoppingcriteria=[None]):
    times = np.arange(0,finaltime,dt)
    timeseries = [np.array(init)]
    for k,ti in enumerate(times[:-1]):
        timeseries.append(rk4.solverp(ti,timeseries[k],dt,model))
        if np.mod(k,50) == 0 and np.any([tuple(np.int8(timeseries[-1] > 0)) == sc for sc in stoppingcriteria]):
            print('Reached equilibrium orthant. Stopping time integration at {0:0.02f}.'.format(ti))
            break
    return np.array(timeseries)

if __name__ == '__main__':
    finaltime = 10.0
    dt=0.01
    init=np.array([6.,-3.,-9.,-3.9])
    # init=np.array([10.,-2.5,-1.5,-1.0])
    # init=np.array([1.,-2.5,-1.5,-1.0])
    # init=np.array([10.,-1.0,-1.5,-1.0])

    print('###################################')
    print('Model 1')
    ts = solveModel(init,finaltime,model1,dt=dt)
    # print(ts)
    s = trans.translateToOrthants(ts)
    print(s)
    i = trans.encodeInts(s,4)
    print(i)

    print('###################################')
    print('Model 1.5')
    ts = solveModel(init,finaltime,model1dot5,dt=dt)
    # print(ts)
    s = trans.translateToOrthants(ts)
    print(s)
    i = trans.encodeInts(s,4)
    print(i)

    print('###################################')
    print('Model 2')
    ts = solveModel(init,finaltime,model2,dt=dt)
    # print(ts)
    s = trans.translateToOrthants(ts)
    print(s)
    i = trans.encodeInts(s,4)
    print(i)
