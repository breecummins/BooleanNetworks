import numpy as np
import pydot

def graphDomainNodesEdges(nodes,edges,fname='domaingraph.png'):
    graph = pydot.Dot(graph_type='digraph')
    for d in nodes:
        graph.add_node(pydot.Node(d))
    for i,e in enumerate(edges):
        for k in e:
            graph.add_edge(pydot.Edge(nodes[i],k))
    graph.write_png(fname)

nodes = ['01','11','21','00','10','20']
edges = [ [['01'],['21'],['20'],['01'],['00','11'],['10']], [['01'],['11'],['11','20'],['01'],['00','11'],['10']], [['11'],['21'],['20'],['01'],['00','11'],['10']], [['11'],['21'],['20'],['01'],['11'],['10']], [['01'],['21'],['20'],['01'],['11'],['10']] ]

for j in range(5):
    fname='domaingraph'+str(j)+'.png'
    graphDomainNodesEdges(nodes,edges[j],fname)