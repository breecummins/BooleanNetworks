import numpy as np
import matplotlib.pyplot as plt
import pydot

from scipy.sparse.csgraph import connected_components

def generateMasterList(fname='/Users/bcummins/ProjectData/malaria/wrair2015_pfalcip_462TF_forLEM/cuffNorm_subTFs_stdNames.txt'):
    f=open(fname,'r')
    wordlist = f.readline().split()[22::]
    f.close()
    genelist = wordlist[::22]
    timeseries=[]
    for k in range(len(genelist)):
        timeseries.append([float(w) for w in wordlist[22*k+1:22*(k+1)]])
    return genelist, timeseries

def parseFile(bound=0,fname='/Users/bcummins/ProjectData/malaria/wrair2015_pfalcip_462TF_forLEM/wrair2015_pfalc_462tf_lem.allscores.tsv'):
    f=open(fname,'r')
    source=[]
    type_reg=[]
    target=[]
    lem_score=[]
    f.readline()
    for l in f.readlines():
        wordlist=l.split()
        if float(wordlist[3])>bound:
            target.append(wordlist[0])
            lem_score.append(float(wordlist[3]))
            two_words=wordlist[2].split('(')
            type_reg.append(two_words[0])
            source.append(two_words[1][:-1])
        else:
            break
    f.close()
    return source,target,type_reg,lem_score

def chooseGenes(topscores,source,target):
    return list(set(source[:topscores]).intersection(target[:topscores]))

def makeOutedges(genes,source,target,type_reg,lem_score):
    outedges=[[] for _ in range(len(genes))]
    regulation=[[] for _ in range(len(genes))]
    lem_scores=[[] for _ in range(len(genes))]
    for s,t,tr,l in zip(source,target,type_reg,lem_score):
        if s in genes and t in genes:
            outedges[genes.index(s)].append(genes.index(t))
            regulation[genes.index(s)].append(tr)
            lem_scores[genes.index(s)].append(l)
    return [tuple(oe) for oe in outedges],[tuple(r) for r in regulation],[tuple(l) for l in lem_scores]

def strongConnect(outedges):
    adjacencymatrix=np.zeros((len(outedges),len(outedges)))
    for i,o in enumerate(outedges):
        for j in o:
            adjacencymatrix[i,j]=1
    N,components=connected_components(adjacencymatrix,directed=True,connection="strong")
    return list(components)

def strongConnectIndices(outedges):
    components=strongConnect(outedges)
    grouped_components=[[k for k,c in enumerate(components) if c == d] for d in range(max(components)+1) if components.count(d)>1]
    return grouped_components

def pruneOutedges(geneinds, outedges, regulation, LEM_scores):
    new_outedges,new_regulation,new_LEM_scores=[],[],[]
    for k in geneinds:
        otup,rtup,ltup=[],[],[]
        for o,r,l in zip(outedges[k],regulation[k],LEM_scores[k]):
            if o in geneinds:
                otup.append(geneinds.index(o)), rtup.append(r), ltup.append(l)
        new_outedges.append(tuple(otup))
        new_regulation.append(tuple(rtup))
        new_LEM_scores.append(tuple(ltup)) 
    return new_outedges,new_regulation,new_LEM_scores       

def makeGraph(genes,genelist,outedges,regulation,name='graph_lastedge500.pdf'):
    graph = pydot.Dot(graph_type='digraph')
    for g in genes:
        graph.add_node(pydot.Node(genelist.index(g)))
    for i,(oe,reg) in enumerate(zip(outedges,regulation)):
        for o,r in zip(oe,reg):
            if r=='r':
                graph.add_edge(pydot.Edge(genelist.index(genes[i]),genelist.index(genes[o]),arrowhead='tee'))
            else:
                graph.add_edge(pydot.Edge(genelist.index(genes[i]),genelist.index(genes[o])))
    graph.write_pdf(name)

