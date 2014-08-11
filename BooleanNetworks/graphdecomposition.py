def strongconnect(k,E):
    global indV, index, S
    v=indV[k][2]
    indV[k][0] = index
    indV[k][1] = index
    index = index+1
    S.append(v)
    for e in E[k]:
        if indV[e][0] < 0:
            scc = strongconnect(e,E)
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
        # print(scc)
        SCCs.append(scc)

def getSCCs(V,E):
    # Tarjan's strongly connected components algorithm - see Wikipedia
    # indV = [index,lowlink,v]
    global indV, index, S, SCCs
    index = 0
    S = []
    indV = [[-1,-1,v] for v in V]
    SCCs = []
    for k,v in enumerate(indV):
        if v[0] < 0:
            strongconnect(k,E)
    return SCCs

def Morsegraph(V,E,ss,SCCs):
    # get relationships between strongly connected path components
    reducedscc=[[s] for s in ss]
    for scc in SCCs:
        if len(scc) == 1:
            continue
        else:
            reducedscc.append(scc)
    sccedges=[]
    for i,scc1 in enumerate(reducedscc):
        for k,scc2 in enumerate(reducedscc):
            if i ==k:
                continue
            flag=0
            for s1 in scc1:
                ind1=V.index(s1)
                for s2 in scc2:
                    ind2=V.index(s2)
                    if ind2 in E[ind1]:
                        sccedges.append((i,k))
                        flag=1
                    if flag:
                        break
                if flag:
                    break
    return reducedscc,sccedges




if __name__=='__main__':
    import makegraphs
    dV,dE,wV,wE,ss = makegraphs.getNodesEdges(makegraphs.probspec_4D_singthresh_2cycles)
    print('Domain SCCs')
    SCC=getSCCs(dV,dE)
    print('\n')
    print('Wall SCCs')
    SCCs=getSCCs(wV,wE)
