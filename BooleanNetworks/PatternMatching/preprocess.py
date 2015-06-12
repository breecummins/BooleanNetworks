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
    inds,outedges,walldomains,varsaffectedatwall,allwalllabels,inedges,triples,sortedwalllabels = filterAllTriples(outedges,walldomains,varsaffectedatwall)
    paramDict = {'walldomains':walldomains,'outedges':outedges,'varsaffectedatwall':varsaffectedatwall,'allwalllabels':allwalllabels,'inedges':inedges,'triples':triples,'sortedwalllabels':sortedwalllabels}
    return patterns,inds,paramDict

def preprocessPatternGenerator(basedir):
    # read input files
    outedges,(walldomains,wallthresh),varnames,threshnames,(patternstart,patternremainder)=fp.parseAllPatternGenerator(basedir+'outEdges.txt',basedir+'walls.txt',basedir+'variables.txt',basedir+'equations.txt',basedir+'patterngenerator.txt')
    # record which variable is affected at each wall
    varsaffectedatwall=varsAtWalls(threshnames,walldomains,wallthresh,varnames)
    # filter out walls not involved in cycles and create wall labels for the filtered walls
    inds,outedges,walldomains,varsaffectedatwall,allwalllabels,inedges,triples,sortedwalllabels = filterAllTriples(outedges,walldomains,varsaffectedatwall)
    paramDict = {'walldomains':walldomains,'outedges':outedges,'varsaffectedatwall':varsaffectedatwall,'allwalllabels':allwalllabels,'inedges':inedges,'triples':triples,'sortedwalllabels':sortedwalllabels}
    return patternstart,patternremainder,inds,varnames,paramDict

def preprocessJSON(basedir):
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
    patterns=constructCyclicPatterns(varnames,patternnames,patternmaxmin)
    # record which variable is affected at each wall
    varsaffectedatwalllist=[]
    for (wd,wt) in zip(walldomainslist,wallthreshlist):
        varsaffectedatwalllist.append(varsAtWalls(threshnames,wd,wt,varnames))
    # create wall labels
    allwalllabelslist=[]
    tripleslist=[]
    for (oe,wd,vw,ie) in zip(outedgeslist,walldomainslist,varsaffectedatwalllist,inedgeslist):
        t,sa,a=WL.makeAllTriples(oe,wd,vw,ie)
        allwalllabelslist.append(a)
        sortedwalllabelslist.append(sa)
        tripleslist.append(t)
    paramDictlist=[]
    for (oe,wd,wv,ie,aw,tp,sw) in zip(outedgeslist,walldomainslist,varsaffectedatwalllist,inedgeslist,allwalllabelslist,tripleslist,sortedwalllabelslist):
        paramDict = {'walldomains':wd,'outedges':oe,'varsaffectedatwall':wv,'allwalllabels':aw,'inedges':ie,'triples':tp,'sortedwalllabels':sw}
        paramDictlist.append(paramDict)
    return patterns,wallindslist,splitparameterinds,paramDictlist

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

def constructPatternGenerator(sequence,varnames):
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
        patterns=pp.constructCyclicPatterns(varnames,patternnames,patternmaxmin)
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

def filterAll(outedges,walldomains,varsaffectedatwall):
    # get indices of walls in nontrivial strongly connected components of the wall graph
    wallinds=strongConnectWallNumbers(outedges)
    # renumber the remaining walls and filter the wall properties
    outedges=filterOutEdges(wallinds,outedges)
    inedges=[tuple([j for j,o in enumerate(outedges) if node in o]) for node in range(len(outedges))]  
    (walldomains,varsaffectedatwall)=filterWallProperties(wallinds,(walldomains,varsaffectedatwall))
    # create all possible wall labels for the remaining walls
    allwalllabels=WL.makeAllTriples(outedges,walldomains,varsaffectedatwall,inedges)[2]
    return wallinds,outedges,walldomains,varsaffectedatwall,allwalllabels,inedges

def filterAllTriples(outedges,walldomains,varsaffectedatwall):
    # get indices of walls in nontrivial strongly connected components of the wall graph
    wallinds=strongConnectWallNumbers(outedges)
    # renumber the remaining walls and filter the wall properties
    outedges=filterOutEdges(wallinds,outedges)
    inedges=[tuple([j for j,o in enumerate(outedges) if node in o]) for node in range(len(outedges))]  
    (walldomains,varsaffectedatwall)=filterWallProperties(wallinds,(walldomains,varsaffectedatwall))
    # create all possible wall labels for the remaining walls
    triples,sortedwalllabels,allwalllabels=WL.makeAllTriples(outedges,walldomains,varsaffectedatwall,inedges)
    return wallinds,outedges,walldomains,varsaffectedatwall,allwalllabels,inedges,triples,sortedwalllabels

if __name__=='__main__':
    out=preprocessJSON('')
    for o in out:
        print o