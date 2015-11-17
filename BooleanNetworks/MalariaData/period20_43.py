import matplotlib.pyplot as plt
import numpy as np
import parseLEMscores as LEM

def generateMasterList(fname='/Users/bcummins/ProjectData/malaria/wrair2015_pfalcip_harmonicGenes_forNewLEM/43geneIDs_intersect18-21hrPer_putative661TFs.txt'):
    f=open(fname,'r')
    genelist = [l[:-1] for l in f.readlines()]
    f.close()
    return genelist

def timeSeriesParserPlotter(genes,masterlist,fname='/Users/bcummins/ProjectData/malaria/wrair2015_pfalcip_harmonicGenes_forNewLEM/wrair2015_pfalc_43tf_20hrPer_lem.tsv',savename='timeseries_malaria_8node_43_20hr.pdf'):
    f=open(fname,'r')
    for _ in range(5):
        f.readline()
    genelist=f.readline().split()[1:]
    times=[[float(w) for w in l.split()[1:]] for l in f.readlines()]
    timeseries=np.array(times).transpose()
    plt.clf()
    fig=plt.figure()
    NUM_COLORS = len(genes)
    cm = plt.get_cmap('spectral')
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set_color_cycle([cm(1.*i/NUM_COLORS) for i in range(NUM_COLORS)])
    plt.hold('on')
    times=range(0,61,3)
    leg=[]
    for g in genes:
        ind=genelist.index(g)
        M=max(timeseries[ind])
        plt.plot(times,[t/M for t in timeseries[ind]],linewidth=2)
        leg.append(str(masterlist.index(g)) + ' ' + g)
    leghandle=plt.legend(leg,loc='center left', bbox_to_anchor=(1, 1))
    # plt.show()
    plt.savefig(savename, bbox_extra_artists=(leghandle,), bbox_inches='tight')
    plt.close('all')
    
def plotTimeSeries():
    masterlist=generateMasterList()
    # genes=['PF3D7_0504700','PF3D7_0506700', 'PF3D7_0818700','PF3D7_0925700','PF3D7_0403500','PF3D7_1115500','PF3D7_1350900','PF3D7_0919000','PF3D7_1406100','PF3D7_0614800','PF3D7_1237800','PF3D7_0809900']
    for g in masterlist:
        timeSeriesParserPlotter([g],masterlist,savename='timeseries_malaria_43_20hr_gene{:02d}.pdf'.format(masterlist.index(g)))

def generateResult(topscores=350,threshold=0.1,scorename='350',thresholdname='00',makegraph=1,saveme=1,onlylargestnetwork=0,LEMfile='/Users/bcummins/ProjectData/malaria/wrair2015_pfalcip_462TF_forLEM/wrair2015_pfalc_462tf_lem.allscores.tsv',masterfile='/Users/bcummins/ProjectData/malaria/wrair2015_pfalcip_462TF_forLEM/cuffNorm_subTFs_stdNames.txt'):
    print 'Parsing file...'
    source,target,type_reg,lem_score=LEM.parseFile(threshold,LEMfile)
    genes=LEM.chooseGenes(topscores,source,target)
    # print genes
    print 'Making outedges...'
    outedges,regulation,LEM_scores=LEM.makeOutedges(genes,source,target,type_reg,lem_score)
    # print outedges
    grouped_scc_gene_inds=LEM.strongConnectIndices(outedges)
    num_scc=len(grouped_scc_gene_inds)
    num_scc_nodes=[len(g) for g in grouped_scc_gene_inds]
    scc_genenames=[[genes[g]  for g in G] for G in grouped_scc_gene_inds ]
    # print scc_genes
    print 'Pruning outedges...'
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
    outedges,regulation,LEM_scores=LEM.pruneOutedges(flat_scc_gene_inds,outedges,regulation,LEM_scores)
    if makegraph:
        genelist=generateMasterList(masterfile)
    if makegraph:
        print 'Making graph for {} nodes and {} edges....'.format(len(flat_scc_gene_inds),len([o for oe in outedges for o in oe]))
        LEM.makeGraph(flat_scc_genenames,genelist,outedges,regulation,name='graph_topscores{}_thresh{}.png'.format(scorename,thresholdname))
    if saveme:
        f=open('data_topscores{}_thresh{}.txt'.format(scorename,thresholdname),'w')
        f.write('{} top scores and threshold of {}'.format(topscores,threshold)+'\n')
        f.write('{} nodes and {} edges'.format(len(flat_scc_gene_inds),len([o for oe in outedges for o in oe]))+'\n')
        f.write('{} strongly connected component(s) with {} nodes in each'.format(num_scc,num_scc_nodes)+'\n')
        f.write(str(scc_genenames)+'\n')
        f.write(str(outedges)+'\n')
        f.write(str(regulation)+'\n')
        f.write(str(LEM_scores))
        f.close()
    return num_scc,num_scc_nodes,scc_genenames

def makeTable(topscorelist,thresholdlist,makegraph=1,saveme=0,onlylargestnetwork=1,tableformat=0,LEMfile='/Users/bcummins/ProjectData/malaria/wrair2015_pfalcip_462TF_forLEM/wrair2015_pfalc_462tf_lem.allscores.tsv',masterfile='/Users/bcummins/ProjectData/malaria/wrair2015_pfalcip_462TF_forLEM/cuffNorm_subTFs_stdNames.txt'):
    if tableformat:
        f=open('data_maxnumnodes.txt','w')
        g=open('data_lenscc.txt','w')
    for topscore in topscorelist:
        for k,threshold in enumerate(thresholdlist):
            print topscore, threshold
            num_scc,num_scc_nodes,scc_genenames=generateResult(topscore,threshold,str(topscore),str(k).zfill(2),makegraph=makegraph,saveme=saveme,onlylargestnetwork=onlylargestnetwork,LEMfile=LEMfile,masterfile=masterfile)
            for name in [s for genenames in scc_genenames for s in genenames]:
                print name
            if tableformat:
                if threshold>thresholdlist[-1]:
                    f.write(str(max(num_scc_nodes))+' & ')
                    g.write(str(num_scc)+' & ')
                else:
                    f.write(str(max(num_scc_nodes))+'\n')
                    g.write(str(num_scc)+'\n')
    if tableformat:
        f.close()
        g.close()

if __name__=='__main__':
    plotTimeSeries()


    # topscorelist=[50,75,100,200]
    # thresholdlist=[0.1,0.01,0.005,0.006,0.007,0.008,0.009,1.e-4,9.e-5,8.e-5,7.e-5,6.e-5,5.e-5,4.5e-5,4.e-5,3.e-5,2.e-5,1.e-5]
    # LEMfile='/Users/bcummins/ProjectData/malaria/wrair2015_pfalcip_harmonicGenes_forNewLEM/wrair2015_pfalc_43tf_lem.allscores.tsv'
    # masterfile='/Users/bcummins/ProjectData/malaria/wrair2015_pfalcip_harmonicGenes_forNewLEM/43geneIDs_intersect18-21hrPer_putative661TFs.txt'
    # tableformat=1
    # saveme=0
    # makegraph=0
    # onlylargestnetwork=0
    # makeTable(topscorelist,thresholdlist,makegraph,saveme,onlylargestnetwork,tableformat,LEMfile,masterfile)