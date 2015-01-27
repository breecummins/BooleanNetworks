def parseOutEdges(fname='outEdges.txt'):
    f=open(fname,'r')
    outedges=[]
    for l in f:
        outedges.append(tuple([int(i) for i in l.split(' ')[1:-1]]))
    return outedges

def parseWalls(fname='walls.txt'):
    f=open(fname,'r')
    walldomains=[]
    for l in f:
        L = filter(None,l.replace('[',' ').replace('x',' ').replace(']',' ').replace(',',' ').split(' ')[2:-1])
        L = [float(n) for n in L]
        T = []
        for k in range(0,len(L)-1,2):
            T.append(sum(L[k:k+2])/2) # thresholds are integers, regular domains end in .5
        walldomains.append(tuple(T))
    return walldomains

def parseVars(fname="variables.txt"):
    # this parser depends on the file being small enough to fit in memory
    f=open(fname,'r')
    R=f.read().split()
    return R[1::2]     

def parsePatterns(fname="patterns.txt"):
    f=open(fname,'r')
    Maxmin=[]
    varnames=[]
    for l in f:
        L=l.replace(',',' ').split()
        varnames.append(L[::2])
        Maxmin.append(L[1::2])
    return varnames, Maxmin

def filterBoundaryWallsAndSteadyStates(outedges):
    # CURRENTLY NOT USED - is possible future optimization
    # get rid of boundary walls and steady states, because we shall assume that 
    # searchable patterns have only extrema
    inedges=[tuple([j for j,o in enumerate(outedges) if i in o ]) for i in range(len(outedges))]
    interiorinds=[]
    interioroutedges=[]
    for q,(o,i) in enumerate(zip(outedges,inedges)):
        if i and (o!=(q,)): 
            interiorinds.append(q)
            interioroutedges.append([o])
    for k,o in enumerate(interioroutedges):
        newo = [j for j in o if j in interiorinds]
        interioroutedges[k] = newo
    return interiorinds,interioroutedges

if __name__=='__main__':
    # print parseVars("/Users/bcummins/ProjectData/DatabaseSimulations/5D_cycle_1/MGCC_14419/variables.txt")
    print parsePatterns()
