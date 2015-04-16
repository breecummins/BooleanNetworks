import test_hillfunctions as thf
import integratehillfunctions as ihf
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
    f.write('L(X3,X1) 1.0\nU(X3,X1) 2\nT(X3,X1) 3\nL(X2,X1) 1.0\nU(X2,X1) 2\nT(X2,X1) 5\nL(X1,X2) 1\nU(X1,X2) 4\nT(X1,X2) 3\nL(X2,X3) 1\nU(X2,X3) 4\nT(X2,X3) 3')
    f.close()

def runme(writefilefunc,n=4,y0=[0.75,0.75,1.25],t0=0,t1=10,dt=0.01):
    writefilefunc()
    times,funcvals=ihf.simulateHillModel(n,y0,t0,t1,dt)
    ihf.plotResults(times,funcvals,{'linewidth':4,'label':[r'$x_1$',r'$x_2$',r'$x_3$']},{'ncol':3})

if __name__ == '__main__':
    # runme(repressilator,9,[0.75,0.75,1.25],t1=30)
    runme(bistable,10,[2.0,4.0,2.0],t1=30)
