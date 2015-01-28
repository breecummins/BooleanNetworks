def parseOutEdges(fname='outEdges.txt'):
    f=open(fname,'r')
    outedges=[]
    for l in f:
        outedges.append(tuple([int(i) for i in l.split(' ')[1:-1]]))
    return outedges

def parseWalls(fname='walls.txt'):
    f=open(fname,'r')
    walldomains=[]
    varatthresh=[]
    for l in f:
        L = filter(None,l.replace('[',' ').replace('x',' ').replace(']',' ').replace(',',' ').split(' ')[1:-1])
        varatthresh.append(int(L[0]))
        L = [float(n) for n in L[1:]]
        T = []
        for k in range(0,len(L)-1,2):
            T.append(sum(L[k:k+2])/2) # thresholds are integers, regular domains end in .5
        walldomains.append(tuple(T))
    return walldomains,varatthresh

def parseVars(fname="variables.txt"):
    # this parser depends on the file being small enough to fit in memory
    f=open(fname,'r')
    R=f.read().split()
    return R[1::2]  

def parseEqns(fname="equations.txt"):
    f=open(fname,'r')
    threshvars=[]
    for l in f:
        L=l.split(':')
        threshvars.append(tuple([L[0].replace(' ',''),L[2].split()]))
    return threshvars

def parsePatterns(fname="patterns.txt"):
    f=open(fname,'r')
    Maxmin=[]
    varnames=[]
    for l in f:
        L=l.replace(',',' ').split()
        varnames.append(L[::2])
        Maxmin.append(L[1::2])
    return varnames, Maxmin

def parseAll(oname='outEdges.txt',wname='walls.txt',vname="variables.txt",ename="equations.txt",pname="patterns.txt"):
    return parseOutEdges(oname), parseWalls(wname), parseVars(vname), parseEqns(ename), parsePatterns(pname)

if __name__=='__main__':
    # print parseVars("/Users/bcummins/ProjectData/DatabaseSimulations/5D_cycle_1/MGCC_14419/variables.txt")
    # print parsePatterns()
    print parseEqns("/Users/bcummins/ProjectData/DatabaseSimulations/5D_cycle_1/MGCC_14419/equations.txt")