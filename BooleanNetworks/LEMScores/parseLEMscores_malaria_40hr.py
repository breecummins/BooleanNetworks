import parseLEMscores_yeast_mouse as PLS
import parseLEMscores_malaria_20hr as PLS20
from networkbuilder_yeast_mouse import createNetworkFile
import time


def parseLEMfile(bound=0,fname='/Users/bcummins/ProjectData/malaria/wrair2015_v2_fpkm-p1_s19_40hr_highest_ranked_genes/wrair2015_v2_fpkm-p1_s19_90tfs_top25_dljtk_lem_score_table.txt'):
    # returns the source, target, and type of regulation sorted by decreasing LEM score (also returned)
    source=[]
    type_reg=[]
    target=[]
    lem_score=[]
    with open(fname,'r') as f:
        for _ in range(8):
           f.readline()
        for l in f.readlines():
            wordlist=l.split()
            lem = float(wordlist[5])
            if lem>bound:
                target.append(wordlist[0])
                lem_score.append(lem)
                two_words=wordlist[2].split('(')
                type_reg.append(two_words[0])
                source.append(two_words[1][:-1])
    [lem_score,source,target,type_reg] = PLS.sort_by_list_in_reverse(lem_score,[source,target,type_reg])
    return source,target,type_reg,lem_score

def generateResult(threshold=0.1,frontname='malaria40hr_90TF_top25',makegraph=1,saveme=1,onlylargestnetwork=0,LEMfile='/Users/bcummins/ProjectData/malaria/wrair2015_v2_fpkm-p1_s19_40hr_highest_ranked_genes/wrair2015_v2_fpkm-p1_s19_90tfs_top25_dljtk_lem_score_table.txt',new_network_path='',new_network_date='',essential=True):    
    print 'Parsing file...'
    source,target,type_reg,lem_score=parseLEMfile(threshold,LEMfile)
    genes = sorted(set(source).intersection(target))
    # print genes
    print 'Making outedges...'
    outedges,regulation,LEM_scores=PLS20.makeOutedges(genes,source,target,type_reg,lem_score)
    # print outedges
    print 'Extracting strongly connected components...'
    grouped_scc_gene_inds=PLS20.strongConnectIndices(outedges)
    scc_genenames=[[genes[g]  for g in G] for G in grouped_scc_gene_inds ]
    # print scc_genes
    if onlylargestnetwork:
        L = [len(g) for g in grouped_scc_gene_inds]
        ind=L.index(max(L))
        grouped_scc_gene_inds = grouped_scc_gene_inds[ind]
        flat_scc_gene_inds = grouped_scc_gene_inds[:]
        scc_genenames = scc_genenames[ind]
        flat_scc_genenames = scc_genenames[:]
    else:    
        flat_scc_gene_inds= [g for G in grouped_scc_gene_inds for g in G]
        flat_scc_genenames = [s for S in scc_genenames for s in S]
    outedges,regulation,LEM_scores=PLS20.pruneOutedges(flat_scc_gene_inds,outedges,regulation,LEM_scores)
    if makegraph:
        print 'Making graph for {} nodes and {} edges....'.format(len(flat_scc_gene_inds),len([o for oe in outedges for o in oe]))
        PLS.makeGraph(flat_scc_genenames,outedges,regulation,name='{}_graph_thresh{}.pdf'.format(frontname,str(threshold).replace('.','-')))
    if saveme:
        createNetworkFile(flat_scc_genenames,outedges,regulation,new_network_path+'{}D_'.format(len(flat_scc_genenames))+time.strftime("%Y_%m_%d")+'_{}_T{}'.format(frontname,str(threshold).replace('.','-')) + '_essential'*essential +'.txt',[essential]*len(flat_scc_genenames))

if __name__ == "__main__":
    # frontname='malaria40hr_90TF_top25'
    # new_network_path = '/Users/bcummins/GIT/DSGRN/networks/'
    # LEMfile='/Users/bcummins/ProjectData/malaria/wrair2015_v2_fpkm-p1_s19_40hr_highest_ranked_genes/wrair2015_v2_fpkm-p1_s19_90tfs_top25_dljtk_lem_score_table.txt'


    # for threshold in [0.01, 0.0075, 0.005, 0.001]:
    #     generateResult(threshold,frontname,1,1,1,LEMfile,new_network_path,True)

    frontname='malaria40hr_50TF_top25'
    new_network_path = '/Users/bcummins/GIT/DSGRN/networks/'
    LEMfile='/Users/bcummins/ProjectData/malaria/wrair2015_v2_fpkm-p1_s19_40hr_highest_ranked_genes/wrair2015_v2_fpkm-p1_s19_50tfs_top25_dljtk_lem_score_table.txt'
    makegraph=1
    saveme=0
    onlylargestnetwork=0
    essential=True


    for threshold in [0.02]:
        generateResult(threshold,frontname,makegraph,saveme,onlylargestnetwork,LEMfile,new_network_path,essential)
