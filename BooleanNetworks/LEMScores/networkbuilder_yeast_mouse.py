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

def extractSubset(node_list,threshold=0,fname='/Users/bcummins/ProjectData/yeast/haase-fpkm-p1_yeast_s29_top25dljtk_lem_score_table.txt'):
    # for debugging
    source,target,type_reg,lem_score = parseLEMfile(threshold,fname)
    edges = []
    for (s,t,r,l) in zip(source,target,type_reg,lem_score):
        if s in node_list and t in node_list:
            edges.append((s,t,r,l))
    return edges


def addNode(node_list,ranked_genes,source,target,type_reg,which_node_to_add = 1):
    count = 0
    new_node = None
    for g in ranked_genes:
        if g not in node_list:
            count += 1
            if count == which_node_to_add:
                new_node=g
                break
    if new_node is None:
        return None, None, None
    best_outedge = None
    best_inedge = None
    N = len(node_list)
    for (s,t,r) in zip(source,target,type_reg):
        if s == new_node and t in node_list and best_outedge is None:
            best_outedge = (N,node_list.index(t),r)
        elif s in node_list and t == new_node and best_inedge is None:
            best_inedge = (node_list.index(s),N,r)
        elif best_outedge is not None and best_inedge is not None:
            break
    return new_node, best_inedge, best_outedge

def addEdge(which_edge_to_add,node_list,graph,regulation,source,target,type_reg):
    count = 0
    new_edge = None
    for (s,t,r) in zip(source,target,type_reg):
        if s in node_list and t in node_list:
            s_ind = node_list.index(s)
            t_ind = node_list.index(t)
            outedges = graph[s_ind]
            if t_ind not in outedges or r != regulation[s_ind][outedges.index(t_ind)]:
                count += 1
                if count == which_edge_to_add:
                    new_edge = (s_ind,t_ind,r)
                    break
    return new_edge

def createNetworkFile(node_list,graph,regulation,fname,essential=None):
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

def getGraphFromNetworkFile(network_filename):
    node_list = []
    inedges = []
    essential = [] #essentialness is inherited
    with open(network_filename,'r') as nf:
        for l in nf.readlines():
            words = l.replace('(',' ').replace(')',' ').replace('+',' ').split()
            if words[-2:] == [':', 'E']:
                essential.append(True)
                words = words[:-2]
            else:
                essential.append(False)
            node_list.append(words[0])
            inedges.append(words[2:]) # get rid of ':' at index 1
    graph = [[] for _ in range(len(node_list))]
    regulation = [[] for _ in range(len(node_list))]
    for target,edgelist in enumerate(inedges):
        for ie in edgelist:
            if ie[0] == '~':
                ind = node_list.index(ie[1:])
                regulation[ind].append('r') 
            else:
                ind = node_list.index(ie)
                regulation[ind].append('a') 
            graph[ind].append(target)  # change inedges to outedges
    return node_list,graph,regulation,essential


def makeNearbyNetwork(starting_network_filename,LEMfile,ranked_genes_file,new_network_filename,which_edge_to_add=1,add_new_node=True,draw_network=False,which_node_to_add=1,is_new_node_essential=False,parser=parseLEMfile):
    # if adding a node, two new edges will be added connecting the new node to the graph and which_edge_to_add is ignored
    # if not adding a node, which_node_to_add is ignored and which_edge_to_add is used with existing nodes
    starting_node_list,starting_graph,starting_regulation,essential = getGraphFromNetworkFile(starting_network_filename)
    source,target,type_reg,lem_score = parser(fname=LEMfile)
    ranked_genes = parseRankedGenes(fname=ranked_genes_file)
    if add_new_node:
        new_node, best_inedge, best_outedge = addNode(starting_node_list,ranked_genes,source,target,type_reg,which_node_to_add)
        if new_node is None:
            raise ValueError("No new node to add.")
        # best_*edge = (source, target, regulation)
        node_list = starting_node_list + [new_node]
        graph = starting_graph + [[]]
        regulation = starting_regulation + [[]]
        graph[best_inedge[0]].append(best_inedge[1])
        regulation[best_inedge[0]].append(best_inedge[2])
        graph[best_outedge[0]].append(best_outedge[1])
        regulation[best_outedge[0]].append(best_outedge[2])
        essential.append(is_new_node_essential)
    else:
        new_edge = addEdge(which_edge_to_add,starting_node_list,starting_graph,starting_regulation,source,target,type_reg)        
        if new_edge is None:
            raise ValueError("No new edge to add.")
        else:
            (s,t,r) = new_edge # new_edge = (source,target,regulation)
        node_list = starting_node_list
        graph = starting_graph
        regulation = starting_regulation
        outedges = graph[s]
        if t in outedges:
            regulation[s][outedges.index[t]] = r
        else:
            graph[s].append(t)
            regulation[s].append(r)
    createNetworkFile(node_list,graph,regulation,new_network_filename,essential)
    if draw_network:
        makeGraph(node_list,graph,regulation,new_network_filename.replace(".txt",".pdf"))
    
