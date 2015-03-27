import numpy as np
from scipy.integrate import ode
import matplotlib.pyplot as plt

def parseEqns(fname='equations.txt'):
    f=open(fname,'r')
    varnames=[]
    eqns=[]
    for l in f:
        L=l.split(' : ')
        varnames.append(L[0])
        eqns.append(L[1])
    f.close()
    inteqns=[]
    for e in eqns:
        for k,v in enumerate(varnames):
            e=e.replace('~'+v,str(k)+' n').replace(v,str(k)+' p').replace(')(',')*(')
        inteqns.append(e)
    return inteqns,varnames

def parseSamples(varnames,fname='samples.txt'):
    f=open(fname,'r')
    params=[]
    vals=[]
    for l in f:
        L=l.split()
        params.append(L[0])
        vals.append(float(L[1]))
    f.close()
    intparams=[]
    for p in params:
        for k,v in enumerate(varnames):
            p=p.replace(v,str(k))
        intparams.append(p)
    return intparams,vals

def posHillFunction(U,L,T,n,X):
    return (U-L) * X**n / (X**n + T**n) + L
    
def negHillFunction(U,L,T,n,X):
    return (U-L) * T**n / (X**n + T**n) + L

def RHS(t,x,eqns,params,vals,n):
    # D has eqns and params and vals and 'n'
    xdot = np.zeros(x.shape)
    for k,e in enumerate(eqns):
        for j in range(len(eqns)):
            if str(j)+' ' in e: 
                U,L,T=None,None,None
                for p,v in zip(params,vals):
                    if p=='U('+str(j)+','+str(k)+')':
                        U=v
                    elif p=='L('+str(j)+','+str(k)+')':  
                        L=v
                    elif p=='T('+str(j)+','+str(k)+')':
                        T=v
                    if U is not None and L is not None and T is not None:
                        break
                e=e.replace(str(j)+' n',"negHillFunction("+str(U)+","+str(L)+','+str(T)+","+str(n)+",x["+str(j)+"])")
                e=e.replace(str(j)+' p',"posHillFunction("+str(U)+","+str(L)+','+str(T)+","+str(n)+",x["+str(j)+"])")
        xdot[k] = eval(e+'-x['+str(k)+']')
    return xdot

def evalHill(n,y0,t0=0,t1=10,dt=0.01):
    eqns,varnames=parseEqns()
    params,vals=parseSamples(varnames)
    D=[eqns,params,vals,n]
    r = ode(RHS).set_integrator('vode', method='bdf')
    r.set_initial_value(y0,t0).set_f_params(*D)
    return integrate(r,y0,t1,dt)

def integrate(r,y0,t0,t1,dt):
    times=[t0]
    funcvals=[y0]
    while r.successful() and r.t < t1:
        r.integrate(r.t+dt)
        times.append(r.t)
        funcvals.append(r.y)
    return times,funcvals

def plotResults(times,funcvals):
    plt.plot(times,np.array(funcvals))
    plt.show()

if __name__=='__main__':
    times,funcvals=evalHill(2,np.array([1,1]))
    plotResults(times,funcvals)

        

