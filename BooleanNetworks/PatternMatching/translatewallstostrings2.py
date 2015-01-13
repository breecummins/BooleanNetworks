def parseOutEdges(fname='outEdges.txt'):
    f=open(fname,'r')
    outedges=[]
    for l in f:
        outedges.append(tuple([int(i) for i in l.split(' ')[1:-1]]))
    return outedges

def testParseOutEdges():
    # compare the output file to the input file by eye
    g=open('parsedoutedges.txt','w')
    for oe in parseOutEdges():
        g.write(str(oe)+'\n')
    g.close()

def parseWalls(fname='walls.txt'):
    f=open(fname,'r')
    walldomains=[]
    for l in f:
        L = filter(None,l.replace('[',' ').replace('x',' ').replace(']',' ').replace(',',' ').split(' ')[2:-1])
        L = [float(n) for n in L]
        T = []
        for k in range(0,len(L)-1,2):
            T.append(sum(L[k:k+2])/2)
        walldomains.append(tuple(T))
    return walldomains

def testParseWalls():
    # compare the output file to the input file by eye
    g=open('parsedwalls.txt','w')
    for wd in parseWalls():
        g.write(str(wd)+'\n')
    g.close()

def filterBoundaryWallsAndSteadyStates(outedges):
    # get rid of boundary walls and steady states, because we shall assume that 
    # searchable patterns have only extrema
    # for use with patternmatch3
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
    # testParseOutEdges()
    testParseWalls()
