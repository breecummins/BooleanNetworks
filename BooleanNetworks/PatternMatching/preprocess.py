import walllabels as WL
import fileparsers as fp
from scipy.sparse.csgraph import connected_components
import numpy as np
import itertools

def preprocess(basedir,cyclic=1):
    # read input files
    outedges,(walldomains,wallthresh),varnames,threshnames,(patternnames,patternmaxmin)=fp.parseAll(basedir+'outEdges.txt',basedir+'walls.txt',basedir+'variables.txt',basedir+'equations.txt',basedir+'patterns.txt')
    # put max/min patterns in terms of the alphabet u,m,M,d
    patterns=translatePatterns(varnames,patternnames,patternmaxmin,cyclic=cyclic)
    # record which variable is affected at each wall
    varsaffectedatwall=varsAtWalls(threshnames,walldomains,wallthresh,varnames)
    # make wall labels
    paramDict = WL.makeAllTriples(outedges,walldomains,varsaffectedatwall)
    return patterns,paramDict

def preprocessPatternGenerator(basedir,cyclic=1):
    # cyclic keyword is placeholder for the fact that this function produces only cyclic patterns
    # read input files
    outedges,(walldomains,wallthresh),varnames,threshnames,(patternstart,patternremainder)=fp.parseAllPatternGenerator(basedir+'outEdges.txt',basedir+'walls.txt',basedir+'variables.txt',basedir+'equations.txt',basedir+'patterngenerator.txt')
    # record which variable is affected at each wall
    varsaffectedatwall=varsAtWalls(threshnames,walldomains,wallthresh,varnames)
    # make wall labels
    paramDict = WL.makeAllTriples(outedges,walldomains,varsaffectedatwall)
    return patternstart,patternremainder,varnames,paramDict

def preprocessJSON(basedir,cyclic=1):
    # read input files
    varnames,wallindslist,outedgeslist,walldomainslist,wallthreshlist,parameterinds=fp.parseJSON(basedir+'output.json')
    threshnames=fp.parseEqns(basedir+'equations.txt')
    patternnames, patternmaxmin=fp.parsePatterns(basedir+'patterns.txt')
    # split according to Morse sets
    Morseoutedges=[]
    Morsewallinds=[]
    Morsedomains=[]
    Morsethresh=[]
    splitparameterinds=[]
    for oe,wi,wd,wt,pi in zip(outedgeslist,wallindslist,walldomainslist,wallthreshlist,parameterinds):
        if oe not in Morseoutedges:
            Morseoutedges.append(oe)
            Morsewallinds.append(wi)
            Morsedomains.append(wd)
            Morsethresh.append(wt)
            splitparameterinds.append([pi])
        else:
            splitparameterinds[Morseoutedges.index(oe)].append(pi)
    outedgeslist=Morseoutedges
    wallindslist=Morsewallinds
    walldomainslist=Morsedomains
    wallthreshlist=Morsethresh
    # relabel wall numbers in outedges
    newoutedgeslist=[]
    for (wallinds,outedges) in zip(wallindslist,outedgeslist):
        newoutedgeslist.append([tuple([wallinds.index(j) for j in o]) for o in outedges])
    outedgeslist=newoutedgeslist
    # put max/min patterns in terms of the alphabet u,m,M,d
    patterns=translatePatterns(varnames,patternnames,patternmaxmin,cyclic=cyclic)
    # record which variable is affected at each wall
    varsaffectedatwalllist=[]
    for (wd,wt) in zip(walldomainslist,wallthreshlist):
        varsaffectedatwalllist.append(varsAtWalls(threshnames,wd,wt,varnames))
    # create wall labels
    paramDictlist=[]
    for (oe,wd,vw) in zip(outedgeslist,walldomainslist,varsaffectedatwalllist):
        paramDictlist.append(WL.makeAllTriples(oe,wd,vw))
    return patterns,splitparameterinds,paramDictlist

def preprocess_JSON_Shaun_format(basedir,cyclic=1):
    # read input files; basedir should have dsgrn_output.json and patterns.txt
    varnames,threshnames,domgraph,cells=fp.parseNewJSONFormat(basedir+'dsgrn_output.json')
    patternnames,patternmaxmin=fp.parsePatterns(basedir+'patterns.txt')
    # put max/min patterns in terms of the alphabet u,m,M,d
    patterns=translatePatterns(varnames,patternnames,patternmaxmin,cyclic=cyclic)
    # translate domain graph into wall graph
    outedges,wallthresh,walldomains=makeWallGraphFromDomainGraph(domgraph,cells)    
    # record which variable is affected at each wall
    varsaffectedatwall=varsAtWalls(zip(varnames,threshnames),walldomains,wallthresh,varnames)
    # make wall labels
    paramDict = WL.makeAllTriples(outedges,walldomains,varsaffectedatwall)
    return patterns, paramDict

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
        # if the pattern meets the criterion, proceed with transalation
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

def constructPatternGenerator(sequence,varnames,cyclic=1):
    # code currently only works for cyclic=1
    # check that there is a max between each max/min pair (at least for 2 pairs)
    for v in varnames:
        m=sequence.count(v+' min')
        if m !=sequence.count(v+' max'):
            print 'No cyclic pattern possible. Check that number of maxima and minima match for every variable.'
            sequence=[]
            break
        elif sequence.count(v+' min')==2:
            i=sequence.index(v+' min')
            k=sequence[i+1:].index(v+' min')
            try:
                j=sequence[i+1:].index(v+' max')
                if j<k:
                    pass                
                else:
                    sequence=[]
                    break
            except:
                sequence=[]
                break
        elif sequence.count(v+'min')>2:
            print 'WARNING: More than 2 max/min pairs for one variable. Spurious patterns may be created.'
    if sequence:
        patternnames=[[s.split()[::2][0] for s in sequence]]
        patternmaxmin=[[s.split()[1::2][0] for s in sequence]]
        patterns=pp.translatePatterns(varnames,patternnames,patternmaxmin,cyclic=cyclic)
    else:
        patterns=[]
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

def makeCombinatorialPatternsFromIntermediateNodes(pattern,flatwalllabels):
    intermediatenodes=[p.replace('m','d').replace('M','u')  if set(p).intersection(['m','M']) else '' for p in pattern[1:]]
    counts= [flatwalllabels.count(i) for i in intermediatenodes] 
    intermediatenodeslist = [[[i]*n for n in range(c+1)] for i,c in zip(intermediatenodes,counts)]
    productlist=[]
    for k in range(len(pattern)-1):
        productlist.append([[pattern[k]]])
        productlist.append(intermediatenodeslist[k])
    productlist.append([[pattern[-1]]])
    productlist=[p if p else [[]] for p in productlist]
    patterngenerator=itertools.product(*productlist)
    return patterngenerator
        
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
        if sum(location) != 1:
            raise RunTimeError("The domain graph has an edge between nonadjacent domains. Aborting.")
        wallthresh.append(location.index(True))
        walldomains.append(tuple([sum(c0[k]+c1[k])/4.0 for k in range(n)])) 
    return outedges,wallthresh,walldomains


if __name__=='__main__':
    print makeWallGraphFromDomainGraph([[1],[2],[5,3],[4],[5],[0]])