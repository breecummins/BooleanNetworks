import matplotlib.pyplot as plt
import parseLEMscores as LEM
import pydot

def makeGraphNonTrivial(scc_genes,genes,genelist,outedges,regulation,name='graph_lastedge500.png'):
    flatoutedges = [o for oe in outedges for o in oe]
    graph = pydot.Dot(graph_type='digraph')
    for g in genes:
        if genelist.index(g) in flatoutedges:
            graph.add_node(pydot.Node(genelist.index(g)))
    for i,(oe,reg) in enumerate(zip(outedges,regulation)):
        for o,r in zip(oe,reg):
            if r=='r':
                graph.add_edge(pydot.Edge(genelist.index(genes[scc_genes[i]]),genelist.index(genes[scc_genes[o]]),arrowhead='tee'))
            else:
                graph.add_edge(pydot.Edge(genelist.index(genes[scc_genes[i]]),genelist.index(genes[scc_genes[o]])))
    graph.write_png(name)

def makeGraph(scc_genes,genes,genelist,outedges,regulation,name='graph_lastedge500.png'):
    graph = pydot.Dot(graph_type='digraph')
    for g in genes:
        graph.add_node(pydot.Node(genelist.index(g)))
    for i,(oe,reg) in enumerate(zip(outedges,regulation)):
        for o,r in zip(oe,reg):
            if r=='r':
                graph.add_edge(pydot.Edge(genelist.index(genes[scc_genes[i]]),genelist.index(genes[scc_genes[o]]),arrowhead='tee'))
            else:
                graph.add_edge(pydot.Edge(genelist.index(genes[scc_genes[i]]),genelist.index(genes[scc_genes[o]])))
    graph.write_png(name)

def pruneOutedges(geneinds, outedges, regulation, LEM_scores):
    new_outedges,new_regulation,new_LEM_scores=[],[],[]
    for k in geneinds:
        otup,rtup,ltup=[],[],[]
        # print k,outedges[k]
        for o,r,l in zip(outedges[k],regulation[k],LEM_scores[k]):
            if o in geneinds:
                otup.append(geneinds.index(o)), rtup.append(r), ltup.append(l)
        # print k,tuple([geneinds[o] for o in otup])
        new_outedges.append(tuple(otup))
        new_regulation.append(tuple(rtup))
        new_LEM_scores.append(tuple(ltup)) 
    return new_outedges,new_regulation,new_LEM_scores       

def getEdges(period20,threshold=0,fname='/Users/bcummins/ProjectData/malaria/wrair2015_pfalc_462tf_lem.allscores.tsv',scc=1):
    source,target,type_reg,lem_score=LEM.parseFile(threshold,fname)
    outedges,regulation,LEM_scores=LEM.makeOutedges(period20,source,target,type_reg,lem_score)
    if scc:
        grouped_scc_gene_inds=LEM.strongConnectIndices(outedges)
        flat_scc_gene_inds= [g for G in grouped_scc_gene_inds for g in G]
        scc_outedges,regulation,LEM_scores=pruneOutedges(flat_scc_gene_inds,outedges,regulation,LEM_scores)
    return flat_scc_gene_inds,scc_outedges,regulation,LEM_scores,outedges,source

def makeNetwork(period20,threshold,scc=1,savename='period20_network.png',nontrivial=0):
    genelist,timeseries = LEM.generateMasterList()
    scc_geneinds,outedges,regulation,LEM_scores,old_outedges,source=getEdges(period20,threshold,scc=scc)
    if nontrivial:
        makeGraphNonTrivial(scc_geneinds,period20,genelist,outedges,regulation,name=savename)
    else:
        makeGraph(scc_geneinds,period20,genelist,outedges,regulation,name=savename)
    return outedges,old_outedges,source


def plottimeseries(period20,fname='period20_timeseries.png'):
    genelist,timeseries = LEM.generateMasterList()
    period20_timeseries = []
    masterinds = []
    for p in period20:
        ind = genelist.index(p)
        masterinds.append(ind)
        period20_timeseries.append(timeseries[ind])
    fig=plt.figure()
    plt.hold('on')
    times=range(0,61,3)
    leg=[]
    for p,ts in zip(period20,period20_timeseries):
        plt.plot(times,[t/max(ts) for t in ts])
        leg.append(str(genelist.index(p))+' '+p)
    leghandle=plt.legend(leg,loc='center left', bbox_to_anchor=(1, 1))
    # plt.show()
    plt.savefig(fname, bbox_extra_artists=(leghandle,), bbox_inches='tight')

