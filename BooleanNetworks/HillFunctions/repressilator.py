import test_hillfunctions as thf
import integratehillfunctions as ihf
import constructhillfunctions as chf
import matplotlib
font = {'family' : 'normal','weight' : 'bold','size'   : 22}
matplotlib.rc('font', **font)

def repressilator():
    f=open('equations.txt','w')
    f.write('X1 : ~X3 : X2\nX2 : ~X1 : X3\nX3 : ~X2 : X1')
    f.close()
    f=open('samples.txt','w')
    f.write('L(X3,X1) 0.5\nU(X3,X1) 1.5\nT(X3,X1) 1\nL(X1,X2) 0.5\nU(X1,X2) 1.5\nT(X1,X2) 1.0\nL(X2,X3) 0.5\nU(X2,X3) 1.5\nT(X2,X3) 1.0')
    f.close()

def bistable():
    f=open('equations.txt','w')
    f.write('X1 : (~X3)(~X2) : X2\nX2 : ~X1 : X3 X1\nX3 : ~X2 : X1')
    f.close()
    f=open('samples.txt','w')
    f.write('L(X3,X1) 1.0\nU(X3,X1) 3\nT(X3,X1) 2\nL(X2,X1) 1.0\nU(X2,X1) 2\nT(X2,X1) 6\nL(X1,X2) 1\nU(X1,X2) 5\nT(X1,X2) 4\nL(X2,X3) 1\nU(X2,X3) 4\nT(X2,X3) 3')
    f.close()

def runme(writefilefunc,n=4,y0=[0.75,0.75,1.25],t0=0,t1=10,dt=0.01):
    writefilefunc()
    times,funcvals=ihf.simulateHillModel(n,y0,t0,t1,dt)
    ihf.plotResults(times,funcvals,{'linewidth':4,'label':[r'$x_1$',r'$x_2$',r'$x_3$']},{'ncol':3})

def bistablecheck(n=7,y0=[0.75,0.75,1.25],t0=0,t1=10,dt=0.01):
    eqns=[ lambda X: - X[0] + chf.negHillFunction(2,1,6,n,X[1])*chf.negHillFunction(3,1,2,n,X[2]), lambda X: - X[1] + chf.negHillFunction(5,1,4,n,X[0]), lambda X: - X[2] + chf.negHillFunction(4,1,3,n,X[1])]
    times,funcvals=ihf.plainIntegrate(eqns,y0,t0,t1,dt)
    ihf.plotResults(times,funcvals,{'linewidth':4,'label':[r'$x_1$',r'$x_2$',r'$x_3$']},{'ncol':3})


if __name__ == '__main__':
    # runme(repressilator,9,[0.75,0.75,1.25],t1=30)
    # runme(bistable,7,[2.0,5.0,1.0],t1=30)
    bistablecheck(6,[2.0,5.0,1.0],t1=3000)
