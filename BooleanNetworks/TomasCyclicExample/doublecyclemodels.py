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
        self.patternstart,self.patternremainder=fp.parsePatternGenerator()
        self.varnames=fp.parseVars()
        self.domains=self.makeDomains()
        self.domainoutedges=self.makeDomainGraph(self.domains)
        walldomains,walloutedges=self.makeWallGraph(self.domains,self.domainoutedges)
        varsaffectedatwall=self.makeVarsAffected(walldomains)
        self.origwallinds,self.outedges,self.walldomains,self.varsaffectedatwall,self.allwalllabels = pp.filterAll(walloutedges,walldomains,varsaffectedatwall)


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

    def checkAllChange(self):
        # print self.outedges
        scc=pp.strongConnect(self.outedges)
        print scc
        mM=[[0,0] for _ in range(len(self.varnames))]
        for l in self.allwalllabels:
            for w in l:
                for k,c in enumerate(w):
                    if c == 'm':
                        mM[k][0]=1
                    elif c =='M':
                        mM[k][1]=1
        print mM

    def writeGraphViz(self,doms,outedges,fname='graph.gv'):
        f=open(fname,'w')
        f.write('digraph {\n')
        for k in range(len(doms)):
            f.write(str(k)+';\n')
        for k,o in enumerate(outedges):
            for e in o:
                f.write(str(k)+' -> '+str(e)+'\n')
        f.write('}')
        f.close()

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
        f=open('patterngenerator.txt','w') 
        patternstart='x3 max'
        remainder='x1 min, x2 min, x3 min, x1 max, x2 max'
        patternstart='x3 max'
        remainder='x3 min, x4 min, x5 min, x4 max, x5 max'
        patternstart='x3 max'
        remainder='x1 min, x2 min, x3 min, x1 max, x2 max, x4 min, x5 min, x4 max, x5 max'
        f.write(patternstart+'\n')
        f.write(remainder+'\n')
        f.close()

    def writeVars(self):
        f=open('variables.txt','w')
        f.write('0 x1\n1 x2\n2 x3\n3 x4\n4 x5')
        f.close()

    def makeDomains(self):
        L=[[0.5,1.5]]*2+[[0.5,1.5,2.5]]+[[0.5,1.5]]*2        
        return list(itertools.product(*L))

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
                        if (d[2]<=1.5 and (d[1]==1.5 or d[4]==1.5)) or (d[2]>=1.5 and d[1]==0.5 and d[4]==0.5):
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
                        varsaffectedatwalls.append(a[0])
                        break
                    elif k == 2 and v==2:
                        varsaffectedatwalls.append(a[1])
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
    w : ~v : u s

    '''

    def __init__(self):
        doublecyclemodels.__init__(self)

    def writePatterns(self):
        f=open('patterngenerator.txt','w') 
        # patternstart='u max'
        # remainder='u min, v min, w min, v max, w max'
        # patternstart='x max'
        # remainder='x min, y min, z min, y max, z max'
        patternstart='w max, x min, u min'
        remainder='s min, y max, v max, z min, w min, x max, u max, s max, y min, v min, z max'
        # patternstart='w max, x min, u min, s min, y max, v max, z min, w min, x max, u max, s max, y min, v min'
        # remainder='z max'
        f.write(patternstart+'\n')
        f.write(remainder+'\n')
        f.close()

    def writeVars(self):
        f=open('variables.txt','w')
        f.write('0 x\n1 y\n2 z\n3 s\n4 u\n5 v\n6 w')
        f.close()

    def makeDomains(self):
        L=[[0.5,1.5]]*6+[[0.5,1.5,2.5]]
        return list(itertools.product(*L))

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
                    elif ind==3:
                        if (d[3]==0.5 and d[6]<=1.5) or (d[3]==1.5 and d[6]==2.5):
                            edges.append(j)
                    elif ind==4:
                        if (d[4]==0.5 and d[6]==0.5) or (d[4]==1.5 and d[6]>=1.5):
                            edges.append(j)
                    elif ind==5:
                        if (d[5]==0.5 and d[4]==0.5) or (d[5]==1.5 and d[4]==1.5):
                            edges.append(j)
                    elif ind==6:
                        if (d[6]<=1.5 and d[5]==0.5) or (d[6]>=1.5 and d[5]==1.5):
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
                        varsaffectedatwalls.append(a[1])
                        break
                    elif k == 6 and v==2:
                        varsaffectedatwalls.append(a[0])
                        break
        return varsaffectedatwalls

class twointermediatenodesymmetric(doublecyclemodels):
    '''
    x1 : x3 : x2
    x2 : ~x1 : x8 x3
    x3 : x2+x7 : x1
    x4 : x6 : x7 x5
    x5 : x4 : x6
    x6 : ~x5 : x4
    x7 : x4 : x3
    x8 : x2 : x6

    '''

    def __init__(self):
        doublecyclemodels.__init__(self)

    def writePatterns(self):
        f=open('patterngenerator.txt','w') 
        patternstart='x1 max'
        remainder='x1 min, x2 min, x3 min, x2 max, x3 max'
        patternstart='x4 max'
        remainder='x4 min, x5 min, x6 min, x5 max, x6 max'
        patternstart='x4 max, x2 max, x7 max, x8 max, x5 max, x3 max'
        remainder='x4 min, x2 min, x7 min, x8 min, x5 min, x3 min, x1 max, x1 min, x6 min, x6 max'
        f.write(patternstart+'\n')
        f.write(remainder+'\n')
        f.close()

    def writeVars(self):
        f=open('variables.txt','w')
        f.write('0 x1\n1 x2\n2 x3\n3 x4\n4 x5\n5 x6\n6 x7\n7 x8')
        f.close()

    def makeDomains(self):
        L=[[0.5,1.5]]+[[0.5,1.5,2.5]]+[[0.5,1.5]]+[[0.5,1.5,2.5]]+[[0.5,1.5]]*4
        return list(itertools.product(*L))

    def makeDomainGraph(self,domains):
        # (x1,x2,x3,x4,x5,x6,x7,x8)
        # (0,1,2,3,4,5,6,7)
        # affectedby=[(2,),(0,),(1,6),(5,),(3,),(4,7),(3,),(1,)]
        outedges=[]
        Domains=np.array(domains)
        for d in Domains:
            diffs=np.abs(Domains-d)
            edges=[]
            for j,r in enumerate(diffs):
                if np.abs(np.sum(r) -1.0)<0.1:
                    ind=np.where(np.abs(r-1.0)<0.1)[0]
                    if ind == 0:
                        if (d[0]==0.5 and d[2]==1.5) or (d[0]==1.5 and d[2]==0.5):
                            edges.append(j)
                    elif ind==1:
                        if (d[1]<=1.5 and d[0]==0.5) or (d[1]>=1.5 and d[0]==1.5):
                            edges.append(j)
                    elif ind==2:
                        if (d[2]==0.5 and (d[1]==2.5 or d[6]==1.5)) or (d[2]==1.5 and d[1]<=1.5 and d[6]==0.5):
                            edges.append(j)
                    elif ind==3:
                        if (d[3]<=1.5 and d[5]==1.5) or (d[3]>=1.5 and d[5]==0.5):
                            edges.append(j)
                    elif ind==4:
                        if (d[4]==0.5 and d[3]==2.5) or (d[4]==1.5 and d[3]<=1.5):
                            edges.append(j)
                    elif ind==5:
                        if (d[5]==0.5 and d[4]==0.5) or (d[5]==1.5 and d[4]==1.5):
                            edges.append(j)
                    elif ind==6:
                        if (d[6]==0.5 and d[3]>=1.5) or (d[6]==1.5 and d[3]==0.5):
                            edges.append(j)
                    elif ind==7:
                        if (d[7]==0.5 and d[1]>=1.5) or (d[7]==1.5 and d[1]==0.5):
                            edges.append(j)
            outedges.append(tuple(edges))
        return outedges

    def makeVarsAffected(self,walls):
        # (x1,x2,x3,x4,x5,x6,x7,x8)
        # (0,1,2,3,4,5,6,7)
        affects=[(1,),(2,7),(0,),(4,6),(5,),(3,),(2,),(5,)]
        varsaffectedatwalls=[]
        for w in walls:
            for k,v in enumerate(w):
                if abs(v-int(v)) < 0.25:
                    a=affects[k]
                    if k in [0,2]+range(4,8):
                        varsaffectedatwalls.append(a[0])
                        break
                    elif k in [1,3] and v==1:
                        varsaffectedatwalls.append(a[1])
                        break
                    elif k in [1,3] and v==2:
                        varsaffectedatwalls.append(a[0])
                        break
        return varsaffectedatwalls

class fullyconnected(doublecyclemodels):
    '''
    x : z+w : y v
    y : (~x)(~u) : z w
    z : y+v : x u
    u : w+z : v y
    v : (~u)(~x) : w z
    w : v+y : u x

    '''

    def __init__(self):
        doublecyclemodels.__init__(self)

    def writePatterns(self):
        f=open('patterngenerator.txt','w') 
        patternstart='x max'
        remainder='x min, y min, z min, y max, z max'
        # patternstart='u max'
        # remainder='u min, v min, w min, v max, w max'
        # patternstart='z max, w max, x max, u max'
        # remainder='x min, y min, z min, u min, v min, w min, y max, v max'
        f.write(patternstart+'\n')
        f.write(remainder+'\n')
        f.close()

    def writeVars(self):
        f=open('variables.txt','w')
        f.write('0 x\n1 y\n2 z\n3 u\n4 v\n5 w')
        f.close()

    def makeDomains(self):
        return list(itertools.product(*[[0.5,1.5,2.5]]*6))

    def makeDomainGraph(self,domains):
        # (x,y,z,u,v,w)
        # (0,1,2,3,4,5)
        # affectedby=[(2,5),(0,3),(1,4),(2,5),(0,3),(1,4)]
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
                        if (d[0]<=1.5 and (d[2]>=1.5 or d[5]==2.5)) or (d[0]>=1.5 and d[2]==0.5 and d[5]==0.5):
                            edges.append(j)
                    elif ind==1:
                        if (d[1]<=1.5 and d[0]==0.5 and d[3]<=1.5) or (d[1]>=1.5 and (d[0]>=1.5 or d[3]==2.5)):
                            edges.append(j)
                    elif ind == 2:
                        if (d[2]<=1.5 and (d[1]>=1.5 or d[4]==2.5)) or (d[2]>=1.5 and d[1]==0.5 and d[4]<=1.5):
                            edges.append(j)
                    elif ind == 3:
                        if (d[3]<=1.5 and (d[2]==2.5 or d[5]>=1.5)) or (d[3]>=1.5 and d[2]<=1.5 and d[5]==0.5):
                            edges.append(j)
                    elif ind==4:
                        if (d[4]<=1.5 and d[0]<=1.5 and d[3]==0.5) or (d[4]>=1.5 and (d[0]==2.5 or d[3]>=1.5)):
                            edges.append(j)
                    elif ind == 5:
                        if (d[5]<=1.5 and (d[1]==2.5 or d[4]>=1.5)) or (d[5]>=1.5 and d[1]<=1.5 and d[4]==0.5):
                            edges.append(j)
            outedges.append(tuple(edges))
        return outedges

    def makeVarsAffected(self,walls):
        # (x,y,z,s,u,v,w)
        # (0,1,2,3,4,5,6)
        affects=[(1,4),(2,5),(0,3),(4,1),(5,2),(3,0)]
        varsaffectedatwalls=[]
        for w in walls:
            for k,v in enumerate(w):
                if abs(v-int(v)) < 0.25:
                    a=affects[k]
                    if v==1:
                        varsaffectedatwalls.append(a[0])
                        break
                    elif v==2:
                        varsaffectedatwalls.append(a[1])
                        break
        return varsaffectedatwalls

class partiallyconnected(doublecyclemodels):
    '''
    x : z+w : y
    y : (~x) : z w
    z : y : x
    u : w : v
    v : (~u) : w
    w : v+y : u x

    '''

    def __init__(self):
        doublecyclemodels.__init__(self)

    def writePatterns(self):
        f=open('patterngenerator.txt','w') 
        patternstart='x max'
        remainder='x min, y min, z min, y max, z max'
        # patternstart='u max'
        # remainder='u min, v min, w min, v max, w max'
        # patternstart='z max, w max, x max, u max, y min, v min, z min, w min, x min, u min, y max'
        # remainder=''
        f.write(patternstart+'\n')
        f.write(remainder+'\n')
        f.close()

    def writeVars(self):
        f=open('variables.txt','w')
        f.write('0 x\n1 y\n2 z\n3 u\n4 v\n5 w')
        f.close()

    def makeDomains(self):
        L=[[0.5,1.5],[0.5,1.5,2.5]] + [[0.5,1.5]]*3 + [[0.5,1.5,2.5]]
        return list(itertools.product(*L))

    def makeDomainGraph(self,domains):
        # (x,y,z,u,v,w)
        # (0,1,2,3,4,5)
        # affectedby=[(2,5),(0,3),(1,4),(2,5),(0,3),(1,4)]
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
                        if (d[0]==0.5 and (d[2]==1.5 or d[5]==2.5)) or (d[0]==1.5 and d[2]==0.5 and d[5]==0.5):
                            edges.append(j)
                    elif ind==1:
                        if (d[1]<=1.5 and d[0]==0.5) or (d[1]>=1.5 and d[0]==1.5):
                            edges.append(j)
                    elif ind == 2:
                        if (d[2]==0.5 and d[1]>=1.5) or (d[2]==1.5 and d[1]==0.5):
                            edges.append(j)
                    elif ind == 3:
                        if (d[3]==0.5 and d[5]>=1.5) or (d[3]==1.5 and d[5]==0.5):
                            edges.append(j)
                    elif ind==4:
                        if (d[4]==0.5 and d[3]==0.5) or (d[4]==1.5 and d[3]==1.5):
                            edges.append(j)
                    elif ind == 5:
                        if (d[5]<=1.5 and (d[1]==2.5 or d[4]==1.5)) or (d[5]>=1.5 and d[1]<=1.5 and d[4]==0.5):
                            edges.append(j)
            outedges.append(tuple(edges))
        return outedges

    def makeVarsAffected(self,walls):
        # (x,y,z,s,u,v,w)
        # (0,1,2,3,4,5,6)
        affects=[(1,4),(2,5),(0,3),(4,1),(5,2),(3,0)]
        varsaffectedatwalls=[]
        for w in walls:
            for k,v in enumerate(w):
                if abs(v-int(v)) < 0.25:
                    a=affects[k]
                    if v==1:
                        varsaffectedatwalls.append(a[0])
                        break
                    elif v==2:
                        varsaffectedatwalls.append(a[1])
                        break
        return varsaffectedatwalls

