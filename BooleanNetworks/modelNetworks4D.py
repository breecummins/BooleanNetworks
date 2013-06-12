import rk4
import numpy as np
from functools import partial
from translations import translateToOrthants, encodeInts, decodeInts

def L0(y2,z,alpha0=None,beta0=20.0,K1=4.0):
    if y2 > 0 and z > 0:
        return alpha0 - K3
    elif y2 <= 0 and z > 0:
        return -K1
    elif y2 > 0 and z <= 0:
        return beta0 + alpha0 - K1
    else:
        return beta0 - K1

def LR(z,beta=20.0,K1=4.0):
    if z > 0:
        return -K
    else:
        return alpha-K

def L1(x,alpha=20,K=4.0):
    if x > 0:
        return alpha-K
    else:
        return -K

def L3(x,y2,alpha3=None,alpha4=None,R0=4.0):
    if x > 0 and y2 > 0:
        return alpha3 + alpha4 - R0
    elif x > 0 and y2 <= 0:
        return alpha3 - R0
    elif x <= 0 and y2 > 0:
        return alpha4 - R0
    else:
        return -R0

def model1(t,y,L0=LR, L1=L1, L2=partial(L1,K=10.0), L3=L3):
    dy = -y
    dy[0] += L0(y[3])
    dy[1] += L1(y[0])
    dy[2] += L2(y[1])
    dy[3] += L3(y[0],y[2])
    return dy

def model1dot5(t,y,L0=L0, L1=L1, L2=partial(L1,K=10.0), L3=partial(L1,alpha=None)):
    dy = -y
    dy[0] += L0(y[2],y[3])
    dy[1] += L1(y[0])
    dy[2] += L2(y[1])
    dy[3] += L3(y[0])
    return dy

def model2(t,y,L0=L0, L1=L1, L2=partial(L1,K=10.0), L3=L3):
    dy = -y
    dy[0] += L0(y[2],y[3])
    dy[1] += L1(y[0])
    dy[2] += L2(y[1])
    dy[3] += L3(y[0],y[2])
    return dy

def solveModel(init,finaltime,model,dt=0.01,stoppingcriteria=[(0,0,0,0,0)]):
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
    ts = solveModel(init,finaltime,partial(model1,L0=partial(L0,alpha14=4.0),L3=partial(L1,alpha=2.0,thresh=1.0)),dt=dt)
    # print(ts)
    s = translateToOrthants(ts)
    print(s)
    i = encodeInts(s,4)
    print(i)

    ts = solveModel(init,finaltime,partial(model2,L0=partial(L0,alpha14=5.0),L3=partial(L3,alpha21=20.0,alpha22=20.0)),dt=dt)
    # print(ts)
    s = translateToOrthants(ts)
    print(s)
    i = encodeInts(s,4)
    print(i)
