from scipy.sparse.csgraph import connected_components
import numpy as np

def strongConnect(outedges):
    adjacencymatrix=np.zeros((len(outedges),len(outedges)))
    for i,o in enumerate(outedges):
        for j in o:
            adjacencymatrix[i,j]=1
    N,components=connected_components(adjacencymatrix,connection="strong")
    return N,components

def strongConnectWallNumbers(outedges):
    N,components=strongConnect(outedges)
    wallcomponents=[]
    for k in range(N):
        inds=[i for i,c in enumerate(components) if c == k]
        if len(inds) > 1:
            wallcomponents.extend(inds)
    return sorted(wallcomponents)

if __name__=='__main__':
    outedges=[(1,),(2,4),(3,),(6,),(0,11),(2,),(5,7),(8,),(7,9),(10,),(),(9,)]
    outedges=[(1,),(2,4),(3,),(6,),(0,11),(2,4),(5,7),(8,),(7,9),(10,),(),(9,)]
    SCC = strongConnect(outedges)
    print SCC[1]
    print strongConnectWallNumbers(outedges)
