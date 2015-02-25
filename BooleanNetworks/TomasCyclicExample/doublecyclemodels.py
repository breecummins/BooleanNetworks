import itertools
import numpy as np
import BooleanNetworks.PatternMatching.fileparsers as fp
import BooleanNetworks.PatternMatching.preprocess as pp

class doublecyclemodels(object):
    '''
    Superclass for double cycle models.

    '''
    def __init__(self):
        self.writeVars()
        self.writePatterns()
        varnames=fp.parseVars()
        patternnames,patternmaxmin=fp.parsePatterns()
        self.patterns=pp.constructCyclicPatterns(varnames,patternnames,patternmaxmin)
        domains=self.makeDomains()
        domainoutedges=self.makeDomainGraph(domains)
        walldomains,walloutedges=self.makeWallGraph(domains,domainoutedges)
        varsaffectedatwall=self.makeVarsAffected(walldomains)
        self.wallinds,self.walloutedges,self.walldomains,self.varsaffectedatwall,self.allwalllabels = pp.filterAll(walloutedges,walldomains,varsaffectedatwall)

    def writeVars(self):
        '''
        Stub for subclass.

        '''
        return None

    def writePatterns(self):
        '''
        Stub for subclass.

        '''
        return None

    def makeDomains(self):
        '''
        Stub for subclass.

        '''
        return None

    def makeDomainGraph(self,domains):
        '''
        Stub for subclass.

        '''
        return None

    def makeVarsAffected(self,walldomains):
        '''
        Stub for subclass.

        '''
        return None

    def makeWallGraph(self,domains,domainoutedges):
        # make list of walls and wall graph.
        walls=[]
        outdom=[]
        indom=[]
        for o,(n,d) in zip(domainoutedges,enumerate(domains)):
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
            nextdoms=domainoutedges[od]
            for j in range(len(walls)):
                if indom[j]==od and outdom[j] in nextdoms:
                    woe.append(j)
            walloutedges.append(tuple(woe))
        return walls, walloutedges

    def checkDomainOutedges(self,domains,domainoutedges):
        Domains=np.array(domains)
        noedges=[]
        for k,d in enumerate(Domains):
            diffs=np.abs(Domains-d)
            for j,r in enumerate(diffs):
                if np.abs(np.sum(r) -1.0)<0.1:
                    if k not in outedges[j] and j not in outedges[k] and (k,j) not in noedges:
                        noedges.append((j,k))
        return noedges


class symmetric5D(doublecyclemodels):
    '''
    x1 : x3 : x2
    x2 : ~x1 : x3
    x3 : x2+x5 : x1 x4
    x4 : x3 : x5
    x5 : ~x4 : x3

    '''

    def __init__(self):
        doublecyclemodels.__init__(self)

    def writePatterns(self):
        f=open('patterns.txt','w')
        f.write('x1 max, x2 min, x3 min, x1 min, x2 max, x3 max\nx4 max, x5 min, x3 min, x4 min, x5 max, x3 max\nx3 min, x1 min, x4 min, x2 max, x5 max, x3 max, x1 max, x4 max, x2 min, x5 min')
        f.close()

    def writeVars(self):
        f=open('variables.txt','w')
        f.write('0 x1\n1 x2\n2 x3\n3 x4\n4 x5')
        f.close()

    def makeDomains(self):
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

    def makeDomainGraph(self,domains):
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

    def makeVarsAffected(self,walldomains):
        # (x1,x2,x3,x4,x5)
        # (0,1,2,3,4)
        affects=[(1,),(2,),(0,3),(4,),(2,)]
        varsaffectedatwalls=[]
        for w in walldomains:
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


class oneintermediatenode(doublecyclemodels):
    '''
    x : ~z : y
    y : (~x)(~s) : z
    z : ~y : x
    s : ~w : y
    u : ~w : v
    v : ~u : w
    w : ~v : s u

    '''

    def __init__(self):
        doublecyclemodels.__init__(self)

    def writePatterns(self):
        f=open('patterns.txt','w')
        f.write('x max, y max, z max, x min, y min, z min\nx min, y max, z min, x max, y min, z max\nu max, v max, w max, u min, v min, w min\nu min, v max, w min, u max, v min, w max\nv max, x max, w min, s max, y min, u max, z max, v min, x min, s min, w max, y max, u min, z min')
        f.close()

    def writeVars(self):
        f=open('variables.txt','w')
        f.write('0 x\n1 y\n2 z\n3 s\n4 u\n5 v\n6 w')
        f.close()

    def makeDomains(self):
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

    def makeDomainGraph(self,domains):
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

    def makeVarsAffected(self,walls):
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

