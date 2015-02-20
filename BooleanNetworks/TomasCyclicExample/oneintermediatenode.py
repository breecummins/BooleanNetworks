import itertools, sys
import numpy as np
import BooleanNetworks.PatternMatching.patternmatch as pm
import BooleanNetworks.PatternMatching.fileparsers as fp
import BooleanNetworks.PatternMatching.preprocess as pp
import BooleanNetworks.PatternMatching.walllabels as wl

def makeDomains():
    # (x,y,z,s,u,v,w)
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
    # when w==2, u affected; when w==1, s affected
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
                elif ind==3:
                    if (d[3]==0.5 and d[6]==0.5) or (d[3]==1.5 and d[6]>=1.5):
                        edges.append(j)
                elif ind==4:
                    if (d[4]==0.5 and d[6]<=1.5) or (d[4]==1.5 and d[6]==2.5):
                        edges.append(j)
                elif ind==5:
                    if (d[5]==0.5 and d[4]==0.5) or (d[5]==1.5 and d[4]==1.5):
                        edges.append(j)
                elif ind==6:
                    if (d[6]==0.5 and d[5]==0.5) or (d[6]==1.5 and d[5]==1.5):
                        edges.append(j)
        outedges.append(tuple(edges))
    return outedges

def makeDomainGraph2(domains):
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

def checkDomainOutedges(domains,outedges):
    Domains=np.array(domains)
    noedges=[]
    for k,d in enumerate(Domains):
        diffs=np.abs(Domains-d)
        for j,r in enumerate(diffs):
            if np.abs(np.sum(r) -1.0)<0.1:
                if k not in outedges[j] and j not in outedges[k] and (k,j) not in noedges:
                    noedges.append((j,k))
    return noedges

def makeWallGraph(domains,outedges):
    # make list of walls in here too, as well as wall graph. I think it will be faster that way.
    walls=[]
    outdom=[]
    indom=[]
    for o,(n,d) in zip(outedges,enumerate(domains)):
        for i in o:
            c=domains[i]
            k=[abs(int(v-w)) for v,w in zip(d,c)].index(1)
            w=list(d)
            w[k]=w[k]-0.5 if d[k]>c[k] else w[k]+0.5
            walls.append(tuple(w))
            outdom.append(i)
            indom.append(n)
    walloutedges=[]
    for od in outdom:
        woe=[]
        nextdoms=outedges[od]
        for j in range(len(walls)):
            if indom[j]==od and outdom[j] in nextdoms:
                woe.append(j)
        walloutedges.append(tuple(woe))
    return walls, walloutedges

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

def searchForPatterns():
    print "Preprocessing..."
    domains=makeDomains()
    domainoutedges=makeDomainGraph2(domains)
    print sum([len(o) for o in domainoutedges])
    walldomains,walloutedges=makeWallGraph(domains,domainoutedges)
    varsaffectedatwall=makeVarsAffected(walldomains)
    wallinds,walloutedges,walldomains,varsaffectedatwall,allwalllabels = pp.filterAll(walloutedges,walldomains,varsaffectedatwall)
    varnames=fp.parseVars()
    patternnames,patternmaxmin=fp.parsePatterns()
    patterns=pp.constructCyclicPatterns(varnames,patternnames,patternmaxmin)
    for pattern in patterns:
        print "\n"
        print '-'*25
        print "Pattern: {}".format(pattern)
        match=pm.matchCyclicPattern(pattern,wallinds,walloutedges,walldomains,varsaffectedatwall, allwalllabels,showfirstwall=0)
        print "Results: {}".format(match)
        print '-'*25
        # sys.stdout.flush()



if __name__=='__main__':
    searchForPatterns()




