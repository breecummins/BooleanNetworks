import integratehillfunctions as ihf
import constructhillfunctions as chf
import numpy as np
from scipy.integrate import ode

class testcase(object):
    def __init__(self):
        self.writeFiles()

    def writeFiles(self):
        pass

    def analyticRHS(self,t,x,n):
        pass

    def evalAnalytic(self,n,y0,t0,t1,dt):
        r = ode(self.analyticRHS).set_integrator('vode', method='bdf')
        r.set_initial_value(y0,t0).set_f_params(n)
        return ihf.integrate(r,y0,t0,t1,dt)

class test2D(testcase):
    def __init__(self):
        testcase.__init__(self)

    def writeFiles(self):
        f=open('equations.txt','w')
        f.write('X1 : (X1)(~X2) : X1 X2\nX2 : X1 : X1')
        f.close()
        f=open('samples.txt','w')
        f.write('L(X1,X1) 1.2\nU(X1,X1) 3.4\nT(X1,X1) 1.5\nL(X2,X1) 1.0\nU(X2,X1) 2.5\nT(X2,X1) 5.0\nL(X1,X2) 4.1\nU(X1,X2) 6.2\nT(X1,X2) 2.0')
        f.close()

    def analyticRHS(self,t,x,n):
        return np.array([-x[0]+chf.posHillFunction(3.4,1.2,1.5,n,x[0])*chf.negHillFunction(2.5,1.0,5.0,n,x[1]),-x[1]+chf.posHillFunction(6.2,4.1,2.0,n,x[0])])

class testrepressilator(testcase):
    def __init__(self):
        testcase.__init__(self)

    def writeFiles(self):
        f=open('equations.txt','w')
        f.write('X : ~Z : Y\nY : ~X : Z\nZ : ~Y : X')
        f.close()
        f=open('samples.txt','w')
        f.write('L(X,Y) 1.2\nU(X,Y) 3.4\nT(X,Y) 1.5\nL(Y,Z) 1.0\nU(Y,Z) 2.5\nT(Y,Z) 2.4\nL(Z,X) 0.6\nU(Z,X) 2.1\nT(Z,X) 2.0')
        f.close()

    def analyticRHS(self,t,x,n):
        return np.array([-x[0]+chf.negHillFunction(2.1,0.6,2.0,n,x[2]),-x[1]+chf.negHillFunction(3.4,1.2,1.5,n,x[0]),-x[2]+chf.negHillFunction(2.5,1.0,2.4,n,x[1])])


class test4DCycle(testcase):
    def __init__(self):
        testcase.__init__(self)

    def writeFiles(self):
        f=open('equations.txt','w')
        f.write('X1 : (X1)(~X2 + ~X4) : X1 X2 X4 \nX2 : (X1)(~X3) : X1 X3 \nX3 : X2 : X2 X4 \nX4 : (X1)(~X3) : X1')
        f.close()
        f=open('samples.txt','w')
        f.write('U(X1,X1) 3.4\nL(X1,X1) 1.2\nT(X1,X1) 1.5\nU(X2,X1) 3.1\nL(X2,X1) 1.7\nT(X2,X1) 5.0\nU(X4,X1) 4.6\nL(X4,X1) 2.2\nT(X4,X1) 1.0\nU(X1,X2) 6.2\nL(X1,X2) 4.1\nT(X1,X2) 2.7\nU(X3,X2) 9.2\nL(X3,X2) 5.2\nT(X3,X2) 10.8\nU(X2,X3) 11.0\nL(X2,X3) 7.0\nT(X2,X3) 7.0\nU(X1,X4) 2.3\nL(X1,X4) 0.2\nT(X1,X4) 3.9\nU(X3,X4) 1.5\nL(X3,X4) 0.6\nT(X3,X4) 11.3')
        f.close()

    def analyticRHS(self,t,x,n):
        return np.array([-x[0]+chf.posHillFunction(3.4,1.2,1.5,n,x[0])*(chf.negHillFunction(3.1,1.7,5.0,n,x[1]) + chf.negHillFunction(4.6,2.2,1.0,n,x[3])),-x[1]+chf.posHillFunction(6.2,4.1,2.7,n,x[0])*chf.negHillFunction(9.2,5.2,10.8,n,x[2]),-x[2]+chf.posHillFunction(11.0,7.0,7.0,n,x[1]),-x[3]+chf.posHillFunction(2.3,0.2,3.9,n,x[0])*chf.negHillFunction(1.5,0.6,11.3,n,x[2])])

def compare(test,n,y0,t0=0,t1=10,dt=0.01):
    times,funcvals=ihf.simulateHillModel(n,y0,t0,t1,dt)
    ihf.plotResults(times,funcvals)
    times,funcvals=test.evalAnalytic(n,y0,t0,t1,dt)
    ihf.plotResults(times,funcvals)

if __name__=='__main__':
    n=20
    T=test2D()
    y0=np.array([1,1])
    T=testrepressilator()
    y0=np.array([1,1,1])
    T=test4DCycle()
    y0=np.array([1,1,1,1])
    compare(T,n,y0)