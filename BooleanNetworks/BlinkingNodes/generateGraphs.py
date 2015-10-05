import pydot

def makeGraph(nodes,edges,regulation,nodeON,nodeOFF,edgeON,edgeOFF,name='example.png'):
    graph = pydot.Dot(graph_type='digraph')
    for n in nodes:
        newnode=pydot.Node(n,style="filled",fillcolor="white")
        if n==nodeON:
            newnode.set_fillcolor("green")
        elif n==nodeOFF:
            newnode=set_fillcolor("red")
        graph.add_node(newnode)
    for i,(oe,reg) in enumerate(zip(edges,regulation)):
        for o,r in zip(oe,reg):
            newedge=pydot.Edge(nodes[i],nodes[o])
            if r=='r':
                newedge.set_arrowhead('tee')
            if (i,o) == edgeON:
                newedge.set_color("green")
            elif (i,o) == edgeOFF:
                newedge.set_color("red")
            graph.add_edge(newedge)
    graph.write_png(name)

def makeGraphSequence(nodes,edges,regulation,pattern):
    if pattern[0] !=pattern[-1]:
        pattern=pattern+pattern[0]
        pat = [tuple(p.split()) for p in pattern] 
    for k,(n,m) in enumerate(pat):
        if m=='max':
            nodeON=n
        elif m=='min':
            nodeOFF=n




if __name__=='__main__':
    nodes=['X1','X2','X3']
    edges=[(1,2),(0,),(1,)]
    regulation=[('a','r'),('a',),('a',)]
    nodeON='X1'
    nodeOFF=''
    edgeON = ()
    edgeOFF = (0,2)
    makeGraph(nodes,edges,regulation,nodeON,nodeOFF,edgeON,edgeOFF)