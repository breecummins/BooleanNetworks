#standard libs
import numpy, itertools, os, pp, cPickle, glob
from functools import partial

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

def paramScan(ampfunc, doms, thresh,pr,ainds,maps,A=None,B=None,C=None,D=None,E=None,F=None):
    '''
    Scan across all parameter sets and calculate the sigma values and the location (domain) 
    of each sigma value.

    '''
    params = []
    allsigs = []
    sigboxes = []
    for p in itertools.product(A,B,C,D,E,F):
        amps = ampfunc(*p)
        sigs = getSigmas(doms,thresh,amps,pr,ainds,maps)
        sb = getSigBox(sigs,doms)
        if sb not in sigboxes and sb: #sb could be None
            params.append(p)
            allsigs.append(sigs)
            sigboxes.append(sb)
    return zip(params, allsigs, sigboxes)

def findMinimalParamSets(model=test4DExample1,modelargs = {'A':numpy.arange(0.5,8.25,0.25),'B':numpy.arange(0.5,2.75,0.25),'C':numpy.arange(0.5,2.75,0.25),'D':numpy.arange(0.5,2.75,0.25),'E':numpy.arange(0.5,5,0.25),'F':numpy.arange(0.1,1,0.1)}):
    ampfunc, doms, thresh,pr,ainds,maps, numsets= model(**modelargs)
    return paramScan(ampfunc, doms, thresh,pr,ainds,maps,**modelargs), numsets

def findMinimalParamSets_Parallel(modelinput = (test4DExample1,{'A':numpy.arange(2.25,4.25,0.25),'B':numpy.arange(0.75,1,0.25),'C':numpy.arange(0.75,1,0.25),'D':numpy.arange(0.75,1,0.25),'E':numpy.arange(0.5,5,0.25),'F':numpy.arange(0.1,1,0.1)},'ParamScanA04')):
    ampfunc, doms, thresh,pr,ainds,maps, numsets= modelinput[0](**modelinput[1])
    paramsets, numsets = paramScan(ampfunc, doms, thresh,pr,ainds,maps,**modelinput[1]), numsets
    msg = 'Total number of parameter sets with focal point collection in a unique set of domains: %d \n Total number of parameter sets tested: %d \n Saving %s.' % (len(paramsets),numsets,fname) 
    print(msg)   
    F = open(os.path.join(os.path.expanduser("~"),modelinput[2]+'.pickle'),'w')
    cPickle.Pickler(F).dump({'paramsets':paramsets,'numsets':numsets})
    F.close()
    return None

def test():
    paramsets, numsets = findMinimalParamSets()
    # for p, s, b in paramsets:
    #     print(p); print(len(b)); # print(s); print('       ')
    print('Total number of parameter sets with focal point collection in a unique set of domains: %d' %len(paramsets))
    # print('Total number of parameter sets tested: {0}'.format(numsets))
    F = open(os.path.join(os.path.expanduser("~"),'ParamScan1.pickle'),'w')
    cPickle.Pickler(F).dump({'paramsets':paramsets,'numsets':numsets})
    F.close()

def makeparamfile(fname=os.path.join(os.path.expanduser("~"),'SimulationResults/BooleanNetworks/ParamScan1.pickle')):
    mydict = fileops.loadPickle(fname)
    newfname = fname[:-6] + 'txt'
    f = open(newfname,'w')
    for p in mydict['paramsets']:
        f.write(str(p[0])+'\n')
    f.close()

def knitme():
    allpsets = []
    allsigms = []
    allboxes = []
    numsets = 0
    for f in glob.glob(os.path.join(os.path.expanduser("~"),'ParamScanA*')):
        print(f)
        F=open(f,'r')
        mydict = cPickle.Unpickler(F).load()
        F.close()
        for p in mydict['paramsets']:
            allpsets.append(p[0])
            allsigms.append(p[1])
            allboxes.append(p[2])
        numsets += mydict['numsets']
        print('Total sets: %d' % numsets)
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

def parallelrun():
    # tuple of all parallel python servers to connect with
    ppservers = ()
    # Creates jobserver with automatically detected # of workers
    job_server = pp.Server(ppservers=ppservers)
    print("Starting pp with " + str(job_server.get_ncpus()) + " workers.")
    model = test4DExample1
    fnames = ('ParamScanA02','ParamScanA04','ParamScanA06','ParamScanA08','ParamScanA10')
    inputs = ( (model,{'A':numpy.arange(0.5,2.25,0.1),'B':numpy.arange(0.75,1,0.25),'C':numpy.arange(0.75,1,0.25),'D':numpy.arange(0.75,1,0.25),'E':numpy.arange(0.5,5,0.1),'F':numpy.arange(0.1,1,0.1)},fnames[0]), (model,{'A':numpy.arange(2.25,4.25,0.1),'B':numpy.arange(0.75,1,0.25),'C':numpy.arange(0.75,1,0.25),'D':numpy.arange(0.75,1,0.25),'E':numpy.arange(0.5,5,0.1),'F':numpy.arange(0.1,1,0.1)},fnames[1]),(model,{'A':numpy.arange(4.25,6.25,0.1),'B':numpy.arange(0.75,1,0.25),'C':numpy.arange(0.75,1,0.25),'D':numpy.arange(0.75,1,0.25),'E':numpy.arange(0.5,5,0.1),'F':numpy.arange(0.1,1,0.1)},fnames[2]),(model,{'A':numpy.arange(6.25,8.25,0.1),'B':numpy.arange(0.75,1,0.25),'C':numpy.arange(0.75,1,0.25),'D':numpy.arange(0.75,1,0.25),'E':numpy.arange(0.5,5,0.1),'F':numpy.arange(0.1,1,0.1)},fnames[3]),(model,{'A':numpy.arange(8.25,10.25,0.1),'B':numpy.arange(0.75,1,0.25),'C':numpy.arange(0.75,1,0.25),'D':numpy.arange(0.75,1,0.25),'E':numpy.arange(0.5,5,0.1),'F':numpy.arange(0.1,1,0.1)},fnames[4]) )
    for inp in inputs:
        job_server.submit(findMinimalParamSets_Parallel,(inp,), depfuncs = (model,getSigmas,getSigBox,paramScan), modules = ("cPickle","numpy", "itertools", "os"),globals=globals())
    job_server.wait()
    job_server.print_stats()
    knitme()

if __name__ == '__main__':
    # import timeit
    # print(timeit.timeit("test()", setup="from __main__ import test",number=1))
    # makeparamfile()
    parallelrun()
    # findMinimalParamSets_Parallel()
    # knitme()





