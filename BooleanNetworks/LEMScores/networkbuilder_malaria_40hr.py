import networkbuilder_yeast_mouse as NBYM
import parseLEMscores_malaria_40hr as PLS40

def makeNearbyNetwork(starting_network_filename,LEMfile,ranked_genes_file,new_network_filename,which_edge_to_add=1,add_new_node=True,draw_network=False,which_node_to_add=1,is_new_node_essential=False,parser=PLS40.parseLEMfile):
    NBYM.makeNearbyNetwork(starting_network_filename,LEMfile,ranked_genes_file,new_network_filename,which_edge_to_add,add_new_node,draw_network,which_node_to_add,is_new_node_essential,parser)


if __name__ == "__main__":
    # # starting files
    # starting_network_filename = "/Users/bcummins/GIT/DSGRN/networks/12D_2016_04_11_malaria40hr_90TF_top25_T0-005_essential.txt"
    # LEMfile='/Users/bcummins/ProjectData/malaria/wrair2015_v2_fpkm-p1_s19_40hr_highest_ranked_genes/wrair2015_v2_fpkm-p1_s19_90tfs_top25_dljtk_lem_score_table.txt'
    # ranked_genes_file = "/Users/bcummins/ProjectData/malaria/wrair2015_v2_fpkm-p1_s19_40hr_highest_ranked_genes/wrair-fpkm-p1_malaria_s19_DLxJTK_90putativeTFs.txt"

    # # add nodes to starting network
    # new_network_filename = "/Users/bcummins/GIT/DSGRN/networks/13D_2016_04_11_malaria40hr_90TF_top25_T0-005_1stnode_essential.txt"
    # makeNearbyNetwork(starting_network_filename,LEMfile,ranked_genes_file,new_network_filename, add_new_node=True,draw_network=True,which_node_to_add=1,is_new_node_essential=True)

    # # add edges to starting network
    # new_network_filename = "/Users/bcummins/GIT/DSGRN/networks/12D_2016_04_11_malaria40hr_90TF_top25_T0-005_1stedge_essential.txt"
    # makeNearbyNetwork(starting_network_filename,LEMfile,ranked_genes_file,new_network_filename, which_edge_to_add=1,add_new_node=False,draw_network=True)

    # starting files
    starting_network_filename = "/Users/bcummins/GIT/DSGRN/networks/8D_2016_04_11_malaria40hr_50TF_top25_T0-05_essential.txt"
    LEMfile='/Users/bcummins/ProjectData/malaria/wrair2015_v2_fpkm-p1_s19_40hr_highest_ranked_genes/wrair2015_v2_fpkm-p1_s19_50tfs_top25_dljtk_lem_score_table.txt'
    ranked_genes_file = "/Users/bcummins/ProjectData/malaria/wrair2015_v2_fpkm-p1_s19_40hr_highest_ranked_genes/wrair-fpkm-p1_malaria_s19_DLxJTK_50putativeTFs.txt"

    # add nodes to starting network
    new_network_filename = "/Users/bcummins/GIT/DSGRN/networks/9D_2016_04_11_malaria40hr_50TF_top25_T0-05_1stnode_essential.txt"
    makeNearbyNetwork(starting_network_filename,LEMfile,ranked_genes_file,new_network_filename, add_new_node=True,draw_network=True,which_node_to_add=1,is_new_node_essential=True)

    new_network_filename = "/Users/bcummins/GIT/DSGRN/networks/9D_2016_04_11_malaria40hr_50TF_top25_T0-05_2ndnode_essential.txt"
    makeNearbyNetwork(starting_network_filename,LEMfile,ranked_genes_file,new_network_filename, add_new_node=True,draw_network=True,which_node_to_add=2,is_new_node_essential=True)

    new_network_filename = "/Users/bcummins/GIT/DSGRN/networks/9D_2016_04_11_malaria40hr_50TF_top25_T0-05_3rdnode_essential.txt"
    makeNearbyNetwork(starting_network_filename,LEMfile,ranked_genes_file,new_network_filename, add_new_node=True,draw_network=True,which_node_to_add=3,is_new_node_essential=True)


    # add edges to starting network
    new_network_filename = "/Users/bcummins/GIT/DSGRN/networks/8D_2016_04_11_malaria40hr_50TF_top25_T0-05_1stedge_essential.txt"
    makeNearbyNetwork(starting_network_filename,LEMfile,ranked_genes_file,new_network_filename, which_edge_to_add=1,add_new_node=False,draw_network=True)

    new_network_filename = "/Users/bcummins/GIT/DSGRN/networks/8D_2016_04_11_malaria40hr_50TF_top25_T0-05_2ndedge_essential.txt"
    makeNearbyNetwork(starting_network_filename,LEMfile,ranked_genes_file,new_network_filename, which_edge_to_add=2,add_new_node=False,draw_network=True)

    new_network_filename = "/Users/bcummins/GIT/DSGRN/networks/8D_2016_04_11_malaria40hr_50TF_top25_T0-05_3rdedge_essential.txt"
    makeNearbyNetwork(starting_network_filename,LEMfile,ranked_genes_file,new_network_filename, which_edge_to_add=3,add_new_node=False,draw_network=True)



