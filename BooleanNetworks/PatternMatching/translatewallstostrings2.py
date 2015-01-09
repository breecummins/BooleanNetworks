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
    walls=[]
    for l in f:
        L = filter(None,l.replace('[',' ').replace('x',' ').replace(']',' ').replace(',',' ').split(' ')[2:-1])
        L = [float(n) for n in L]
        T = []
        for k in range(0,len(L)-1,2):
            T.append(sum(L[k:k+2])/2)
        walls.append(tuple(T))
    return walls

def testParseWalls():
    # compare the output file to the input file by eye
    g=open('parsedwalls.txt','w')
    for wd in parseWalls():
        g.write(str(wd)+'\n')
    g.close()


if __name__=='__main__':
    # testParseOutEdges()
    testParseWalls()
