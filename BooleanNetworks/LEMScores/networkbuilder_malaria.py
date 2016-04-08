from math import sqrt
from parseLEMscores_malaria import parseFile
import networkbuilder_yeast_mouse as NBYM

def parseLEMFile(threshold=0,fname='/Users/bcummins/ProjectData/malaria/wrair2015_pfalcip_harmonicGenes_forNewLEM/wrair2015_pfalc_43tf_lem.allscores.tsv'):
    # malaria LEM files are sorted in descending order according to lem score
    source,target,type_reg,lem_score = parseFile(threshold,fname)
    return source,target,type_reg,lem_score

def sort_by_list(X,Y,reverse):
    # sort Y by the sorted order of X
    newX, newY = [], []
    for (x,y) in sorted(zip(X,Y),reverse=reverse):
        newX.append(x)
        newY.append(y)
    return newX,newY

def rankGenes(genes,LEMfile='/Users/bcummins/ProjectData/malaria/wrair2015_pfalcip_harmonicGenes_forNewLEM/wrair2015_pfalc_43tf_lem.allscores.tsv',outputfile='malaria20hr43rankedgenes.txt'):
    source,target,_=parseLEMFile(bound=0,fname=LEMfile) # do not rank 0-scored edges; source,target are sorted by decreasing lem score
    num_edges = len(source)
    print(num_edges)
    scores = [0]*len(genes)
    for k,(src,tar) in enumerate(zip(source,target)):
        scores[genes.index(src)] += (num_edges-k) # give highest score to top edges
        scores[genes.index(tar)] += (num_edges-k)
    descending_scores, ranked_genes = sort_by_list(scores,genes,reverse=True)
    with open(outputfile,'w') as f:
        for (r,s) in zip(ranked_genes,descending_scores):
            f.write("{}    {}\n".format(r,s))

def makeNearbyNetwork(starting_network_filename,LEMfile,ranked_genes_file,new_network_filename,which_edge_to_add=1,add_new_node=True,draw_network=False,which_node_to_add=1,is_new_node_essential=False,parser=parseLEMfile):
    NBYM.makeNearbyNetwork(starting_network_filename,LEMfile,ranked_genes_file,new_network_filename,which_edge_to_add,add_new_node,draw_network,which_node_to_add,is_new_node_essential,parser)

if __name__=='__main__':
    # genes_20hr=['PF3D7_1115500','PF3D7_1006100','PF3D7_0504700','PF3D7_0604600','PF3D7_1408400','PF3D7_1027000','PF3D7_1103800','PF3D7_0614800','PF3D7_1435700','PF3D7_1405100','PF3D7_0403500','PF3D7_1301500','PF3D7_1428800','PF3D7_0506700','PF3D7_1350900','PF3D7_0925700','PF3D7_0518400','PF3D7_0529500','PF3D7_0809900','PF3D7_1008000','PF3D7_1009400','PF3D7_1225200','PF3D7_1337400','PF3D7_1437000','PF3D7_0313000','PF3D7_0627300','PF3D7_0629800','PF3D7_0704600','PF3D7_0729000','PF3D7_0812600','PF3D7_0818700','PF3D7_0915100','PF3D7_0919000','PF3D7_0926100','PF3D7_1119400','PF3D7_1138800','PF3D7_1225800','PF3D7_1227400','PF3D7_1233600','PF3D7_1237800','PF3D7_1302500','PF3D7_1406100','PF3D7_1412900']
    # rankGenes(genes_20hr)

    # starting files
    starting_network_filename = ""
    LEMfile = '/Users/bcummins/ProjectData/malaria/wrair2015_pfalcip_harmonicGenes_forNewLEM/wrair2015_pfalc_43tf_lem.allscores.tsv'
    ranked_genes_file = "malaria20hr43rankedgenes.txt"

    # # add nodes to starting network
    # new_network_filename = "/Users/bcummins/GIT/DSGRN/networks/8D_2016_04_07_yeastLEM_1stnode_essential.txt"
    # makeNearbyNetwork(starting_network_filename,LEMfile,ranked_genes_file,new_network_filename, add_new_node=True,draw_network=True,which_node_to_add=1,is_new_node_essential=True)
