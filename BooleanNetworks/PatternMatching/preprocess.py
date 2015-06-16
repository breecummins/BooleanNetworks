import walllabels as WL
import fileparsers as fp
from scipy.sparse.csgraph import connected_components
import numpy as np
import itertools

def preprocess(basedir,cyclic=1):
    # read input files
    outedges,(walldomains,wallthresh),varnames,threshnames,(patternnames,patternmaxmin)=fp.parseAll(basedir+'outEdges.txt',basedir+'walls.txt',basedir+'variables.txt',basedir+'equations.txt',basedir+'patterns.txt')
    # put max/min patterns in terms of the alphabet u,m,M,d
    patterns=constructPatterns(varnames,patternnames,patternmaxmin,cyclic=cyclic)
    # record which variable is affected at each wall
    varsaffectedatwall=varsAtWalls(threshnames,walldomains,wallthresh,varnames)
    # filter out walls not involved in cycles and create wall labels for the filtered walls
    origwallinds,outedges,walldomains,varsaffectedatwall,allwalllabels,inedges,triples,sortedwalllabels = filterAllTriples(outedges,walldomains,varsaffectedatwall)
    paramDict = {'allwalllabels':allwalllabels,'triples':triples,'sortedwalllabels':sortedwalllabels}
    return patterns,origwallinds,paramDict

def preprocessPatternGenerator(basedir,cyclic=1):
    # cyclic keyword is placeholder for the fact that this function produces only cyclic patterns
    # read input files
    outedges,(walldomains,wallthresh),varnames,threshnames,(patternstart,patternremainder)=fp.parseAllPatternGenerator(basedir+'outEdges.txt',basedir+'walls.txt',basedir+'variables.txt',basedir+'equations.txt',basedir+'patterngenerator.txt')
    # record which variable is affected at each wall
    varsaffectedatwall=varsAtWalls(threshnames,walldomains,wallthresh,varnames)
    # filter out walls not involved in cycles and create wall labels for the filtered walls
    origwallinds,outedges,walldomains,varsaffectedatwall,allwalllabels,inedges,triples,sortedwalllabels = filterAllTriples(outedges,walldomains,varsaffectedatwall)
    paramDict = {'allwalllabels':allwalllabels,'triples':triples,'sortedwalllabels':sortedwalllabels}
    return patternstart,patternremainder,origwallinds,varnames,paramDict

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
        newoutedgeslist.append(filterOutEdgesJSON(wallinds,outedges))
    outedgeslist=newoutedgeslist
    inedgeslist=[[tuple([j for j,o in enumerate(outedges) if node in o]) for node in range(len(outedges))] for outedges in outedgeslist]  
    # put max/min patterns in terms of the alphabet u,m,M,d
    patterns=constructPatterns(varnames,patternnames,patternmaxmin,cyclic=cyclic)
    # record which variable is affected at each wall
    varsaffectedatwalllist=[]
    for (wd,wt) in zip(walldomainslist,wallthreshlist):
        varsaffectedatwalllist.append(varsAtWalls(threshnames,wd,wt,varnames))
    # create wall labels
    allwalllabelslist=[]
    tripleslist=[]
    sortedwalllabelslist=[]
    for (oe,wd,vw,ie) in zip(outedgeslist,walldomainslist,varsaffectedatwalllist,inedgeslist):
        t,sa,a=WL.makeAllTriples(oe,wd,vw,ie)
        allwalllabelslist.append(a)
        sortedwalllabelslist.append(sa)
        tripleslist.append(t)
    paramDictlist=[]
    for (aw,tp,sw) in zip(allwalllabelslist,tripleslist,sortedwalllabelslist):
        paramDict = {'allwalllabels':aw,'triples':tp,'sortedwalllabels':sw}
        paramDictlist.append(paramDict)
    return patterns,wallindslist,splitparameterinds,paramDictlist

def constructPatterns(varnames,patternnames,patternmaxmin,cyclic=0):
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
        patterns=pp.constructPatterns(varnames,patternnames,patternmaxmin,cyclic=cyclic)
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

def filterOutEdgesJSON(wallinds,outedges):
    return [tuple([wallinds.index(j) for j in o]) for o in outedges]

def filterWallProperties(interiorinds,wallproperties):
    # strip filtered walls from associated wall properties
    return [[p for i,p in enumerate(wp) if i in interiorinds] for wp in wallproperties]

def filterAllTriples(outedges,walldomains,varsaffectedatwall):
    # get indices of walls in nontrivial strongly connected components of the wall graph
    origwallinds=strongConnectWallNumbers(outedges)
    # renumber the remaining walls and filter the wall properties
    outedges=filterOutEdges(origwallinds,outedges)
    inedges=[tuple([j for j,o in enumerate(outedges) if node in o]) for node in range(len(outedges))]  
    (walldomains,varsaffectedatwall)=filterWallProperties(origwallinds,(walldomains,varsaffectedatwall))
    # create all possible wall labels for the remaining walls
    triples,sortedwalllabels,allwalllabels=WL.makeAllTriples(outedges,walldomains,varsaffectedatwall,inedges)
    return origwallinds,outedges,walldomains,varsaffectedatwall,allwalllabels,inedges,triples,sortedwalllabels

if __name__=='__main__':
    out=preprocessJSON('')
    for o in out:
        print o