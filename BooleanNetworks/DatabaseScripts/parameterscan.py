#standard libs
import numpy, itertools, os, cPickle, pp, glob

def Example8D_1(A1,A2,A3,A4,A5,A6,A7,A8,A9,A10,B1,B2,B3,B4,B5,B6):
    # define the interactions between variables
    variables = ['x','y1','y2','y3','z','w1','w2','w3']
    affectedby = [['x','y3','z','w1'],['x'],['x','y1','w1'],['y2','w1'],['x','w2'],['y2','w2'],['w1','w3'],['x','w2']]
    # give the thresholds for each interaction
    thresholds = [[2,1,1,2],[1],[4,1,1],[1,2],[3,1],[1,1],[1,1],[3,1]]
    # give the maps and amplitudes of each interaction (upper and lower bounds for parameter search)
    maps = [[(0,0,0,0),(1,0,0,0),(0,1,0,0),(1,1,0,0),(0,0,1,0),(1,0,1,0),(0,1,1,0),(1,1,1,0),(0,0,0,1),(1,0,0,1),(0,1,0,1),(1,1,0,1),(0,0,1,1),(1,0,1,1),(0,1,1,1),(1,1,1,1)],[(0,),(1,)],[(0,0,0),(1,0,0),(0,1,0),(1,1,0),(0,0,1),(1,0,1),(0,1,1),(1,1,1)],[(0,0),(1,0),(0,1),(1,1)],[(0,0),(1,0),(0,1),(1,1)],[(0,0),(1,0),(0,1),(1,1)],[(0,0),(1,0),(0,1),(1,1)],[(0,0),(1,0),(0,1),(1,1)] ]
    ampfunc = lambda A1,A2,A3,A4,A5,A6,A7,A8,A9,A10,B1,B2,B3,B4,B5,B6: [ [0,A1,A2,A1+A2,0,A1*B1,A2*B1,(A1+A2)*B1,0,A1*B2,A2*B2,(A1+A2)*B2,0,A1*B1*B2,A2*B1*B2,(A1+A2)*B1*B2],[0,A3],[0,A4,A5,A4+A5,A6,A4+A6,A5+A6,A4+A5+A6],[0,A7,0,A7*B3],[0,A8,0,A8*B4],[0,A9,0,A9*B5],[0,A10,0,A10*B6],[0,A8,0,A8*B4]  ]
    # give the endogenous production rates. 
    productionrates = [0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1] 
    # get upper and lower bounds
    bigamps = ampfunc(A1[-1],A2[-1],A3[-1],A4[-1],A5[-1],A6[-1],A7[-1],A8[-1],A9[-1],A10[-1],B1[-1],B2[-1],B3[-1],B4[-1],B5[-1],B6[-1])
    upperbounds = 1.1*( numpy.array([numpy.max(u) for u in bigamps]) + numpy.array(productionrates) ) # calculate upper bounds of domains
    lowerbounds = numpy.zeros(upperbounds.shape)
    # make domains
    thresh,ainds,pr = makeParameterArrays(variables, affectedby, thresholds, productionrates)
    doms = getDomains(thresh,lowerbounds,upperbounds)
    numsets = len(A1)*len(A2)*len(A3)*len(A4)*len(A5)*len(A6)*len(A7)*len(A8)*len(A9)*len(A10)*len(B1)*len(B2)*len(B3)*len(B4)*len(B5)*len(B6)
    print('Number of parameter sets to test: %d' %numsets)
    return ampfunc, doms, thresh,pr,ainds,maps,numsets

