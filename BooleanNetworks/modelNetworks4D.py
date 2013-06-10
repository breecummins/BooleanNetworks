import rk4
import numpy as np
from functools import partial
from modelNetworks import translateToOrthants, encodeInts, decodeInts, solveModel

def L0(y,z,thresh_y=1.0-1.5,thresh_z=1.0-0.5,A=0.5,B=1.0,C=2.0):
    if y > thresh_y and z > thresh_z:
        return -(A+C)
    elif y <= thresh_y and z > thresh_z:
        return -(B+C)
    elif y > thresh_y and z <= thresh_z:
        return 0
    else:
        return -C

def L1(x,thresh=1.0-2.0,A=1.5):
    if x > thresh:
        return 0.0
    else:
        return -A

def model1(t,y,L0=L0, L1=L1, L2=partial(L1,thresh=1.0-1.5), L3=partial(L1,A=0.5)):
    dy = -y
    dy[0] += L0(y[2],y[3])
    dy[1] += L1(y[0])
    dy[2] += L2(y[1])
    dy[3] += L3(y[2])
    return dy

if __name__ == '__main__':
    finaltime = 10.0
    init=np.array([3.0,-0.19,-0.2,-0.21])
    ts = solveModel(init,finaltime,model1,dt=0.05)
    s = translateToOrthants(ts)
    i = encodeInts(s)
    print(ts)

