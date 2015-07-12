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
    patterninds=[[varnames.index(q) for q in p] for p in patternnames]
    patterns=[]
    # loop over each provided pattern
    for inds,extrema in zip(patterninds,patternmaxmin):
        length_pattern = len(inds)
        # record locations of extrema for each variable
        variable_extrema=[['0' if k != i else 'M' if e=='max' else 'm' for i,e in zip(inds,extrema)] for k in range(numvars)]
        # make sure the pattern makes physical sense (no two identical extrema in a row)
        if isGoodPattern(variable_extrema,inds,extrema):
            # build a set of template patterns if there are missing variables in the pattern (these could either be 'u' or 'd')
            templates=makeTemplates(numvars,inds,variable_extrema,length_pattern)
            # for each template, fill in the remaining blanks based on the location of the extrema, and knit the variable sequences into a pattern
            for template in templates:
                pattern=makePattern(template,length_pattern,cyclic)
                patterns.append(pattern)
    return patterns

def isGoodPattern(variable_extrema,inds,extrema):
    for varext in variable_extrema:
        filt_varext = filter(None,[v if v in ['m','M'] else None for v in varext])
        if set(filt_varext[::2])==set(['m','M']) or set(filt_varext[1::2])==set(['m','M']):
            print "Pattern {} is not consistent. Every variable must alternate maxima and minima. Removing from search.".format(zip(inds,extrema))
            return False
    return True

def makeTemplates(numvars,inds,variable_extrema,length_pattern):
    missingvars=sorted(list(set(range(numvars)).difference(set(inds))))
    if missingvars:
        templates=[]
        for c in itertools.combinations_with_replacement(['u','d'],len(missingvars)):
            new_template=[ [c[missingvars.index(k)]]*length_pattern if k in missingvars else variable_extrema[k] for k in range(numvars)]
            templates.append(new_template)
    else:
        templates=[variable_extrema]
    return templates

def makePattern(template,length_pattern,cyclic):
    # use locations of extrema to fill in blanks; for example, 'M00m0' --> 'Mddmu', by inspection of extrema, where 'Mddmu' = max down down min up
    for i,t in enumerate(template):
        for j in range(length_pattern):
            if t[j]=='0':
                J,K=j,j
                while t[K]=='0' and K>0:
                    K-=1
                while t[J]=='0' and J<length_pattern-1:
                    J+=1
                t[j] = 'd' if t[K] in ['M','d'] or t[J] in ['m','d'] else 'u'
        template[i]=t
    # knit the individual variable sequences into the words of the pattern
    # for example, ['uuMd','dmuu','Mddm'] --> ['udM','umd','Mud','dum']
    pattern = [''.join([t[k] for t in template]) for k in range(length_pattern)]
    # if a cyclic pattern is desired, make sure first and last elements are the same
    if cyclic and pattern[0] != pattern[-1]: 
        pattern.append(pattern[0])
    return pattern
 
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
        location=[True if c0[k]!=c1[k] else False for k in range(n)]
        if sum(location) > 1:
            raise RunTimeError("The domain graph has an edge between nonadjacent domains. Aborting.")
        elif sum(location)==0:
            raise RunTimeError("The domain graph has a self-loop. Aborting.")
        else:
            wallthresh.append(location.index(True))
            walldomains.append(tuple([sum(c0[k]+c1[k])/4.0 for k in range(n)])) 
    return outedges,wallthresh,walldomains