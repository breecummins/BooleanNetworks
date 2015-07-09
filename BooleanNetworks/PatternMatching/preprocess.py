import walllabels as wl
import fileparsers as fp
import itertools

def preprocess(fname='dsgrn_output.json',pname='patterns.txt',cyclic=1):
    # read input files; basedir should have dsgrn_output.json and patterns.txt
    varnames,threshnames,domgraph,cells=fp.parseJSONFormat(fname)
    patternnames,patternmaxmin=fp.parsePatterns(pname)
    # put max/min patterns in terms of the alphabet u,m,M,d
    patterns=translatePatterns(varnames,patternnames,patternmaxmin,cyclic=cyclic)
    # translate domain graph into wall graph
    outedges,wallthresh,walldomains=makeWallGraphFromDomainGraph(domgraph,cells)    
    # record which variable is affected at each wall
    varsaffectedatwall=varsAtWalls(threshnames,walldomains,wallthresh,varnames)
    # make wall labels
    wallinfo = wl.makeWallInfo(outedges,walldomains,varsaffectedatwall)
    return patterns, wallinfo

def translatePatterns(varnames,patternnames,patternmaxmin,cyclic=0):
    numvars=len(varnames)
    varinds=[[varnames.index(q) for q in p] for p in patternnames]
    patterns=[]
    # loop over each provided pattern
    for pvars,extrema in zip(varinds,patternmaxmin):
        P = len(pvars)
        # record locations of extrema
        split_pattern=[]
        for k in range(numvars):
            varstring=[]
            for j in range(P):
                varstring.append('0' if k != pvars[j] else 'M' if extrema[j]=='max' else 'm')
            split_pattern.append(varstring)
        # make sure the pattern makes physical sense (no two identical extrema in a row)
        good_pattern=1
        for sp in split_pattern:
            seq = filter(None,[sp[k] if sp[k] in ['m','M'] else None for k in range(P)])
            if set(seq[::2])==set(['m','M']) or set(seq[1::2])==set(['m','M']):
                print "Pattern {} is not consistent; not including in search. Every variable must alternate maxima and minima.".format(zip(patternnames,patternmaxmin))
                good_pattern=0
        # if the pattern meets the criterion, proceed with translation
        # first build a set of template patterns if there are missing variables in the pattern (these could either be 'u' or 'd')
        if good_pattern:
            missingvars=sorted(list(set(range(numvars)).difference(set(pvars))))
            if missingvars:
                split_patterns=[]
                for c in itertools.combinations_with_replacement(['u','d'],len(missingvars)):
                    spc = split_pattern[:]
                    for k in range(numvars):
                        if k in missingvars:
                            spc[k]=[c[missingvars.index(k)]]*P 
                    split_patterns.append(spc)
            else:
                split_patterns=[split_pattern]
            # for each pattern, fill in the remaining blanks based on the location of the extrema
            for pat in split_patterns:
                for v in range(len(pat)):
                    for k in range(P):
                        if pat[v][k]=='0':
                            K=k
                            while pat[v][K]=='0' and K>0:
                                K-=1
                            J=k
                            while pat[v][J]=='0' and J<P-1:
                                J+=1
                            pat[v][k] = 'd' if pat[v][K] in ['M','d'] or pat[v][J] in ['m','d'] else 'u'
                pattern = [''.join([p[k] for p in pat]) for k in range(P)]
                # if a cyclic pattern is desired, make sure first and last elements are the same
                if cyclic and pattern[0] != pattern[-1]: 
                    pattern.append(pattern[0])
                patterns.append(pattern)
    return patterns
 
def varsAtWalls(threshnames,walldomains,wallthresh,varnames):
    varsaffectedatthresh=[]
    for t in threshnames:
        varsaffectedatthresh.append(tuple([varnames.index(u) for u in t]))
    varsaffectedatwall=[-1]*len(walldomains)
    for k,(j,w) in zip(wallthresh,enumerate(walldomains)):
        if k>-1 and w[k]-int(w[k])<0.25 and 0<w[k]<len(varsaffectedatthresh[k])+1:
            varsaffectedatwall[j]=varsaffectedatthresh[k][int(w[k]-1)]
    return varsaffectedatwall

def makeWallGraphFromDomainGraph(domgraph,cells):
    domedges=[(k,d) for k,e in enumerate(domgraph) for d in e]
    wallgraph=[(k,j) for k,edge1 in enumerate(domedges) for j,edge2 in enumerate(domedges) if edge1[1]==edge2[0]]
    outedges=[[] for _ in range(len(domedges))]
    for e in wallgraph:
        outedges[e[0]].append(e[1])
    outedges=[tuple(o) for o in outedges]
    wallthresh=[]
    walldomains=[]
    for de in domedges:
        c0=cells[de[0]]
        c1=cells[de[1]]
        n=len(c0)
        location=[False if c0[k]==c1[k] else True for k in range(n)]
        if sum(location) > 1:
            raise RunTimeError("The domain graph has an edge between nonadjacent domains. Aborting.")
        elif sum(location)==0:
            raise RunTimeError("The domain graph has a self-loop. Aborting.")
        else:
            wallthresh.append(location.index(True))
            walldomains.append(tuple([sum(c0[k]+c1[k])/4.0 for k in range(n)])) 
    return outedges,wallthresh,walldomains

