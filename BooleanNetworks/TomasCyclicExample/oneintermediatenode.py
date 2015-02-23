import numpy as np

def makeDomains():
    '''
    x : ~z : y
    y : (~x)(~s) : z
    z : ~y : x
    s : ~w : y
    u : ~w : v
    v : ~u : w
    w : ~v : s u

    '''
    base=[0.5]*6
    doms=[]
    for k in range(7):
        inds=itertools.combinations(range(6),k)
        for i in inds:
            b=base[:]
            for j in i:
                b[j]=1.5
            doms.append(b)
    domains = [tuple(d+[n]) for d in doms for n in [0.5,1.5,2.5]]
    return domains

def makeDomainGraph(domains):
    # (x,y,z,s,u,v,w)
    # (0,1,2,3,4,5,6)
    # affectedby=[(2,),(0,3),(1,),(6,),(6,),(4,),(5,)]
    # when w==1, u affected; when w==2, s affected
    outedges=[]
    Domains=np.array(domains)
    for d in Domains:
        diffs=np.abs(Domains-d)
        edges=[]
        for j,r in enumerate(diffs):
            if np.abs(np.sum(r) -1.0)<0.1:
                ind=np.where(np.abs(r-1.0)<0.1)[0]
                if ind == 0:
                    if (d[0]==0.5 and d[2]==0.5) or (d[0]==1.5 and d[2]==1.5):
                        edges.append(j)
                elif ind==1:
                    if (d[1]==0.5 and d[0]==0.5 and d[3]==0.5) or (d[1]==1.5 and (d[0]==1.5 or d[3]==1.5)):
                        edges.append(j)
                elif ind==2:
                    if (d[2]==0.5 and d[1]==0.5) or (d[2]==1.5 and d[1]==1.5):
                        edges.append(j)
                elif ind==4:
                    if (d[4]==0.5 and d[6]==0.5) or (d[4]==1.5 and d[6]>=1.5):
                        edges.append(j)
                elif ind==3:
                    if (d[3]==0.5 and d[6]<=1.5) or (d[3]==1.5 and d[6]==2.5):
                        edges.append(j)
                elif ind==5:
                    if (d[5]==0.5 and d[4]==0.5) or (d[5]==1.5 and d[4]==1.5):
                        edges.append(j)
                elif ind==6:
                    if (d[6]==0.5 and d[5]==0.5) or (d[6]==1.5 and d[5]==1.5):
                        edges.append(j)
        outedges.append(tuple(edges))
    return outedges

def makeVarsAffected(walls):
    # (x,y,z,s,u,v,w)
    # (0,1,2,3,4,5,6)
    affects=[(1,),(2,),(0,),(1,),(5,),(6,),(3,4)]
    varsaffectedatwalls=[]
    for w in walls:
        for k,v in enumerate(w):
            if abs(v-int(v)) < 0.25:
                a=affects[k]
                if k<6:
                    varsaffectedatwalls.append(a[0])
                    break
                elif k == 6 and v==1:
                    varsaffectedatwalls.append(3)
                    break
                elif k == 6 and v==2:
                    varsaffectedatwalls.append(4)
                    break
    return varsaffectedatwalls

def writePatterns():
    f=open('patterns.txt','w')
    f.write('x max, y max, z max, x min, y min, z min\nx min, y max, z min, x max, y min, z max\nu max, v max, w max, u min, v min, w min\nu min, v max, w min, u max, v min, w max\nv max, x max, w min, s max, y min, u max, z max, v min, x min, s min, w max, y max, u min, z min')
    f.close()

def writeVars():
    f=open('variables.txt','w')
    f.write('0 x\n1 y\n2 z\n3 s\n4 u\n5 v\n6 w')
    f.close()

if __name__=='__main__':
    import sharedfunctions as sf
    # domains=makeDomains()
    # outedges=makeDomainGraph(domains)
    # noedges=sf.checkDomainOutedges(domains,outedges)
    # print len(domains)
    # print sum([len(o) for o in outedges])+len(noedges)
    sf.searchForPatterns(pymod='oneintermediatenode')

