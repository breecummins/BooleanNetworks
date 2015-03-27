import numpy as np
from scipy.integrate import ode
import matplotlib.pyplot as plt
import hillparsers as hp

def posHillFunction(U,L,T,n,X):
    return (U-L) * X**n / (X**n + T**n) + L
    
def negHillFunction(U,L,T,n,X):
    return (U-L) * T**n / (X**n + T**n) + L

def makeNumericalEqns(eqns,params,vals,n):
    numeqns=[]
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
        numeqns.append(e+'-x['+str(k)+']')
    return numeqns

def RHS(t,x,eqns):
    xdot = [eval(e) for e in eqns]
    return np.array(xdot)

def simulateHillModel(n,y0,t0=0,t1=10,dt=0.01):
    eqns,varnames=hp.parseEqns()
    params,vals=hp.parseSamples(varnames)
    eqns=makeNumericalEqns(eqns,params,vals,n)
    r = ode(RHS).set_integrator('vode', method='bdf')
    r.set_initial_value(y0,t0).set_f_params(eqns)
    return integrate(r,y0,t0,t1,dt)

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

        

