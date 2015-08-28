# import numpy as np
import pydot

f=open('/Users/bcummins/ProjectData/malaria/wrair2015_pfalc_462tf_lem.allscores.tsv','r')
source=[]
type_reg=[]
target=[]
lem_score=[]
f.readline()
M=500
m=0
for l in f.readlines():
    if m==M:
        break
    wordlist=l.split()
    source.append(wordlist[0])
    lem_score.append(float(wordlist[3]))
    two_words=wordlist[2].split('(')
    type_reg.append(two_words[0])
    target.append(two_words[1][:-1])
    m+=1
f.close()

genes=list(set(source).intersection(target))

short_source=[]
short_target=[]
short_typreg=[]
for src,typ,tar in zip(source,type_reg,target):
    if src in genes and tar in genes:
        short_source.append(src)
        short_target.append(tar)
        short_typreg.append(typ)

outedges=[]
regulation=[]
for g in genes:
    oe=[]
    reg=[]
    for s,t,tr in zip(short_source,short_target,short_typreg):
        if s==g:
            oe.append(genes.index(t))
            reg.append(tr)
    outedges.append(tuple(oe))
    regulation.append(tuple(reg))

print len(genes)
print sum([len(oe) for oe in outedges])
print sorted(list(set([o for oe in outedges for o in oe])))
print len(set([o for oe in outedges for o in oe]))
print outedges
print genes[91],genes[148]
print regulation[91][outedges[91].index(148)]
print regulation[148][outedges[148].index(91)]


# graph = pydot.Dot(graph_type='digraph')
# for d in range(len(genes)):
#     graph.add_node(pydot.Node(d))
# for i,oe in enumerate(outedges):
#     for o in oe:
#         graph.add_edge(pydot.Edge(i,o))
# graph.write_png('graph_M500.png')