def network6and15incolor():
    network6node=[60,93,184,188,234,395]
    network15node=[248,100,118,345,14,154,411,17,340,366,176,406,111,288,171]
    print 'Parsing file...'
    source,target,type_reg,lem_score=parseFile(0.1)
    genes=LEM.chooseGenes(750,source,target)
    # print genes
    print 'Making outedges...'
    outedges,regulation,LEM_scores=LEM.makeOutedges(genes,source,target,type_reg,lem_score)
    # print outedges
    grouped_scc_gene_inds=LEM.strongConnectIndices(outedges)
    scc_genenames=[[genes[g]  for g in G] for G in grouped_scc_gene_inds ]
    # print scc_genes
    print 'Pruning outedges...'
    L = [len(g) for g in grouped_scc_gene_inds]
    ind=L.index(max(L))
    grouped_scc_gene_inds = grouped_scc_gene_inds[ind]
    flat_scc_gene_inds = grouped_scc_gene_inds[:]
    scc_genenames = scc_genenames[ind]
    genes = scc_genenames[:]
    outedges,regulation,LEM_scores=LEM.pruneOutedges(flat_scc_gene_inds,outedges,regulation,LEM_scores)
    genelist,timeseries=LEM.generateMasterList()
    print 'Making graph for {} nodes and {} edges....'.format(len(flat_scc_gene_inds),len([o for oe in outedges for o in oe]))
    graph = pydot.Dot(graph_type='digraph')
    for g in genes:
        if genelist.index(g) in network6node: 
            graph.add_node(pydot.Node(genelist.index(g),style="filled",fillcolor='red'))
        elif genelist.index(g) in network15node: 
            graph.add_node(pydot.Node(genelist.index(g),style="filled",fillcolor='green'))
        else:
            graph.add_node(pydot.Node(genelist.index(g)))
    for i,(oe,reg) in enumerate(zip(outedges,regulation)):
        for o,r in zip(oe,reg):
            if genelist.index(genes[i]) in network6node and genelist.index(genes[o]) in network6node:
                if r=='r':
                    graph.add_edge(pydot.Edge(genelist.index(genes[i]),genelist.index(genes[o]),arrowhead='tee',color='red'))
                else:
                    graph.add_edge(pydot.Edge(genelist.index(genes[i]),genelist.index(genes[o]),color='red'))
            elif genelist.index(genes[i]) in network15node and genelist.index(genes[o]) in network15node:
                if r=='r':
                    graph.add_edge(pydot.Edge(genelist.index(genes[i]),genelist.index(genes[o]),arrowhead='tee',color='green'))
                else:
                    graph.add_edge(pydot.Edge(genelist.index(genes[i]),genelist.index(genes[o]),color='green'))
            else:
                if r=='r':
                    graph.add_edge(pydot.Edge(genelist.index(genes[i]),genelist.index(genes[o]),arrowhead='tee'))
                else:
                    graph.add_edge(pydot.Edge(genelist.index(genes[i]),genelist.index(genes[o])))
    graph.write_dot('network6node15nodecolored_40.dot')
  

if __name__=='__main__':
    period20 = ['PF3D7_0504700','PF3D7_0506700','PF3D7_0518400','PF3D7_0729000','PF3D7_0818700','PF3D7_0919000','PF3D7_0925700','PF3D7_1008000','PF3D7_1009400','PF3D7_1138800','PF3D7_1225200','PF3D7_1337400']

    plottimeseries(period20[:2]+period20[3:7],'period20_timeseries_6node.png')
    # LEM.makeTable()
    network6and15incolor()
    # exponents=[10,15,20,22,25]
    # outedgeslist=[]
    # sourcelist=[]
    # sccoutedgeslist=[]
    # for exp,threshold in zip(exponents,[10**(-e) for e in exponents]):
    #     print exp
    #     sccoe,outedges,source=makeNetwork(period20,threshold,scc=1,savename='period20_network_threshexp{}.png'.format(exp),nontrivial=1)
    #     sccoutedgeslist.append(sccoe)
    #     outedgeslist.append(outedges)
    #     sourcelist.append(source)
