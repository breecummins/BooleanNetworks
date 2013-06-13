import rk4
import numpy as np
from functools import partial
import HeavisideFunctions as HF

L1=partial(HF.Activate,alpha=20.0,K=4.0)
L2=partial(HF.Activate,alpha=20.0,K=10.0)
L3=partial(HF.Activate,alpha=20.0,K=10.0)
L0R=partial(HF.Repress,beta=20.0,K=4.0)
L0AR=partial(HF.ActivatePlusRepress,alpha=10.0,beta=20.0,K=4.0)
L4A=partial(HF.Activate,alpha=10.0,K=4.0)
L4AA=partial(HF.ActivatePlusActivate,alpha1=10.0,alpha2=10.0,K=4.0)
L4AAR=partial(HF.ActivatePlusActivatePlusRepress,alpha1=10.0,alpha2=10.0,beta=20.0,K=4.0)


def model1(t,y,L0=L0AR, L1=L1, L2=L2, L3=L3, L4=L4A):
    dy = -y
    dy[0] += L0(y[3],y[4])
    dy[1] += L1(y[0])
    dy[2] += L2(y[1])
    dy[3] += L3(y[2])
    dy[4] += L4(y[0])
    return dy

def model2(t,y,L0=L0AR, L1=L1, L2=L2, L3=L3, L4=L4AA):
    dy = -y
    dy[0] += L0(y[3],y[4])
    dy[1] += L1(y[0])
    dy[2] += L2(y[1])
    dy[3] += L3(y[2])
    dy[4] += L4(y[0],y[2])
    return dy

def model2dot5(t,y,L0=L0R, L1=L1, L2=L2, L3=L3, L4=L4AA):
    dy = -y
    dy[0] += L0(y[4])
    dy[1] += L1(y[0])
    dy[2] += L2(y[1])
    dy[3] += L3(y[2])
    dy[4] += L4(y[0],y[2])
    return dy

def model3(t,y,L0=L0AR, L1=L1, L2=L2, L3=L3, L4=L4AA):
    dy = -y
    dy[0] += L0(y[3],y[4])
    dy[1] += L1(y[0])
    dy[2] += L2(y[1])
    dy[3] += L3(y[2])
    dy[4] += L4(y[0],y[3])
    return dy

def model3dot5(t,y,L0=L0R, L1=L1, L2=L2, L3=L3, L4=L4AA):
    dy = -y
    dy[0] += L0(y[4])
    dy[1] += L1(y[0])
    dy[2] += L2(y[1])
    dy[3] += L3(y[2])
    dy[4] += L4(y[0],y[3])
    return dy

def model4(t,y,L0=L0AR, L1=L1, L2=L2, L3=L3, L4=L4AAR):
    dy = -y
    dy[0] += L0(y[3],y[4])
    dy[1] += L1(y[0])
    dy[2] += L2(y[1])
    dy[3] += L3(y[2])
    dy[4] += L4(y[0],y[2],y[3])
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

if __name__=='__main__':
    from translations import translateToOrthants, translateDerivativesToOrthants,encodeInts, decodeInts
    finaltime = 5.0
    # #periodic loop
    # init = np.array([1.0,0.1,0.1,0.1,-1.0])
    # init = np.array([0.1,1.0,1.0,1.0,-0.1])
    # ts = solveModel(init,finaltime,model5)
    # s = translateToOrthants(ts)
    # print(s)
    # # model 2 robust to init conditions example
    # for i in [1.0,1.5,2.0,3.0]:
    #     init = np.array([i,-0.5,-0.1,-0.1,-0.1])
    #     ts = solveModel(init,finaltime,model1)
    #     # print(ts)
    #     s = translateToOrthants(ts)
    #     print('Model 1, initial x = ' + str(i))
    #     print(s)
    #     print('******************')
    # for i in [1.0,1.5,2.0,3.0,10.0]:
    #     init = np.array([i,-0.5,-0.1,-0.1,-0.1])
    #     ts = solveModel(init,finaltime,model2)
    #     # print(ts)
    #     s = translateToOrthants(ts)
    #     print('Model 2, initial x = ' + str(i))
    #     print(s)
    #     print('******************')

    # #symmetry
    # init=np.array([1.0,-0.2,-0.2,-0.2,-0.2])
    # ts = solveModel(init,finaltime,model3)
    # s = translateToOrthants(ts)
    # print(ts[:20])
    # print(s)

    # init=np.array([1.0,-0.1,-0.2,-0.2,-0.2])
    # ts = solveModel(init,finaltime,model3)
    # s = translateToOrthants(ts)
    # print(ts[:20])
    # print(s)

    # init=np.array([1.0,-1.0,-0.9,-0.8,-0.2])
    # ts = solveModel(init,finaltime,model4)
    # s = translateToOrthants(ts)
    # print(ts[-50:])
    # print(s)

    # init=np.array([1.0,-0.1,-0.1,-0.1,-0.2])
    # ts = solveModel(init,finaltime,model4)
    # s = translateToOrthants(ts)
    # print(ts[:20])
    # print(s)

    # init=np.array([1.0,-0.19,-0.2,-0.22,-0.21])
    # ts = solveModel(init,finaltime,model1)
    # s = translateToOrthants(ts)
    # i = encodeInts(s)
    # si = decodeInts(i)
    # print(ts[-25:])
    # # print(ts)
    # print(s)
    # # print(i)
    # # print(si)

    init=np.array([3.0,-0.19,-0.2,-0.22,-0.21])
    dt = 0.01
    ts = solveModel(init,finaltime,model4,dt=dt,stoppingcriteria=[(0,0,0,0,0),(1,1,1,1,0)])
    s = translateDerivativesToOrthants(ts,dt)
    i = encodeInts(s)
    si = decodeInts(i)
    print(ts[-50:])
    # print(ts)
    print(s)
    # print(i)
    # print(si)