def test4DExample1(A=numpy.arange(0.05,12.25,0.5),B=numpy.arange(0.05,12.25,0.5),C=numpy.arange(0.05,12.25,0.5),D=numpy.arange(0.05,12.25,0.5),E=numpy.arange(0.05,12.25,0.5),F=numpy.arange(0.05,1,0.25)):
    '''
    Create all parameter sets given as ranges in the arguments.
    **Assume equal decay rates of 1.**

    '''
    # define the interactions between variables
    variables = ['x','y1','y2','z']
    affectedby = [['x','y2','z'],['x'],['y1'],['x']]
    # give the thresholds for each interaction
    thresholds = [[2,1,1],[3],[1],[1]]
    # give the maps and amplitudes of each interaction (upper and lower bounds for parameter search)
    maps = [[(0,0,0),(1,0,0),(0,1,0),(1,1,0),(0,0,1),(1,0,1),(0,1,1),(1,1,1)],[(0,),(1,)],[(0,),(1,)],[(0,),(1,)]]
    ampfunc = lambda a,b,c,d,e,f: [[0,e,a,a+e,0,f*e,f*a,(a+e)*f],[0,c],[0,d],[0,b]]
    # give the endogenous production rates. 
    productionrates = [0.1,0.5,0.5,0.5] 
    # get upper and lower bounds
    bigamps = ampfunc(A[-1],B[-1],C[-1],D[-1],E[-1],F[-1])
    upperbounds = 1.1*( numpy.array([numpy.max(u) for u in bigamps]) + numpy.array(productionrates) ) 
    lowerbounds = numpy.zeros(upperbounds.shape)
    # make domains
    thresh,ainds,pr = makeParameterArrays(variables, affectedby, thresholds, productionrates)
    doms = getDomains(thresh,lowerbounds,upperbounds)
    numsets = len(A)*len(B)*len(C)*len(D)*len(E)*len(F)
    print('Number of parameter sets to test: %d' %numsets)
    return ampfunc, doms, thresh,pr,ainds,maps,numsets

def makeParameterArrays(variables, affectedby, thresholds, productionrates):
    '''
    Put model parameters into square arrays, where the column 
    index indicates the source variable and the row index 
    indicates the target variable.

    The outputs thresh, lamp, uamp, and rep are len(variables) x len(variables)
    arrays with threshold values, amplitudes, and repressor 
    identities filled in between the appropriate source-target 
    interactions. All other array values are zero. The output
    pr is simply the list productionrates converted to an array.

    '''
    N = len(variables)
    thresh = numpy.zeros((N,N))
    ainds = []
    for j,a in enumerate(affectedby): #j is index of target
        at = []
        for k,t in enumerate(a):
            i =  variables.index(t) #i is index of source
            at.append(i)
            thresh[j,i] = thresholds[j][k]
        ainds.append(at)
    pr = numpy.array(productionrates)
    return thresh, ainds, pr

def getDomains(thresh,lowerbounds,upperbounds):
    '''
    Find the domain bounds for each 
    regular domain (area between thresholds).

    '''
    dp = []
    for j in range(thresh.shape[1]):
        tl = list(numpy.unique(thresh[:,j])) + [upperbounds[j]]
        if tl[0] != 0:
            tl = [0] + tl
        tl[0] = tl[0] + lowerbounds[j]
        dp.append( [tl[k:k+2] for k in range(len(tl[:-1]))] )
    # return the bounds for each regular domain 
    return numpy.array(list(itertools.product(*dp)))

def getSigmas(doms,thresh,amp,pr,ainds,maps):
    '''
    Find the sigma bounds in each regular domain.

    '''
    sigs = []
    midpts = numpy.mean(doms,2)
    for i in range(doms.shape[0]):
        comp = (midpts[i,:] > thresh).astype(int) # compare domain midpts to thresholds
        s=[]
        for j,a in enumerate(ainds):
            bmap = tuple( comp[j][a] ) # get the binary map for target j
            for k,m in enumerate(maps[j]): # get the index of binary map; this method is slightly faster than k = maps[j].index(bmap)
                if m == bmap:
                    s.append(amp[j][k]+pr[j]) # calculate sigma (is the focal point also if decay rates are 1)
                    break
        sigs.append(s)
    return sigs

