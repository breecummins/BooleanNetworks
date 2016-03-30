import matplotlib.pyplot as plt
import numpy as np
import parseLEMscores as LEM
import sys

def generateMasterList(masterfile='/Users/bcummins/ProjectData/malaria/wrair2015_pfalcip_harmonicGenes_forNewLEM/43geneIDs_intersect18-21hrPer_putative661TFs.txt'):
    f=open(masterfile,'r')
    genelist = [l[:-1] for l in f.readlines()]
    f.close()
    return genelist

def makeRankings(genelist,threshold=0, LEMfile='/Users/bcummins/ProjectData/malaria/wrair2015_pfalcip_harmonicGenes_forNewLEM/wrair2015_pfalc_43tf_lem.allscores.tsv'):
    # get LEM scores
    source,target,type_reg,lem_score=LEM.parseFile(threshold,LEMfile)
    # FIXME: LEM scores SHOULD be in order, but sort just in case
    N=len(genelist)
    rowrankings=np.zeros((N,N))
    colrankings=np.zeros((N,N))
    activating_or_repressing=np.empty((N,N),dtype='str')
    for s,t,r,l in zip(source,target,type_reg,lem_score):  
        if l >0:
            i,j=genelist.index(s),genelist.index(t)
            outmax=np.max(rowrankings[i,:])
            inmax=np.max(colrankings[:,j])
            if rowrankings[i,j] == 0:
                rowrankings[i,j] = outmax+1
                activating_or_repressing[i,j] = r
            if colrankings[i,j] ==0:
                colrankings[i,j] = inmax+1
                activating_or_repressing[i,j] = r
    return rowrankings,colrankings,activating_or_repressing

def chooseHighest(numberedges,rowrankings,colrankings,activating_or_repressing,genelist):
    N=len(genelist)
    row_outedges=[]
    col_outedges=[]
    row_regulation=[]
    col_regulation=[]
    for i in range(N):
        inds=np.nonzero([r >0 and r < numberedges+1 for r in rowrankings[i,:]])
        row_outedges.append(tuple(inds[0]))
        row_regulation.append(tuple([activating_or_repressing[i,q] for q in inds[0]]))
        inds=np.nonzero([r >0 and r < numberedges+1 for r in colrankings[:,i]])
        col_outedges.append(tuple(inds[0]))
        col_regulation.append(tuple([activating_or_repressing[q,i] for q in inds[0]]))
    return row_outedges, col_outedges, row_regulation, col_regulation

def getSCC(row_outedges,col_outedges, row_regulation, col_regulation,genelist):
    row_scc=LEM.strongConnectIndices(row_outedges)
    row_gene_names=[genelist[g] for G in row_scc   for g in G]
    col_scc=LEM.strongConnectIndices(col_outedges)
    col_gene_names=[genelist[g] for G in col_scc   for g in G]
    new_row_outedges,new_row_regulation=pruneOutedges(row_scc, row_outedges, row_regulation)
    new_col_outedges,new_col_regulation=pruneOutedges(col_scc, col_outedges, col_regulation)
    return new_row_outedges, new_col_outedges, new_row_regulation, new_col_regulation, row_gene_names, col_gene_names

def pruneOutedges(scc, outedges, regulation):
    flatscc = [s for S in scc for s in S]
    new_outedges,new_regulation=[],[]
    for k in flatscc:
        otup,rtup=[],[]
        for o,r in zip(outedges[k],regulation[k]):
            if o in flatscc:
                otup.append(flatscc.index(o)), rtup.append(r)
        new_outedges.append(tuple(otup))
        new_regulation.append(tuple(rtup))
    return new_outedges,new_regulation   

def graphNetworks(numberedges=2):
    genelist=generateMasterList()
    rowrankings,colrankings,activating_or_repressing=makeRankings(genelist)
    row_outedges, col_outedges, row_regulation, col_regulation=chooseHighest(numberedges,rowrankings,colrankings,activating_or_repressing,genelist)
    row_outedges, col_outedges, row_regulation, col_regulation, row_gene_names, col_gene_names= getSCC(row_outedges,col_outedges, row_regulation, col_regulation,genelist)
    print sum([len(c) for c in col_outedges]),len(col_gene_names)
    print sum([len(c) for c in row_outedges]),len(row_gene_names)
    LEM.makeGraph(row_gene_names,genelist,row_outedges,row_regulation,name='graph_row_topnumedges{:02d}.png'.format(numberedges))
    LEM.makeGraph(col_gene_names,genelist,col_outedges,col_regulation,name='graph_col_topnumedges{:02d}.png'.format(numberedges))

if __name__=='__main__':
    graphNetworks(2)
