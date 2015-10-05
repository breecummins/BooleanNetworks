import numpy as np
from functools import partial
import HeavisideFunctions as HF

L0R=partial(HF.Repress,beta=20.0,K=4.0) # model 1
L0AR=partial(HF.ActivatePlusRepress,alpha=20.0,beta=5.0,K=10.0) # model 1.5, 2
L1=partial(HF.Activate,alpha=20.0,K=4.0) # all
L2=partial(HF.Activate,alpha=20.0,K=10.0) # all
L3A=partial(HF.Activate,alpha=10.0,K=4.0) # model 1.5
L3AA=partial(HF.ActivatePlusActivate,alpha1=10.0,alpha2=10.0,K=4.0) # model 1, 2

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

if __name__ == '__main__':
    import translations as trans
    from networkScripts import solveModel
    finaltime = 10.0
    dt=0.01
    L0ARrev=partial(HF.ActivatePlusRepress,alpha=5.0,beta=20.0,K=10.0) # model 1.5, 2
    L0Rrev=partial(HF.Repress,beta=5.0,K=10.0)
    init=np.array([6.,-3.,-9.,-3.9])
    # init=np.array([10.,-2.5,-1.5,-1.0])
    # init=np.array([1.,-2.5,-1.5,-1.0])
    # init=np.array([10.,-1.0,-1.5,-1.0])

    print('###################################')
    print('Model 1, negative')
    ts = solveModel(init,finaltime,partial(model1,L0=L0Rrev),dt=dt)
    # print(ts)
    s = trans.translateToOrthants(ts)
    print(s)
    i = trans.encodeInts(s,4)
    print(i)

    print('###################################')
    print('Model 1, positive')
    ts = solveModel(init,finaltime,model1,dt=dt)
    # print(ts)
    s = trans.translateToOrthants(ts)
    print(s)
    i = trans.encodeInts(s,4)
    print(i)

    # print('###################################')
    # print('Model 1.5')
    # ts = solveModel(init,finaltime,partial(model1dot5,L0=L0ARrev),dt=dt)
    # # print(ts)
    # s = trans.translateToOrthants(ts)
    # print(s)
    # i = trans.encodeInts(s,4)
    # print(i)

    # print('###################################')
    # print('Model 2')
    # ts = solveModel(init,finaltime,partial(model2,L0=L0ARrev),dt=dt)
    # # print(ts)
    # s = trans.translateToOrthants(ts)
    # print(s)
    # i = trans.encodeInts(s,4)
    # print(i)