if __name__ == "__main__":
    # starting files
    starting_network_filename = "/Users/bcummins/GIT/DSGRN/networks/7D_2016_04_05_yeastLEMoriginal_essential.txt"
    LEMfile = '/Users/bcummins/ProjectData/yeast/haase-fpkm-p1_yeast_s29_top25dljtk_lem_score_table.txt'
    ranked_genes_file = "/Users/bcummins/ProjectData/yeast/haase-fpkm-p1_yeast_s29_DLxJTK_257TFs.txt"

    # # add nodes to starting network
    # new_network_filename = "/Users/bcummins/GIT/DSGRN/networks/8D_2016_04_07_yeastLEM_1stnode_essential.txt"
    # makeNearbyNetwork(starting_network_filename,LEMfile,ranked_genes_file,new_network_filename, add_new_node=True,draw_network=True,which_node_to_add=1,is_new_node_essential=True)

    # new_network_filename = "/Users/bcummins/GIT/DSGRN/networks/8D_2016_04_07_yeastLEM_2ndnode_essential.txt"
    # makeNearbyNetwork(starting_network_filename,LEMfile,ranked_genes_file,new_network_filename, add_new_node=True,draw_network=True,which_node_to_add=2,is_new_node_essential=True)

    # new_network_filename = "/Users/bcummins/GIT/DSGRN/networks/8D_2016_04_07_yeastLEM_3rdnode_essential.txt"
    # makeNearbyNetwork(starting_network_filename,LEMfile,ranked_genes_file,new_network_filename, add_new_node=True,draw_network=True,which_node_to_add=3,is_new_node_essential=True)

    # new_network_filename = "/Users/bcummins/GIT/DSGRN/networks/8D_2016_04_07_yeastLEM_4thnode_essential.txt"
    # makeNearbyNetwork(starting_network_filename,LEMfile,ranked_genes_file,new_network_filename, add_new_node=True,draw_network=True,which_node_to_add=4,is_new_node_essential=True)

    # new_network_filename = "/Users/bcummins/GIT/DSGRN/networks/8D_2016_04_07_yeastLEM_5thnode_essential.txt"
    # makeNearbyNetwork(starting_network_filename,LEMfile,ranked_genes_file,new_network_filename, add_new_node=True,draw_network=True,which_node_to_add=5,is_new_node_essential=True)

    # # add edges to starting network
    # new_network_filename = "/Users/bcummins/GIT/DSGRN/networks/7D_2016_04_07_yeastLEM_1stedge_essential.txt"
    # makeNearbyNetwork(starting_network_filename,LEMfile,ranked_genes_file,new_network_filename, which_edge_to_add=1,add_new_node=False,draw_network=True)

    # new_network_filename = "/Users/bcummins/GIT/DSGRN/networks/7D_2016_04_07_yeastLEM_2ndedge_essential.txt"
    # makeNearbyNetwork(starting_network_filename,LEMfile,ranked_genes_file,new_network_filename, which_edge_to_add=2,add_new_node=False,draw_network=True)

    # new_network_filename = "/Users/bcummins/GIT/DSGRN/networks/7D_2016_04_07_yeastLEM_3rdedge_essential.txt"
    # makeNearbyNetwork(starting_network_filename,LEMfile,ranked_genes_file,new_network_filename, which_edge_to_add=3,add_new_node=False,draw_network=True)

    # new_network_filename = "/Users/bcummins/GIT/DSGRN/networks/7D_2016_04_07_yeastLEM_4thedge_essential.txt"
    # makeNearbyNetwork(starting_network_filename,LEMfile,ranked_genes_file,new_network_filename, which_edge_to_add=4,add_new_node=False,draw_network=True)

    # new_network_filename = "/Users/bcummins/GIT/DSGRN/networks/7D_2016_04_07_yeastLEM_5thedge_essential.txt"
    # makeNearbyNetwork(starting_network_filename,LEMfile,ranked_genes_file,new_network_filename, which_edge_to_add=5,add_new_node=False,draw_network=True)

    for t in extractSubset(['FKH1','SPT21','PLM2','SWI4','WTM2','NDD1','HCM1'],threshold=0,fname=LEMfile):
        print t

    # for g in makeGraphFromNetworkFile(network_filename+'.txt'):
    #     print g
