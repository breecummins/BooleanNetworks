import itertools
from scipy.sparse.csgraph import connected_components
import numpy as np

def makeDomains():
    base=[0.5]*7
    domains=[]
    for k in range(8):
        inds=itertools.combinations(range(7),k)
        for i in inds:
            b=base[:]
            for j in i:
                b[j]=1.5
            domains.append(tuple(b))
    return domains

def makeDomainGraph(domains):
    affectedby=[(2,),(0,6),(1,),(5,),(3,),(4,),(5,)]
    outedges=[]
    for d in domains:
        edges=[]
        for j,c in enumerate(domains):
            diffs=[k for k,(v,w) in enumerate(zip(d,c)) if v-w]
            if len(diffs)==1:
                domvals = [d[i] for a in affectedby for i in a]
                if ( d[diffs[0]]==0.5 and (0.5 in domvals) ) or ( d[diffs[0]]==1.5 and (1.5 in domvals) ):
                    edges.append(j)
        outedges.append(tuple(edges))
    return outedges

def makeWallGraph(domains,outedges):
    # make list of walls in here too, as well as wall graph. I think it will be faster that way.
    walls=[]
    walldomoutedges=[]
    for o,d in zip(outedges,domains):
        for i in o:
            c=domains[i]
            k=[abs(int(v-w)) for v,w in zip(d,c)].index(1)
            w=list(d)
            w[k]=w[k]-0.5 if d[k]>c[k] else w[k]+0.5
            walls.append(tuple(w))
            walldomoutedges.append(outedges[i])
    walloutedges=[]
    for w in walldomoutedges:
        woe=[]
        for i in w:
            nextdoms=set(outedges[i])
            for k,o in enumerate(walldomoutedges):
                if nextdoms.intersection(o):
                    woe.append(k)
        walloutedges.append(tuple(woe))
    return walls, walloutedges

def makeVarsAffected(walls):
    affects=[(1,),(2,),(0,),(4,),(5,),(3,6),(1,)]
    varsaffectedatwalls=[]
    for w in walls:
        for k,v in enumerate(w):
            if abs(v-int(v)) < 0.25:
                varsaffectedatwalls.append(k)
                break
    return varsaffectedatwalls

if __name__=='__main__':
    domains=makeDomains()
    outedges=makeDomainGraph(domains)
    walls, walloutedges=makeWallGraph(domains,outedges)
    varsaffectedatwalls=makeVarsAffected(walls)
    for k,(v,w) in enumerate(zip(varsaffectedatwalls,walls)):
        print k,v,w



