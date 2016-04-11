import parseLEMscores_malaria_20hr as parseLEMscores
import pydot

def parseFile(bound=0,fname='/Users/bcummins/ProjectData/yeast/haase-fpkm-p1_yeast_s29_top25dljtk_lem_score_table.txt'):
    # returns the source, target, and type of regulation sorted by decreasing LEM score (also returned)
    source=[]
    type_reg=[]
    target=[]
    lem_score=[]
    with open(fname,'r') as f:
        f.readline()
        f.readline()
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
    [lem_score,source,target,type_reg] = sort_by_list_in_reverse(lem_score,[source,target,type_reg])
    return source,target,type_reg,lem_score

def sort_by_list_in_reverse(X,Y):
    # sort every list in Y by the reverse sorted order of X
    newlists = [[] for _ in range(len(Y)+1)]
    for ztup in sorted(zip(X,*Y),reverse=True):
        for k,z in enumerate(ztup):
            newlists[k].append(z)
    return newlists

def makeGraph(genes,outedges,regulation,name='graph_lastedge500.pdf'):
    graph = pydot.Dot(graph_type='digraph')
    for g in genes:
        graph.add_node(pydot.Node(g))
    for i,(oe,reg) in enumerate(zip(outedges,regulation)):
        for o,r in zip(oe,reg):
            if r=='r':
                graph.add_edge(pydot.Edge((genes[i],genes[o]),arrowhead='tee'))
            else:
                graph.add_edge(pydot.Edge(genes[i],genes[o]))
    graph.write_pdf(name)

def generateResult(threshold=0.1,frontname='yeast25',makegraph=1,saveme=1,onlylargestnetwork=0,LEMfile='/Users/bcummins/ProjectData/yeast/haase-fpkm-p1_yeast_s29_top25dljtk_lem_score_table.txt'):
    print 'Parsing file...'
    source,target,type_reg,lem_score=parseFile(threshold,LEMfile)
    genes = sorted(set(source).intersection(target))
    # print genes
    print 'Making outedges...'
    outedges,regulation,LEM_scores=parseLEMscores.makeOutedges(genes,source,target,type_reg,lem_score)
    # print outedges
    print 'Extracting strongly connected components...'
    grouped_scc_gene_inds=parseLEMscores.strongConnectIndices(outedges)
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
    outedges,regulation,LEM_scores=parseLEMscores.pruneOutedges(flat_scc_gene_inds,outedges,regulation,LEM_scores)
    if makegraph:
        print 'Making graph for {} nodes and {} edges....'.format(len(flat_scc_gene_inds),len([o for oe in outedges for o in oe]))
        makeGraph(flat_scc_genenames,outedges,regulation,name='{}_graph_thresh{}.pdf'.format(frontname,str(threshold).replace('.','-')))
    if saveme:
        f=open('{}_data_thresh{}.txt'.format(frontname,str(threshold).replace('.','-')),'w')
        f.write('Threshold of {}'.format(threshold)+'\n')
        f.write('{} nodes and {} edges'.format(len(flat_scc_gene_inds),len([o for oe in outedges for o in oe]))+'\n')
        f.write('{} strongly connected component(s) with {} nodes in each'.format(len(grouped_scc_gene_inds),[len(g) for g in grouped_scc_gene_inds])+'\n')
        f.write(str(scc_genenames)+'\n')
        f.write(str(outedges)+'\n')
        f.write(str(regulation)+'\n')
        f.write(str(LEM_scores))
        f.close()
    return grouped_scc_gene_inds

if __name__ == "__main__":
    # for t in [0.5,0.4,0.1,0.05]:
    #     generateResult(threshold=t,saveme=0)

    # for t in [0.4,0.3,0.2,0.1]:
    #     generateResult(threshold=t,saveme=0,frontname='yeast40',LEMfile='/Users/bcummins/ProjectData/yeast/haase-fpkm-p1_yeast_s29_top40dljtk_lem_score_table.txt')

    for t in [0.6,0.5,0.4,0.3,0.2,0.1]:
        generateResult(threshold=t,saveme=0,frontname='mouseliver40',LEMfile='/Users/bcummins/ProjectData/mouseliver/hogenesch-10st2013_livr_top40dljtk_lem_score_table.txt')