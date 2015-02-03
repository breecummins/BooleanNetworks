import walllabels as WL
from scipy.sparse.csgraph import connected_components
import numpy as np

def preprocess(basedir):
    # read input files
    outedges,(walldomains,wallthresh),varnames,threshnames,(patternnames,patternmaxmin)=fp.parseAll(basedir+'outEdges.txt',basedir+'walls.txt',basedir+'variables.txt',basedir+'equations.txt',basedir+'patterns.txt')
    # put max/min patterns in terms of the alphabet u,m,M,d
    patterns=ppm.constructCyclicPatterns(varnames,patternnames,patternmaxmin)
    # record which variable is affected at each wall
    varsaffectedatwall=ppm.varsAtWalls(threshnames,walldomains,wallthresh,varnames)
    # filter out walls not involved in cycles and create wall labels for the filtered walls
    inds,outedges,walldomains,varsaffectedatwall,allwalllabels = ppm.filterAll(outedges,walldomains,varsaffectedatwall)
    return patterns,inds,outedges,walldomains,varsaffectedatwall,allwalllabels

def constructCyclicPatterns(varnames,patternnames,patternmaxmin):
    numvars=len(varnames)
    varinds=[[varnames.index(q) for q in p] for p in patternnames]
    patterns=[]
    for v,p in zip(varinds,patternmaxmin):
        P=len(p)
        wordlist=[['0' for _ in range(numvars)] for _ in range(P)]
        for i,(k,q) in zip(v,enumerate(p)):
            wordlist[k][i] = 'M' if q=='max' else 'm' 
        for k in range(P):
            for n in range(numvars):
                if wordlist[k][n]=='0':
                    K=k
                    while wordlist[K][n] == '0':
                        K=(K-1)%P #the mod P means I'm assuming cyclicity
                    wordlist[k][n] = 'd' if wordlist[K][n] in ['M','d'] else 'u'
        wordlist+=[wordlist[0]]
        patterns.append([''.join(w) for w in wordlist])
    return patterns

def varsAtWalls(threshnames,walldomains,wallthresh,varnames):
    varsaffectedatthresh=[-1]*len(threshnames)
    for t in threshnames:
        varsaffectedatthresh[varnames.index(t[0])]=tuple([varnames.index(u) for u in t[1]])
    varsaffectedatwall=[-1]*len(walldomains)
    for k,(j,w) in zip(wallthresh,enumerate(walldomains)): #CHECKME: Must handle boundaries
        if k>-1 and w[k]-int(w[k])<0.25 and 0<w[k]<len(varsaffectedatthresh[k])+1:
            varsaffectedatwall[j]=varsaffectedatthresh[k][int(w[k]-1)]
    return varsaffectedatwall

def strongConnect(outedges):
    adjacencymatrix=np.zeros((len(outedges),len(outedges)))
    for i,o in enumerate(outedges):
        for j in o:
            adjacencymatrix[i,j]=1
    N,components=connected_components(adjacencymatrix,connection="strong")
    return N,components

def strongConnectWallNumbers(outedges):
    N,components=strongConnect(outedges)
    wallinds=[]
    for k in range(N):
        inds=[i for i,c in enumerate(components) if c == k]
        if len(inds) > 1:
            wallinds.extend(inds)
    return sorted(wallinds)

def filterOutEdges(interiorinds,outedges):
    return [tuple([interiorinds.index(j) for j in outedges[k] if j in interiorinds]) for k in interiorinds]

def filterWallLabels(walllabels):
    return [k for k,w in enumerate(walllabels) if w]

def filterWallProperties(interiorinds,wallproperties):
    # strip filtered walls from associated wall properties
    return [[p for i,p in enumerate(wp) if i in interiorinds] for wp in wallproperties]

def filterAll(outedges,walldomains,varsaffectedatwall):
    # get indices of walls that participate in a strongly connected component of the wall graph
    wallinds=strongConnectWallNumbers(outedges)
    # renumber the remaining walls and filter the wall properties
    outedges=filterOutEdges(wallinds,outedges)
    (walldomains,varsaffectedatwall)=filterWallProperties(wallinds,(walldomains,varsaffectedatwall))
    # create all possible wall labels for the remaining walls
    allwalllabels=WL.makeAllWallLabels(outedges,walldomains,varsaffectedatwall)
    return wallinds,outedges,walldomains,varsaffectedatwall,allwalllabels


if __name__=='__main__':
    for p in constructCyclicPatterns("/Users/bcummins/ProjectData/DatabaseSimulations/5D_cycle_1/MGCC_14419/variables.txt"):
        print p 