def getSigBox(sigs,doms):
    sigboxes = []
    for s in sigs:
        sig = numpy.array(s)
        inds = numpy.nonzero(numpy.all((sig - doms[:,:,0])*(sig-doms[:,:,1]) < 0,1))[0]
        if len(inds)==1:
            sigboxes.append(inds[0])
        elif len(inds) == 0:
            return None
    return tuple(sigboxes)

def paramScan(ampfunc, doms, thresh,pr,ainds,maps,paramranges):
    '''
    Scan across all parameter sets and calculate the sigma values and the location (domain) 
    of each sigma value.

    '''
    params = []
    allsigs = []
    sigboxes = []
    for p in itertools.product(*paramranges):
        amps = ampfunc(*p)
        sigs = getSigmas(doms,thresh,amps,pr,ainds,maps)
        sb = getSigBox(sigs,doms)
        if sb not in sigboxes and sb: #sb could be None
            params.append(p)
            allsigs.append(sigs)
            sigboxes.append(sb)
    return zip(params, allsigs, sigboxes)

def findMinimalParamSets(model=test4DExample1,paramranges = (numpy.arange(0.5,8.25,0.25),numpy.arange(0.5,2.75,0.25),numpy.arange(0.5,2.75,0.25),numpy.arange(0.5,2.75,0.25),numpy.arange(0.5,5,0.25),numpy.arange(0.1,1,0.1))):
    ampfunc, doms, thresh,pr,ainds,maps, numsets= model(*paramranges)
    return paramScan(ampfunc, doms, thresh,pr,ainds,maps,paramranges), numsets

def findMinimalParamSets_Parallel(model,paramranges,fname):
    # Do not make a default arg for model - it may not be in the pp name space. Hard to debug.
    ampfunc, doms, thresh,pr,ainds,maps, numsets= model(*paramranges)
    paramsets = paramScan(ampfunc, doms, thresh,pr,ainds,maps,paramranges)
    F = open(os.path.join(os.path.expanduser("~"),fname+'.pickle'),'w')
    cPickle.Pickler(F).dump({'paramsets':paramsets,'numsets':numsets})
    F.close()
    msg = 'Total number of parameter sets with focal point collection in a unique set of domains: %d \n Total number of parameter sets tested: %d \n Saving %s.' % (len(paramsets),numsets,fname) 
    return msg

def knitme(globstr='ParamScanA*'):
    allpsets = []
    allsigms = []
    allboxes = []
    numsets = 0
    for f in glob.glob(os.path.join(os.path.expanduser("~"),globstr)):
        print(f)
        F=open(f,'r')
        mydict = cPickle.Unpickler(F).load()
        F.close()
        for p in mydict['paramsets']:
            allpsets.append(p[0])
            allsigms.append(p[1])
            allboxes.append(p[2])
        numsets += mydict['numsets']
        print('Total sets: %d' % mydict['numsets'])
        print('Unique sets: %d' % len(mydict['paramsets']))
    print('New list length: %d' % len(allpsets))
    uniqparam = []
    uniqsigms = []
    uniqboxes = []
    for p,s,b in zip(allpsets,allsigms,allboxes):
        if b not in uniqboxes:
            uniqparam.append(p)
            uniqsigms.append(s)
            uniqboxes.append(b)
    print('Total number of parameter sets with focal point collection in a unique set of domains: %d' %len(uniqparam))
    print('Total number of parameter sets tested: {0}'.format(numsets))
    fname=os.path.join(os.path.expanduser("~"),'ParamScanTotal.pickle')
    print('Saving '+fname)
    F = open(fname,'w')
    cPickle.Pickler(F).dump({'paramsets':zip(uniqparam,uniqsigms,uniqboxes),'numsets':numsets})
    F.close()