def generateResult(topscores=350,threshold=0.1,scorename='350',thresholdname='00',makegraph=1,saveme=1,plottimeseries=1,onlylargestnetwork=0,LEMfile='/Users/bcummins/ProjectData/malaria/wrair2015_pfalcip_462TF_forLEM/wrair2015_pfalc_462tf_lem.allscores.tsv',masterfile='/Users/bcummins/ProjectData/malaria/wrair2015_pfalcip_462TF_forLEM/cuffNorm_subTFs_stdNames.txt'):
    print 'Parsing file...'
    source,target,type_reg,lem_score=parseFile(threshold,LEMfile)
    genes=chooseGenes(topscores,source,target)
    # print genes
    print 'Making outedges...'
    outedges,regulation,LEM_scores=makeOutedges(genes,source,target,type_reg,lem_score)
    # print outedges
    grouped_scc_gene_inds=strongConnectIndices(outedges)
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
    outedges,regulation,LEM_scores=pruneOutedges(flat_scc_gene_inds,outedges,regulation,LEM_scores)
    if makegraph or plottimeseries:
        genelist,timeseries=generateMasterList(masterfile)
    if makegraph:
        makeGraph(genes,genelist,outedges,regulation,name='allgenes_topscores{}_thresh{}.pdf'.format(scorename,thresholdname))
        print 'Making graph for {} nodes and {} edges....'.format(len(flat_scc_gene_inds),len([o for oe in outedges for o in oe]))
        makeGraph(flat_scc_genenames,genelist,outedges,regulation,name='graph_topscores{}_thresh{}.pdf'.format(scorename,thresholdname))
    if plottimeseries and onlylargestnetwork:
        # L=[len(g) for g in grouped_scc_gene_inds]
        # ind = L.index(max(L))
        # scc=grouped_scc_gene_inds[ind]
        # sccnames=scc_genenames[ind]
        fig=plt.figure()
        plt.hold('on')
        times=range(0,61,3)
        leg=[]
        for s,sn in zip(flat_scc_gene_inds,flat_scc_genenames):
            plt.plot(times,[t/max(timeseries[s]) for t in timeseries[s]])
            leg.append(str(genelist.index(sn))+' '+sn)
        leghandle=plt.legend(leg,loc='center left', bbox_to_anchor=(1, 1))
        # plt.show()
        plt.savefig('timeseries_largestcomponent_topscores{}_thresh{}.png'.format(scorename,thresholdname), bbox_extra_artists=(leghandle,), bbox_inches='tight')
    if saveme:
        f=open('data_topscores{}_thresh{}.txt'.format(scorename,thresholdname),'w')
        f.write('{} top scores and threshold of {}'.format(topscores,threshold)+'\n')
        f.write('{} nodes and {} edges'.format(len(flat_scc_gene_inds),len([o for oe in outedges for o in oe]))+'\n')
        f.write('{} strongly connected component(s) with {} nodes in each'.format(len(grouped_scc_gene_inds),[len(g) for g in grouped_scc_gene_inds])+'\n')
        f.write(str(scc_genenames)+'\n')
        f.write(str(outedges)+'\n')
        f.write(str(regulation)+'\n')
        f.write(str(LEM_scores))
        f.close()
    return grouped_scc_gene_inds

def makeTable(topscorelist,thresholdlist,makegraph=1,saveme=0,plottimeseries=0,onlylargestnetwork=1,tableformat=0,LEMfile='/Users/bcummins/ProjectData/malaria/wrair2015_pfalcip_462TF_forLEM/wrair2015_pfalc_462tf_lem.allscores.tsv',masterfile='/Users/bcummins/ProjectData/malaria/wrair2015_pfalcip_462TF_forLEM/cuffNorm_subTFs_stdNames.txt'):
    if tableformat:
        f=open('data_maxnumnodes.txt','w')
        g=open('data_lenscc.txt','w')
    for topscore in topscorelist:
        for k,threshold in enumerate(thresholdlist):
            print topscore, threshold
            grouped_scc_gene_inds=generateResult(topscore,threshold,str(topscore),str(k).zfill(2),makegraph=makegraph,saveme=saveme,plottimeseries=plottimeseries,onlylargestnetwork=onlylargestnetwork,LEMfile=LEMfile,masterfile=masterfile)
            if tableformat:
                if threshold>thresholdlist[-1]:
                    f.write(str(max([len(s) for s in grouped_scc_gene_inds]))+' & ')
                    g.write(str(len(grouped_scc_gene_inds))+' & ')
                else:
                    f.write(str(max([len(s) for s in grouped_scc_gene_inds]))+'\n')
                    g.write(str(len(grouped_scc_gene_inds))+'\n')
    if tableformat:
        f.close()
        g.close()

if __name__=='__main__':
    # topscorelist=range(100,1100,100)
    # thresholdlist=[10e-5,10e-10,10e-50,10e-100]
    # LEMfile='/Users/bcummins/ProjectData/malaria/wrair2015_pfalcip_harmonicGenes_forNewLEM/wrair2015_pfalc_43tf_lem.allscores.tsv'
    topscorelist=[650]
    thresholdlist=[0.16]
    LEMfile = '/Users/bcummins/ProjectData/malaria/wrair2015_pfalcip_462TF_forLEM/wrair2015_pfalc_462tf_lem.allscores.tsv'
    tableformat=1
    saveme=0
    makegraph=1
    plottimeseries=0
    onlylargestnetwork=0
    # makeTable(topscorelist,thresholdlist,makegraph,saveme,plottimeseries,onlylargestnetwork,tableformat,LEMfile,masterfile='/Users/bcummins/ProjectData/malaria/wrair2015_pfalcip_462TF_forLEM/cuffNorm_subTFs_stdNames.txt')
    generateResult(topscorelist[0],thresholdlist[0],scorename=str(topscorelist[0]),thresholdname='016',makegraph=makegraph,saveme=saveme,plottimeseries=plottimeseries,onlylargestnetwork=onlylargestnetwork)