import numpy as np
import pydot, itertools

def makeParameterArrays(variables, affectedby):
    '''
    The output ainds contains the variable indices for the 
    variables in affectedby. 

    '''
    ainds = []
    for j,a in enumerate(affectedby): #j is index of target
        at = []
        for k,t in enumerate(a):
            at.append(variables.index(t)) #i is index of source
        ainds.append(at)
    return ainds

def getDomains(states):
    return list(itertools.product(*states))

def getWalls(states):
    walls = []
    for j in range(len(states)):
        for k in states[j][1:]:
            otherstates = states[:]
            otherstates[j] = [-k]
            walls.extend(list(itertools.product(*otherstates)))
    return walls

def getSigmas(doms,binnedsigmas,ainds,logicmap):
    '''
    Find the sigma bounds in the domains.  
    Sigma is the same as the focal point if the decay rates are all 1.

    '''
    sigs=[]
    steadystates=[]
    for d in doms:
        # print('\n')
        # print('Domain:')
        # print(d)
        # print('------------')
        s=[]
        for j,a in enumerate(ainds):
            bmap = tuple([d[_i] for _i in a]) # get the map for target j
            # print(a,bmap,logicmap[j])
            for k,m in enumerate(logicmap[j]):
                if m == bmap:
                    s.append(binnedsigmas[j][k])
                    break
            if tuple(s) == d:
                steadystates.append(d)
            # print(len(s)==2)
        sigs.append(s)    
    return sigs,steadystates

def translatelogicfunction(variables,affectedby,states,logicmap,binnedsigmas):
    ainds = makeParameterArrays(variables, affectedby)
    doms = getDomains(states)
    sigs,steadystates = getSigmas(doms,binnedsigmas,ainds,logicmap)
    walls = getWalls(states)
    return doms,sigs,steadystates,walls

def getWallNeighbors(doms,walls):
    neighbors = []
    for w in walls:
        n = []
        w = list(w)
        j = np.nonzero(np.array(w) < 0)[0]
        # print('\n')
        # print(w)
        # print('-------')
        for i,v in enumerate(walls):
            v = list(v)
            k = np.nonzero(np.array(v) < 0)[0]
            w1 = w[:j] + [np.abs(w[j])] + w[j+1:]
            w2 = w[:j] + [np.abs(w[j])-1] + w[j+1:]
            v1 = v[:k] + [np.abs(v[k])] + v[k+1:]
            v2 = v[:k] + [np.abs(v[k])-1] + v[k+1:]
            if w1 == v1 or w1 == v2:
                dom1 = tuple(w1)
            elif w2 == v1 or w2 == v2:
                dom1 = tuple(w2)
            else:
                dom1 = False
            # print((v,dom1))
            # print((w1,w2,v1,v2))
            if dom1:
                for ell,d in enumerate(doms):
                    if d == dom1:
                        break
                n.append((i,ell))
        neighbors.append(n)
    return neighbors

def getDomainNeighbors(doms):
    neighbors = []
    for d in doms:
        n=[]
        for j,e in enumerate(doms):
            diff = np.abs(np.array(d)-np.array(e))
            if np.sum(diff) == 1:
                n.append((j,np.nonzero(diff)[0])) #(domain ind, var ind for thresh on wall)
        neighbors.append(n)
    return neighbors

def testWallOutgoingEdge(mp1,mp2,sig1,sig2,thresh1,thresh2,ss=False):
    outgoing = np.sign(mp1-thresh1) == np.sign(sig1-thresh1)
    incoming = np.sign(mp2-thresh2) != np.sign(sig2-thresh2)
    return outgoing and incoming

def testDomainOutgoingEdge(mp1,sig1,sig2,thresh):
    match = np.sign(sig1 -thresh) == np.sign(sig2-thresh)
    outgoing = np.sign(mp1-thresh) == np.sign(thresh-sig1)
    return match and outgoing

def getWallEdges(doms,walls,neighbors,steadystates,sigs):
    edges = []
    ssedges = []
    for i,w in enumerate(walls):
        e = []
        k1 = np.nonzero(np.array(w)<0)[0]
        thresh1 = np.abs([w[k1]])
        # print('\n')
        # print(w)
        # print('-------')
        for j in neighbors[i]:
            if doms[j[1]] in steadystates:
                continue
            v = walls[j[0]]
            k2 = np.nonzero(np.array(v)<0)[0]
            thresh2 = np.abs([v[k2]])
            s1 = sigs[j[1]][k1] + 0.25
            s2 = sigs[j[1]][k2] + 0.25
            if k1 != k2:
                mpt1 = thresh1+0.5 if v[k1] ==thresh1 else thresh1-0.5
                mpt2 = thresh2+0.5 if w[k2] ==thresh2 else thresh2-0.5
            else:
                mpt1 = np.mean([thresh1,thresh2])
                mpt2 = mpt1
            # if k1==k2:
            #     print('\n')
            #     print((w,thresh1,s1,mpt1))
            #     print((v,thresh2,s2,mpt2))
            if testWallOutgoingEdge(mpt1,mpt2,s1,s2,thresh1,thresh2):
                # print(v)
                e.append(j[0])
        se = []
        for j,ss in enumerate(steadystates):
            diff = np.sum(np.abs(np.abs(w)-np.array(ss)))
            if (diff==1 and ss[k1] < thresh1) or (diff==0 and ss[k1] == thresh1): #if wall is adjacent
                se.append(j)
        edges.append(e)
        ssedges.append(se)
    return edges, ssedges

