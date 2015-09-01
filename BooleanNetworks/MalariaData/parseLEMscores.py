import numpy as np
import pydot

from scipy.sparse.csgraph import connected_components

def parseFile(bound=0,fname='/Users/bcummins/ProjectData/malaria/wrair2015_pfalc_462tf_lem.allscores.tsv'):
    f=open(fname,'r')
    source=[]
    type_reg=[]
    target=[]
    lem_score=[]
    f.readline()
    for l in f.readlines():
        wordlist=l.split()
        if float(wordlist[3])>bound:
            source.append(wordlist[0])
            lem_score.append(float(wordlist[3]))
            two_words=wordlist[2].split('(')
            type_reg.append(two_words[0])
            target.append(two_words[1][:-1])
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
    # print components
    # print max(components)
    number_components=[components.count(k) for k in range(max(components)) if components.count(k)>1]
    return number_components, [k for k,c in enumerate(components) if components.count(c)>1]

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

def makeGraph(genes,outedges,regulation,name='graph_lastedge500.png'):
    graph = pydot.Dot(graph_type='digraph')
    for d in range(len(genes)):
        graph.add_node(pydot.Node(d))
    for i,(oe,reg) in enumerate(zip(outedges,regulation)):
        for o,r in zip(oe,reg):
            if r=='r':
                graph.add_edge(pydot.Edge(i,o,arrowhead='tee'))
            else:
                graph.add_edge(pydot.Edge(i,o))
    graph.write_png(name)

def generateResult(topscores=350,threshold=0.1,scorename='350',thresholdname='00',makegraph=1,saveme=1):
    print 'Parsing file...'
    source,target,type_reg,lem_score=parseFile(threshold)
    genes=chooseGenes(topscores,source,target)
    # print genes
    print 'Making outedges...'
    outedges,regulation,LEM_scores=makeOutedges(genes,source,target,type_reg,lem_score)
    # print outedges
    number_components,scc_gene_inds=strongConnectIndices(outedges)
    scc_genes=[genes[g] for g in scc_gene_inds]
    # print scc_genes
    print 'Pruning outedges...'
    outedges,regulation,LEM_scores=pruneOutedges(scc_gene_inds,outedges,regulation,LEM_scores)
    # flatscores=[l for ls in LEM_scores for l in ls]
    # if flatscores:
    #     print min(flatscores), max(flatscores)
    # print outedges
    if makegraph:
        print 'Making graph for {} nodes and {} edges....'.format(len(scc_genes),len([o for oe in outedges for o in oe]))
        makeGraph(scc_genes,outedges,regulation,name='graph_topscores{}_thresh{}.png'.format(scorename,thresholdname))
    if saveme:
        f=open('data_topscores{}_thresh{}.txt'.format(scorename,thresholdname),'w')
        f.write('{} top scores and threshold of {}'.format(topscores,threshold)+'\n')
        f.write('{} nodes and {} edges'.format(len(scc_genes),len([o for oe in outedges for o in oe]))+'\n')
        f.write('{} strongly connected component(s) with {} nodes in each'.format(len(number_components),number_components)+'\n')
        f.write(str(scc_genes)+'\n')
        f.write(str(outedges)+'\n')
        f.write(str(regulation)+'\n')
        f.write(str(LEM_scores))
        f.close()
    return number_components

f=open('datamaxnumnodes.txt','w')
g=open('datalenscc.txt','w')
for topscores in [450, 500, 550, 575, 600, 625, 650, 700, 750]:
    M=[]
    for k,threshold in enumerate([0.5,0.2,0.195,0.19,0.185,0.18,0.17,0.16,0.15,0.12,0.1]):
        print topscores, threshold
        number_components=generateResult(topscores,threshold,str(topscores),str(k).zfill(2),0,0)
        if threshold>0.1:
            f.write(str(max(number_components))+' & ')
            g.write(str(len(number_components))+' & ')
        else:
            f.write(str(max(number_components))+'\n')
            g.write(str(len(number_components))+'\n')
f.close()
g.close()







