from parseLEMscores_yeast_mouse import parseFile, makeGraph

def parseLEMfile(threshold=0,fname='/Users/bcummins/ProjectData/yeast/haase-fpkm-p1_yeast_s29_top25dljtk_lem_score_table.txt'):
    source,target,type_reg,lem_score = parseFile(threshold,fname)
    return source,target,type_reg,lem_score

def parseRankedGenes(fname="/Users/bcummins/ProjectData/yeast/haase-fpkm-p1_yeast_s29_DLxJTK_257TFs.txt"):
    ranked_genes = []
    with open(fname,'r') as f:
        f.readline()
        for l in f.readlines():
            wordlist=l.split()
            ranked_genes.append(wordlist[0])
    return ranked_genes

def addNode(starting_node_list,ranked_genes,source,target,type_reg):
    N = len(starting_node_list)
    new_node = None
    for g in ranked_genes:
        if g not in starting_node_list:
            new_node=g
            break
    if new_node is None:
        return None, None, None
    best_outedge = None
    best_inedge = None
    for (s,t,r) in zip(source,target,type_reg):
        if s == new_node and t in starting_node_list and best_outedge is None:
            best_outedge = (N,starting_node_list.index(t),r)
        elif s in starting_node_list and t == new_node and best_inedge is None:
            best_inedge = (starting_node_list.index(s),N,r)
        elif best_outedge is not None and best_inedge is not None:
            break
    return new_node, best_inedge, best_outedge

def addEdges(number_new_edges,starting_node_list,starting_graph,starting_regulation,source,target,type_reg):
    new_edges = []
    for (s,t,r) in zip(source,target,type_reg):
        if s in starting_node_list and t in starting_node_list:
            s_ind = starting_node_list.index(s)
            t_ind = starting_node_list.index(t)
            outedges = starting_graph[s_ind]
            if t_ind in outedges and r != starting_regulation[s_ind][outedges.index(t_ind)]:
                new_edges.append((s_ind,t_ind,r))
            elif t_ind not in outedges:
                new_edges.append((s_ind,t_ind,r))
            if len(new_edges) == number_new_edges:
                return new_edges
    return new_edges

def outputNetworkFile(node_list,graph,regulation,fname,essential=None):
    # which edges are essential
    if essential is None:
        essential = [False]*len(node_list)
    # calculate inedges and get regulation type
    dual=[[(j,reg[outedges.index(node)]) for j,(outedges,reg) in enumerate(zip(graph,regulation)) if node in outedges] for node in range(len(node_list))]
    # auto-generate network file for database  
    with open(fname,'w') as f:
        for (name,inedgereg,ess) in zip(node_list,dual,essential):
            act = "(" + " + ".join([node_list[i] for (i,r) in inedgereg if r == 'a']) + ")"
            if len(act)==2:
                act = ""
            rep = "".join(["(~"+node_list[i]+")" for (i,r) in inedgereg if r == 'r'])
            if ess:
                f.write(name + " : " + act + rep + " : E\n")
            else:
                f.write(name + " : " + act + rep + "\n")

def makeGraphFromNetworkFile(network_filename):
    pass

def makeNearbyNetwork(starting_node_list,starting_graph,starting_regulation,LEMfile,ranked_genes_file,network_filename = "network",number_new_edges=0,add_new_node=True,draw_network=False):
    # if adding a node, two new edges will be added and number_new_edges is ignored
    source,target,type_reg,lem_score = parseLEMfile(fname=LEMfile)
    ranked_genes = parseRankedGenes(fname=ranked_genes_file)
    if add_new_node:
        new_node, best_inedge, best_outedge = addNode(starting_node_list,ranked_genes,source,target,type_reg)
        node_list = starting_node_list + [new_node]
        graph = starting_graph + [[]]
        regulation = starting_regulation + [[]]
        graph[best_inedge[0]].append(best_inedge[1])
        regulation[best_inedge[0]].append(best_inedge[2])
        graph[best_outedge[0]].append(best_outedge[1])
        regulation[best_outedge[0]].append(best_outedge[2])
    elif number_new_edges:
        new_edges = addEdges(number_new_edges,starting_node_list,starting_graph,starting_regulation,source,target,type_reg)
        node_list = starting_node_list
        graph = starting_graph
        regulation = starting_regulation
        for (s_ind,t_ind,r) in new_edges:
            outedges = graph[s_ind]
            if t_ind in outedges:
                regulation[s_ind][outedges.index[t_ind]] = r
            else:
                graph[s_ind] = outedges + [t_ind]
                regulation[s_ind] = regulation[s_ind] + [r]
    outputNetworkFile(node_list,graph,regulation,network_filename+".txt")
    if draw_network:
        makeGraph(node_list,graph,regulation,network_filename+".pdf")
    
if __name__ == "__main__":
    starting_node_list=['FKH1','SPT21','PLM2','SWI4','WTM2']
    starting_regulation=[['r','r'],['a','r'],['a'],['r'],['r']]
    starting_graph=[[1,3],[2,4],[0],[4],[0]]
    LEMfile = '/Users/bcummins/ProjectData/yeast/haase-fpkm-p1_yeast_s29_top25dljtk_lem_score_table.txt'
    ranked_genes_file = "/Users/bcummins/ProjectData/yeast/haase-fpkm-p1_yeast_s29_DLxJTK_257TFs.txt"
    network_filename = "5D_plus_next_node"
    makeNearbyNetwork(starting_node_list,starting_graph,starting_regulation,LEMfile,ranked_genes_file,network_filename, number_new_edges=0,add_new_node=True,draw_network=False)
    network_filename = "5D_plus_2edges"
    makeNearbyNetwork(starting_node_list,starting_graph,starting_regulation,LEMfile,ranked_genes_file,network_filename, number_new_edges=2,add_new_node=False,draw_network=False)

