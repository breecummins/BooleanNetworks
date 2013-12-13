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

def getSigmas(doms,binnedsigmas,ainds,logicmap):
    '''
    Find the sigma bounds in the domains.  
    Sigma is the same as the focal point if the decay rates are all 1.

    '''
    sigs=[]
    for d in doms:
        s=[]
        for j,a in enumerate(ainds):
            bmap = tuple([d[_i] for _i in a]) # get the map for target j
            for k,m in enumerate(logicmap[j]):
                if m == bmap:
                    s.append(binnedsigmas[j][k])
                    break
        sigs.append(s)    
    return sigs

def translatelogicfunction(variables,affectedby,states,logicmap,binnedsigmas):
    ainds = makeParameterArrays(variables, affectedby)
    doms = getDomains(states)
    sigs = getSigmas(doms,binnedsigmas,ainds,logicmap)
    return doms,sigs

def getNeighbors(doms):
    neighbors = []
    for d in doms:
        n=[]
        for j,e in enumerate(doms):
            diff = np.abs(np.array(d)-np.array(e))
            if np.sum(diff) == 1:
                n.append((j,np.nonzero(diff)[0]))
        neighbors.append(n)
    return neighbors

def testOutgoingEdge(sig1,sig2,thresh):
    return np.sign(sig1 -thresh) >0 and np.sign(sig2-thresh) >0

def getEdges(doms,neighbors,sigs):
    edges = []
    for i,d in enumerate(doms):
        e = []
        for j in neighbors[i]:
            n = doms[j[0]]
            s1 = sigs[i][j[1]] + 0.5
            s2 = sigs[j[0]][j[1]] + 0.5
            thresh = max([d[j[1]],n[j[1]]])
            if testOutgoingEdge(s1,s2,thresh):
                e.append(j[0])
        edges.append(e)
    return edges

def graphNodesEdges(doms,neighbors,edges,fname='example.png'):
    graph = pydot.Dot(graph_type='digraph')
    dnames = [''.join([str(s) for s in d]) for d in doms]
    for j,d in enumerate(doms):
        graph.add_node(pydot.Node(dnames[j]))
    for i,e in enumerate(edges):
        for k in e:
            graph.add_edge(pydot.Edge(dnames[i],dnames[k]))
    graph.write_png(fname)

def makeGraphFromLogic(variables,affectedby,states,logicmap,binnedsigmas,fname='example.png'):
    doms,sigs = translatelogicfunction(variables,affectedby,states,logicmap,binnedsigmas)
    neighbors = getNeighbors(doms)
    edges = getEdges(doms,neighbors,sigs)
    graphNodesEdges(doms,neighbors,edges,fname)
    print('Output saved in '+fname)

if __name__=='__main__':
    # # define the interactions between variables
    # variables = ['x','y1','y2','y3','z','w1','w2','w3']
    # affectedby = [['x','y3','z','w1'],['x'],['x','y1','w1'],['y2','w1'],['x','w2'],['y2','w2'],['w1','w3'],['x','w2']]
    # # give the thresholds for each interaction
    # thresholds = [[2,1,1,2],[1],[4,1,1],[1,2],[3,1],[1,1],[1,1],[3,1]]
    # define the interactions between variables
    variables = ['x','y1','y2','z']
    affectedby = [['x','y2','z'],['x'],['y1'],['x']]
    states = [range(4),range(2),range(2),range(2)]
    logicmap = [[(0,0,0),(1,0,0),(2,0,0),(3,0,0),(0,1,0),(1,1,0),(2,1,0),(3,1,0),(0,0,1),(1,0,1),(2,0,1),(3,0,1),(0,1,1),(1,1,1),(2,1,1),(3,1,1)],[(0,),(1,),(2,),(3,)],[(0,),(1,)],[(0,),(1,),(2,),(3,)]]
    binnedsigmas = [[0,0,3,3,2,2,3,3,0,0,1,1,1,1,3,3],[0,0,0,1],[0,1],[0,1,1,1]]
    makeGraphFromLogic(variables,affectedby,states,logicmap,binnedsigmas)
