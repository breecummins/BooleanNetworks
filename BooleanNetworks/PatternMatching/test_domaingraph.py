from subprocess import call
import numpy as np
import fileparsers as fp
import preprocess as pp

def testgraph(domains,edges):
    for k,(c,d) in enumerate(zip(domains,edges)):
        for i in range(n):
            diffs=[]
            for e in d:
                c2=domains[e]
                diffs.append(np.sign(np.mean(c[i]) - np.mean(c2[i])))
            if set([-1,1]).issubset(diffs):
                print k,c
                for e in d:
                    print e,domains[e]

def testwallgraph(domains,edges):
    for k,(c,d) in enumerate(zip(domains,edges)):
        for i in range(n):
            diffs=[]
            for e in d:
                c2=domains[e]
                diffs.append(np.sign(c[i] - c2[i]))
            if set([-1,1]).issubset(diffs):
                print k,c
                for e in d:
                    print e,domains[e]

specfile="networks/5D_Malaria_20hr.txt"
parameter=116014
morseset=0

call(["dsgrn network {} analyze morseset {} {} >dsgrn_output.json".format(specfile,morseset,parameter)],shell=True)
varnames,threshnames,domgraph,cells=fp.parseJSONFormat('dsgrn_output.json')
n=len(cells[0])

# testgraph(cells,domgraph)

outedges,wallthresh,walldomains=pp.makeWallGraphFromDomainGraph(domgraph,cells) 

testwallgraph(walldomains,outedges)  


