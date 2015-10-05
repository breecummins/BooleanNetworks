from collections import deque
from functools import partial

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

def breadthfirst(V,E,start,end,queue=deque([])):
    paths = []
    temp_path = [start]
    queue.append(temp_path)
    while queue:
        tpath = queue.popleft()
        last_node = tpath[len(tpath)-1]
        if last_node == end:
            paths.append(tpath)
        for lind in E[V.index(last_node)]:
            link_node = V[lind]
            if link_node not in tpath:
                new_path = tpath+[link_node]
                queue.append(new_path)
    return paths

def transitivereduction(nodes,edges):
    ''' helper function for Morsegraph '''
    reducededges=[[] for _ in range(len(nodes))]
    for i,n1 in enumerate(nodes):
        for k,n2 in enumerate(nodes):
            if n1 != n2:
                paths = breadthfirst(nodes,edges,n1,n2,queue=deque([]))
                if len(paths)==1 and len(paths[0])==2:
                    reducededges[i].append(k)
    return reducededges

def Morsegraph(V,E,ss,SCCs):
    # get relationships between strongly connected path components
    sccnodes=[]
    gradnodes=[]
    for scc in SCCs:
        if len(scc) == 1:
            if scc[0] in ss:
                sccnodes.append(scc)
            else:
                gradnodes.append(scc[0])
        else:
            sccnodes.append(scc)
    sccedges=[[] for _ in range(len(sccnodes))]
    for i,scc1 in enumerate(sccnodes):
        for k,scc2 in enumerate(sccnodes):
            if i == k:
                continue
            flag=0
            for s1 in scc1:
                if not E[V.index(s1)]:
                    continue
                for s2 in scc2:
                    queue=deque([])
                    paths=breadthfirst(V,E,s1,s2,queue)
                    for p in paths:
                        if all([q in gradnodes for q in p[1:-1]]):
                            sccedges[i].append(k)
                            flag=1
                        if flag:
                            break
                    if flag:
                        break
                if flag:
                    break
    sccedges = transitivereduction(sccnodes,sccedges)
    return sccnodes, sccedges



    


if __name__=='__main__':
    import makegraphs
    bs = [[0,0,3,3,2,2,3,3,0,0,1,1,2,2,3,3],[0,1,1,1],[0,1],[0,0,0,1]]
    makegraphs.makeMorseGraph(partial(makegraphs.probspec_4D_ArnaudExample_2A,bs))
    # dV,dE,wV,wE,ss = makegraphs.getNodesEdges(partial(makegraphs.probspec_4D_ArnaudExample_2A,bs))
    # # for d in dV:
    # #     print(d)
    # # print(dE)
    # SCCs=getSCCs(dV,dE)
    # # for s in SCCs:
    # #     print(s)
    # sccnodes, sccedges = Morsegraph(dV,dE,ss,SCCs)
    # print('Domain SCCs')
    # for s in sccnodes:
    #     print(s) 
    # print('Domain SCC edges')
    # print(sccedges)

    # # toy
    # V = range(8)
    # E = [[2],[0,7],[1,3],[5],[6],[4],[5,7],[]]
    # ss = [7]
    # SCCs = [[0,1,2],[4,5,6],[7],[3]]
    # sccnodes, sccedges = Morsegraph2(V,E,ss,SCCs)

    # print('Domain SCCs')
    # for s in sccnodes:
    #     print(s) 
    # print('Domain SCC edges')
    # print(sccedges)
