def strongconnect(k,E):
    global indV, index, S
    v=indV[k][2]
    indV[k][0] = index
    indV[k][1] = index
    index = index+1
    S.append(v)
    for e in E[k]:
        if indV[e][0] < 0:
            strongconnect(e,E)
            indV[k][1] = min(indV[k][1],indV[e][1])
        elif indV[e][2] in S:
            indV[k][1] = min(indV[k][1],indV[e][0])
    if indV[k][0] == indV[k][1]:
        scc = []
        w = S.pop()
        while w != v:
            scc.append(w)
            w = S.pop()
        scc.append(w)
        return scc
    else:
        return None

def getSCCs(V,E):
    # Tarjan's strongly connected components algorithm - see Wikipedia
    # indV = [index,lowlink,v]
    global indV, index, S
    index = 0
    S = []
    indV = [[-1,-1,v] for v in V]
    allsccs = []
    for k,v in enumerate(indV):
        if v[0] < 0:
            allsccs.append(strongconnect(k,E))
    return allsccs

if __name__=='__main__':
    import makegraphs
    dV,dE,wV,wE = makegraphs.getNodesEdges(makegraphs.probspec_2D_multthresh)
    allsccs = getSCCs(dV,dE)
    print(allsccs)