def parallelrun_4D():
    # tuple of all parallel python servers to connect with
    ppservers = ()
    # Creates jobserver with automatically detected # of workers
    job_server = pp.Server(ppservers=ppservers)
    print("Starting pp with " + str(job_server.get_ncpus()) + " workers.")
    model = test4DExample1
    fnames = ('ParamScanA02','ParamScanA04','ParamScanA06','ParamScanA08','ParamScanA10')
    A = [numpy.arange(0.5,2.25,0.1), numpy.arange(2.25,4.25,0.1), numpy.arange(4.25,6.25,0.1), numpy.arange(6.25,8.25,0.1), numpy.arange(8.25,10.25,0.1)]
    B = numpy.arange(0.75,1,0.25)
    C = numpy.arange(0.75,1,0.25)
    D = numpy.arange(0.75,1,0.25)
    E = numpy.arange(0.5,5,0.1)
    F = numpy.arange(0.1,1,0.1)
    jobs = []
    for j,f in enumerate(fnames):
        jobs.append(job_server.submit(findMinimalParamSets_Parallel,( model,(A[j],B,C,D,E,F),f ), depfuncs = (model,paramScan), modules = ("cPickle","numpy", "itertools", "os"),globals=globals()))
    for job in jobs:
        print(job())
    job_server.print_stats()
    knitme('ParamScanA*')

def parallelrun_8D():
    # tuple of all parallel python servers to connect with
    ppservers = ()
    # Creates jobserver with automatically detected # of workers
    job_server = pp.Server(ppservers=ppservers)
    print("Starting pp with " + str(job_server.get_ncpus()) + " workers.")
    model = Example8D_1
    A1 = [0.5,1.0,3.0,5.0,8.0,10.0]
    A2 = [0.5,1.0,5.0]
    A3 = [1.0]
    A4,A5,A6 = [0.4,0.6,1.0,2.0], [0.4,0.6,1.0,2.0], [0.4,0.6,1.0,2.0]
    A7,A8,A9,A10 = [1.0,5.0],[1.0,5.0],[1.0,5.0],[1.0,5.0]
    B1,B2,B3,B4,B5,B6 = [0.25,0.5,0.75],[0.25,0.5,0.75],[0.25,0.5,0.75],[0.25,0.5,0.75],[0.25,0.5,0.75],[0.25,0.5,0.75]
    jobs = []
    for i in range(len(A1)):
        for j in range(len(A2)):
            jobs.append(job_server.submit(findMinimalParamSets_Parallel,( model,([A1[i]],[A2[j]],A3,A4,A5,A6,A7,A8,A9,A10,B1,B2,B3,B4,B5,B6),'ParamScan_'+str(i)+str(j) ), depfuncs = (model,paramScan), modules = ("cPickle","numpy", "itertools", "os"),globals=globals()))
    for job in jobs:
        print(job())
    job_server.print_stats()
    knitme('ParamScan_*')

def makeparamfile(fname=os.path.join(os.path.expanduser("~"),'SimulationResults/BooleanNetworks/ParamScan1.pickle')):
    mydict = fileops.loadPickle(fname)
    newfname = fname[:-6] + 'txt'
    f = open(newfname,'w')
    for p in mydict['paramsets']:
        f.write(str(p[0])+'\n')
    f.close()

if __name__ == '__main__':
    # makeparamfile()
    # parallelrun_4D()
    parallelrun_8D()
    # findMinimalParamSets_Parallel(Example8D_1, ([0.5], [0.5,1.0,5.0], [1.0], [0.4,0.6,1.0,2.0], [0.4,0.6,1.0,2.0], [0.4,0.6,1.0,2.0], [1.0,5.0],[1.0,5.0],[1.0,5.0],[1.0,5.0], [0.25,0.5,0.75],[0.25,0.5,0.75],[0.25,0.5,0.75],[0.25,0.5,0.75],[0.25,0.5,0.75],[0.25,0.5,0.75]), 'ParamScanA1_onehalf')
    # knitme()





