import walllabels as WL
import fileparsers as fp
from scipy.sparse.csgraph import connected_components
import numpy as np
import itertools

def preprocess(basedir):
    # read input files
    outedges,(walldomains,wallthresh),varnames,threshnames,(patternnames,patternmaxmin)=fp.parseAll(basedir+'outEdges.txt',basedir+'walls.txt',basedir+'variables.txt',basedir+'equations.txt',basedir+'patterns.txt')
    # put max/min patterns in terms of the alphabet u,m,M,d
    patterns=constructCyclicPatterns(varnames,patternnames,patternmaxmin)
    # record which variable is affected at each wall
    varsaffectedatwall=varsAtWalls(threshnames,walldomains,wallthresh,varnames)
    # filter out walls not involved in cycles and create wall labels for the filtered walls
    inds,outedges,walldomains,varsaffectedatwall,allwalllabels = filterAll(outedges,walldomains,varsaffectedatwall)
    return patterns,inds,outedges,walldomains,varsaffectedatwall,allwalllabels

def constructCyclicPatterns(varnames,patternnames,patternmaxmin):
    numvars=len(varnames)
    varinds=[[varnames.index(q) for q in p] for p in patternnames]
    patterns=[]
    for v,p in zip(varinds,patternmaxmin):
        P=len(p)
        missingvars=sorted(list(set(range(numvars)).difference(set(v))))
        if not missingvars:
            wordlist=[['0' for _ in range(numvars)] for _ in range(P)]
        else:
            wordlist=[]
            for c in itertools.combinations_with_replacement(['u','d'],len(missingvars)):
                wl = [[c[missingvars.index(k)] if k in missingvars else '0' for k in range(numvars)] for _ in range(P)]
                wordlist.extend(wl)
        for j in range(len(wordlist)/P):
            wl=wordlist[j*P:(j+1)*P]
            for i,(k,q) in zip(v,enumerate(p)):
                wl[k][i] = 'M' if q=='max' else 'm' 
            for k in range(len(wl)):
                for n in range(numvars):
                    if wl[k][n]=='0':
                        K=k
                        while wl[K][n] == '0':
                            K=(K-1)%P #the mod P means I'm assuming cyclicity
                        wl[k][n] = 'd' if wl[K][n] in ['M','d'] else 'u'
            if wl[0] != wl[-1]:
                wl+=[wl[0]]
            patterns.append([''.join(w)  for w in wl])
    return patterns

def varsAtWalls(threshnames,walldomains,wallthresh,varnames):
    varsaffectedatthresh=[-1]*len(threshnames)
    for t in threshnames:
        varsaffectedatthresh[varnames.index(t[0])]=tuple([varnames.index(u) for u in t[1]])
    varsaffectedatwall=[-1]*len(walldomains)
    for k,(j,w) in zip(wallthresh,enumerate(walldomains)):
        if k>-1 and w[k]-int(w[k])<0.25 and 0<w[k]<len(varsaffectedatthresh[k])+1:
            varsaffectedatwall[j]=varsaffectedatthresh[k][int(w[k]-1)]
    return varsaffectedatwall

def strongConnect(outedges):
    adjacencymatrix=np.zeros((len(outedges),len(outedges)))
    for i,o in enumerate(outedges):
        for j in o:
            adjacencymatrix[i,j]=1
    N,components=connected_components(adjacencymatrix,directed=True,connection="strong")
    return list(components)

def strongConnectWallNumbers(outedges):
    components=strongConnect(outedges)
    return [k for k,c in enumerate(components) if components.count(c)>1]

def filterOutEdges(wallinds,outedges):
    return [tuple([wallinds.index(j) for j in outedges[k] if j in wallinds]) for k in wallinds]

def filterWallProperties(interiorinds,wallproperties):
    # strip filtered walls from associated wall properties
    return [[p for i,p in enumerate(wp) if i in interiorinds] for wp in wallproperties]

def filterAll(outedges,walldomains,varsaffectedatwall):
    # get indices of walls in nontrivial strongly connected components of the wall graph
    wallinds=strongConnectWallNumbers(outedges)
    # renumber the remaining walls and filter the wall properties
    outedges=filterOutEdges(wallinds,outedges)
    (walldomains,varsaffectedatwall)=filterWallProperties(wallinds,(walldomains,varsaffectedatwall))
    # create all possible wall labels for the remaining walls
    allwalllabels=WL.makeAllWallLabels(outedges,walldomains,varsaffectedatwall)
    return wallinds,outedges,walldomains,varsaffectedatwall,allwalllabels