def getDomainEdges(doms,neighbors,sigs):
    edges = []
    for i,d in enumerate(doms):
        e = []
        for j in neighbors[i]:
            n = doms[j[0]]
            thresh = max([d[j[1]],n[j[1]]])
            try:
                s1 = sigs[i][j[1]] + 0.5
            except:
                print((doms[i],n,sigs[i]))
            s2 = sigs[j[0]][j[1]] + 0.5
            if testDomainOutgoingEdge(d[j[1]]+0.5,s1,s2,thresh):
                e.append(j[0])
        edges.append(e)
    return edges

def graphDomainNodesEdges(doms,edges,fname='domaingraph.png'):
    graph = pydot.Dot(graph_type='digraph')
    dnames = [''.join([str(s) for s in d]) for d in doms]
    for d in dnames:
        graph.add_node(pydot.Node(d))
    for i,e in enumerate(edges):
        for k in e:
            graph.add_edge(pydot.Edge(dnames[i],dnames[k]))
    graph.write_png(fname)

def graphWallNodesEdges(walls,steadystates,edges,ssedges,fname='wallgraph.png'):
    graph = pydot.Dot(graph_type='digraph')
    wnames = ['('+','.join([str(s) if s >= 0 else 'T'+str(np.abs(s)) for s in w])+')' for w in walls] + [''.join([str(s) for s in d]) for d in steadystates]
    for w in wnames:
        graph.add_node(pydot.Node(w))
    for i,e in enumerate(edges):
        for k in e:
            graph.add_edge(pydot.Edge(wnames[i],wnames[k]))
    for i,e in enumerate(ssedges):
        for k in e:
            ind = k+len(walls)
            graph.add_edge(pydot.Edge(wnames[i],wnames[ind]))
    graph.write_png(fname)

def makeGraphFromLogic(variables,affectedby,states,logicmap,binnedsigmas,domfname='domaingraph.png',wallfname='wallgraph.png'):
    doms,sigs,steadystates,walls = translatelogicfunction(variables,affectedby,states,logicmap,binnedsigmas)
    domneighbors = getDomainNeighbors(doms)
    wallneighbors = getWallNeighbors(doms,walls)
    domedges = getDomainEdges(doms,domneighbors,sigs)
    walledges, sswalledges = getWallEdges(doms,walls,wallneighbors,steadystates,sigs)
    graphDomainNodesEdges(doms,domedges,domfname)
    print('Output saved in '+domfname)
    graphWallNodesEdges(walls,steadystates,walledges,sswalledges,wallfname)
    print('Output saved in '+wallfname)

if __name__=='__main__':
    # 3D example, single thresholds: x -> y -> z -> x
    variables = ['x','y','z']
    affectedby = [['z'],['x'],['y']]
    states = [range(2),range(2),range(2)]
    logicmap = [[(0,),(1,)],[(0,),(1,)],[(0,),(1,)]]
    binnedsigmas = [[0,1],[0,1],[0,1]]
    # # 2D example, multiple thresholds: x -> x at thresh 1, x -> z at thresh 2, z -| x
    # variables=['x','z']
    # affectedby=[['x','z'],['x']]
    # states=[range(3),range(2)]
    # logicmap=[[(0,0),(1,0),(2,0),(0,1),(1,1),(2,1)],[(0,),(1,),(2,)]]
    # binnedsigmas=[[0,2,2,0,0,1],[0,0,1]]
    # # 4D example
    # variables = ['x','y1','y2','z']
    # affectedby = [['x','y2','z'],['x'],['y1'],['x']]
    # states = [range(4),range(2),range(2),range(2)]
    # logicmap = [[(0,0,0),(1,0,0),(2,0,0),(3,0,0),(0,1,0),(1,1,0),(2,1,0),(3,1,0),(0,0,1),(1,0,1),(2,0,1),(3,0,1),(0,1,1),(1,1,1),(2,1,1),(3,1,1)],[(0,),(1,),(2,),(3,)],[(0,),(1,)],[(0,),(1,),(2,),(3,)]]
    # binnedsigmas = [[0,0,3,3,2,2,3,3,0,0,1,1,1,1,3,3],[0,0,0,1],[0,1],[0,1,1,1]]
    makeGraphFromLogic(variables,affectedby,states,logicmap,binnedsigmas)
