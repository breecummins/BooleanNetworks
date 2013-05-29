import numpy as np
import os, random, cPickle
from functools import partial
import modelNetworks as mN

def partitionOrthant(model=mN.model1,fname=os.path.expanduser('~/temp/model1tracks'),orthrange = np.arange(-0.1,-2.2,-0.2),per=[0.0,-0.01,0.01,0.02],dt=0.01,finaltime=5.0):
    
    tracks = []
    for i in orthrange:
        for j in orthrange:
            for k in orthrange:
                for l in orthrange:
                    random.shuffle(per)
                    init = np.array([1.0,i+per[0],j+per[1],k+per[2],l+per[3]])
                    ts = mN.solveModel(init,finaltime,model,dt)
                    t = mN.translateToOrthants(ts)
                    tracks.append(mN.encodeInts(t))
    fname += '.pickle'
    of = open(fname,'w')
    cPickle.dump(tracks,of)
    of.close()

def alterParams(maindir,Alist=[0.5,1.0,1.5,2.0],Blist=[-0.5,-1.0,-2.0],per=[0.0,-0.01,0.01,0.02],dt=0.01):
    for k,A in enumerate(Alist):
        L0 = partial(mN.L0,A0=A)
        fname1=os.path.join(maindir,'model1tracksA'+str(k))
        mod1 = partial(mN.model1,L0=L0)
        partitionOrthant(mod1,fname1,per=per,dt=dt)
        for j,B in enumerate(Blist):
            L4 =partial(mN.L0,A0=1.0,B0=B,C0=2.0,D0=1.0)
            fname2=os.path.join(maindir,'model2tracksA'+str(k)+'B'+str(j))
            mod2=partial(mN.model2,L0=L0,L4=L4)
            partitionOrthant(mod2,fname2)
            mod3=partial(mN.model3,L0=L0,L4=L4)
            fname3=os.path.join(maindir,'model3tracksA'+str(k)+'B'+str(j))
            partitionOrthant(mod3,fname3)
            newL4=partial(mN.L4,B0=B)
            mod4=partial(mN.model4,L0=L0,L4=newL4)
            fname4=os.path.join(maindir,'model4tracksA'+str(k)+'B'+str(j))
            partitionOrthant(mod4,fname4)

def partitionOrthantRandInits(inits,model=mN.model1,fname=os.path.expanduser('~/temp/model1tracks'),dt=0.01,finaltime=5.0):    
    tracks = []
    for k in range(inits.shape[0]):
        ts = mN.solveModel(inits[k,:],finaltime,model,dt)
        t = mN.translateToOrthants(ts)
        tracks.append(mN.encodeInts(t))
    fname += '.pickle'
    of = open(fname,'w')
    cPickle.dump(tracks,of)
    of.close()

def randInits(maindir,Alist=[0.5,1.0,1.5,2.0],Blist=[-0.5,-1.0,-2.0],dt=0.01,xinit=1.0,numinits=2000):
    if 'inits.pickle' not in os.listdir(maindir):
        print('Generating new initial conditions...')
        inits = -2.1 + 2*np.random.random((numinits,4))
        of = open(os.path.join(maindir,'inits.pickle'),'w')
        cPickle.dump({'inits':inits},of)
        of.close()
    else:
        print('Using existing initial conditions file...')
        of = open(os.path.join(maindir,'inits.pickle'),'r')
        idict=cPickle.load(of)
        of.close()
        inits=idict['inits']
    initsx = xinit*np.ones(5)
    initsx[:,1:] = inits
    del(inits)
    inits = initsx
    for k,A in enumerate(Alist):
        print('Model 1, A = ' + str(A))
        L0 = partial(mN.L0,A0=A)
        fname1=os.path.join(maindir,'model1tracksA'+str(k))
        mod1 = partial(mN.model1,L0=L0)
        partitionOrthantRandInits(inits,mod1,fname1,dt=dt)
        for j,B in enumerate(Blist):
            print('Model 2, A = ' + str(A) + ', B = ' + str(B))
            L4 =partial(mN.L0,A0=1.0,B0=B,C0=2.0,D0=1.0)
            fname2=os.path.join(maindir,'model2tracksA'+str(k)+'B'+str(j))
            mod2=partial(mN.model2,L0=L0,L4=L4)
            partitionOrthantRandInits(inits,mod2,fname2)
            print('Model 3, A = ' + str(A) + ', B = ' + str(B))
            mod3=partial(mN.model3,L0=L0,L4=L4)
            fname3=os.path.join(maindir,'model3tracksA'+str(k)+'B'+str(j))
            partitionOrthantRandInits(inits,mod3,fname3)
            newL4=partial(mN.L4,B0=B)
            print('Model 4, A = ' + str(A) + ', B = ' + str(B))
            mod4=partial(mN.model4,L0=L0,L4=newL4)
            fname4=os.path.join(maindir,'model4tracksA'+str(k)+'B'+str(j))
            partitionOrthantRandInits(inits,mod4,fname4)

def randInitsWithX(maindir,Alist=[0.5,1.0,1.5,2.0],Blist=[-0.5,-1.0,-2.0],dt=0.01,numinits=20000):
    if 'inits.pickle' not in os.listdir(maindir):
        print('Generating new initial conditions...')
        inits = -2.1 + 2*np.random.random((numinits,5))
        inits[:,0] = 10.0 - 9*np.random.random((numinits,))
        of = open(os.path.join(maindir,'inits.pickle'),'w')
        cPickle.dump(inits,of)
        of.close()
    else:
        print('Using existing initial conditions file...')
        of = open(os.path.join(maindir,'inits.pickle'),'r')
        inits=cPickle.load(of)
        of.close()
    for k,A in enumerate(Alist):
        print('Model 1, A = ' + str(A))
        L0 = partial(mN.L0,A0=A)
        fname1=os.path.join(maindir,'model1tracksA'+str(k))
        mod1 = partial(mN.model1,L0=L0)
        partitionOrthantRandInits(inits,mod1,fname1,dt=dt)
        for j,B in enumerate(Blist):
            print('Model 2, A = ' + str(A) + ', B = ' + str(B))
            L4 =partial(mN.L0,A0=1.0,B0=B,C0=2.0,D0=1.0)
            fname2=os.path.join(maindir,'model2tracksA'+str(k)+'B'+str(j))
            mod2=partial(mN.model2,L0=L0,L4=L4)
            partitionOrthantRandInits(inits,mod2,fname2)
            print('Model 3, A = ' + str(A) + ', B = ' + str(B))
            mod3=partial(mN.model3,L0=L0,L4=L4)
            fname3=os.path.join(maindir,'model3tracksA'+str(k)+'B'+str(j))
            partitionOrthantRandInits(inits,mod3,fname3)
            newL4=partial(mN.L4,B0=B)
            print('Model 4, A = ' + str(A) + ', B = ' + str(B))
            mod4=partial(mN.model4,L0=L0,L4=newL4)
            fname4=os.path.join(maindir,'model4tracksA'+str(k)+'B'+str(j))
            partitionOrthantRandInits(inits,mod4,fname4)

if __name__ == "__main__":
        alterParams()