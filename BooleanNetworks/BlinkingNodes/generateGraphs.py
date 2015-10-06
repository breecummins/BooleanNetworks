import pydot

def makeGraph(nodes,edges,regulation,nodeON,nodeOFF,edgesON,edgesOFF,name='example.png'):
    graph = pydot.Dot(graph_type='digraph')
    for n in nodes:
        newnode=pydot.Node(n,style="filled",fillcolor="white")
        if n==nodeON:
            newnode.set_fillcolor("green")
        elif n==nodeOFF:
            newnode.set_fillcolor("red")
        graph.add_node(newnode)
    for i,(oe,reg) in enumerate(zip(edges,regulation)):
        for o,r in zip(oe,reg):
            newedge=pydot.Edge(nodes[i],nodes[o])
            if r=='r':
                newedge.set_arrowhead('tee')
            if (i,o) in edgesON:
                newedge.set_color("green")
            elif (i,o) in edgesOFF:
                newedge.set_color("red")
            graph.add_edge(newedge)
    graph.write_png(name)

def makeGraphSequence(nodes,edges,regulation,pattern,fnamestart='example'):
    if pattern[0:2] !=pattern[-2:-1]:
        if pattern[0] == pattern[-1]:
            pattern = pattern+[pattern[1]]
        else:
            pattern.extend(pattern[0:2])
    pat = [tuple(p.split()) for p in pattern] 
    edgesON=[]
    edgesOFF=[]
    for k,(n,m) in enumerate(pat):
        nodeON=''
        nodeOFF=''
        if m=='max':
            nodeON=n
        elif m=='min':
            nodeOFF=n
        for i,(oe,reg) in enumerate(zip(edges,regulation)):
            for e,r in zip(oe,reg):
                if nodes.index(n) == e:
                    if (i,e) in edgesON: edgesON.remove((i,e))
                    elif (i,e) in edgesOFF: edgesOFF.remove((i,e))
        makeGraph(nodes,edges,regulation,nodeON,nodeOFF,edgesON,edgesOFF,name=fnamestart+'{:02d}.png'.format(2*k))
        nodeON=''
        nodeOFF=''
        for i,(oe,reg) in enumerate(zip(edges,regulation)):
            for e,r in zip(oe,reg):
                if nodes.index(n)==i and ((m=='max' and r == 'a') or (m=='min' and r=='r')):
                    edgesON.append((i,e))
                    if (i,e) in edgesOFF:
                        edgesOFF.remove((i,e))
                elif nodes.index(n)==i and ((m=='min' and r == 'a') or (m=='max' and r=='r')):
                    edgesOFF.append((i,e))
                    if (i,e) in edgesON:
                        edgesON.remove((i,e))
        # print edgesON, edgesOFF
        makeGraph(nodes,edges,regulation,nodeON,nodeOFF,edgesON,edgesOFF,name=fnamestart+'{:02d}.png'.format(2*k+1))


def dsgrn5D_Model_B():
    pattern1=['X max','Z max','Y2 max', 'Y1 max', 'Y3 max', 'X min','Y1 min','Y2 min', 'Z min', 'Y3 min']
    pattern2=['X max','Y2 max','Z max', 'Y1 max', 'Y3 max', 'X min','Y1 min', 'Z min','Y2 min', 'Y3 min']
    nodes=['X','Y1','Y2','Y3','Z']
    edges=[(0,1,2,4),(2,),(3,),(0,),(0,)]
    regulation=[('a','a','a','a'),('a',),('a',),('a',),('r',)]
    makeGraphSequence(nodes,edges,regulation,pattern1,'pattern1_5D_Model_B')
    makeGraphSequence(nodes,edges,regulation,pattern2,'pattern2_5D_Model_B')

if __name__=='__main__':
    # nodes=['X1','X2','X3']
    # edges=[(1,2),(0,),(1,)]
    # regulation=[('a','r'),('a',),('a',)]
    # pattern=['X3 max', 'X2 max', 'X1 max','X3 min', 'X2 min', 'X1 min']
    # makeGraphSequence(nodes,edges,regulation,pattern)
    dsgrn5D_Model_B()