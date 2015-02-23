import numpy as np

def makeDomains():
    '''
    x1 : x3 : x2
    x2 : ~x1 : x3
    x3 : x2+x5 : x1 x4
    x4 : x3 : x5
    x5 : ~x4 : x3

    '''
    base=[0.5]*4
    doms=[]
    for k in range(5):
        inds=itertools.combinations(range(4),k)
        for i in inds:
            b=base[:]
            for j in i:
                b[j]=1.5
            doms.append(b)
    domains = [tuple(d[:2]+[n]+d[2:]) for d in doms for n in [0.5,1.5,2.5]]
    return domains

def makeDomainGraph(domains):
    # (x1,x2,x3,x4,x5)
    # (0,1,2,3,4)
    # affectedby=[(2,),(0,),(1,4),(2,),(3,)]
    # when x3==1, x1 affected; when x3==2, x4 affected
    outedges=[]
    Domains=np.array(domains)
    for d in Domains:
        diffs=np.abs(Domains-d)
        edges=[]
        for j,r in enumerate(diffs):
            if np.abs(np.sum(r) -1.0)<0.1:
                ind=np.where(np.abs(r-1.0)<0.1)[0]
                if ind == 0:
                    if (d[0]==0.5 and d[2]>=1.5) or (d[0]==1.5 and d[2]==0.5):
                        edges.append(j)
                elif ind==1:
                    if (d[1]==0.5 and d[0]==0.5) or (d[1]==1.5 and d[0]==1.5):
                        edges.append(j)
                elif ind==2:
                    if (d[2]==0.5 and (d[1]==1.5 or d[4]==1.5)) or (d[2]==1.5 and d[1]==0.5 and d[4]==0.5):
                        edges.append(j)
                elif ind==3:
                    if (d[3]==0.5 and d[2]==2.5) or (d[3]==1.5 and d[2]<=1.5):
                        edges.append(j)
                elif ind==4:
                    if (d[4]==0.5 and d[3]==0.5) or (d[4]==1.5 and d[3]==1.5):
                        edges.append(j)
        outedges.append(tuple(edges))
    return outedges

def makeVarsAffected(walls):
    # (x1,x2,x3,x4,x5)
    # (0,1,2,3,4)
    affects=[(1,),(2,),(0,3),(4,),(2,)]
    varsaffectedatwalls=[]
    for w in walls:
        for k,v in enumerate(w):
            if abs(v-int(v)) < 0.25:
                a=affects[k]
                if k!=2:
                    varsaffectedatwalls.append(a[0])
                    break
                elif k == 2 and v==1:
                    varsaffectedatwalls.append(0)
                    break
                elif k == 2 and v==2:
                    varsaffectedatwalls.append(3)
                    break
    return varsaffectedatwalls

def writePatterns():
    f=open('patterns.txt','w')
    f.write('x1 max, x2 min, x3 min, x1 min, x2 max, x3 max\nx4 max, x5 min, x3 min, x4 min, x5 max, x3 max\nx3 min, x1 min, x4 min, x2 max, x5 max, x3 max, x1 max, x4 max, x2 min, x5 min')
    f.close()

def writeVars():
    f=open('variables.txt','w')
    f.write('0 x1\n1 x2\n2 x3\n3 x4\n4 x5')
    f.close()

if __name__=='__main__':
    import sharedfunctions as sf
    # domains=makeDomains()
    # outedges=makeDomainGraph(domains)
    # noedges=sf.checkDomainOutedges(domains,outedges)
    # print len(domains)
    # print sum([len(o) for o in outedges])+len(noedges)
    sf.searchForPatterns(pymod='symmetric5D')
    