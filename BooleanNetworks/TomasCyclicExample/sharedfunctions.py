import numpy as np
import BooleanNetworks.PatternMatching.patternmatch as pm
import BooleanNetworks.PatternMatching.fileparsers as fp
import BooleanNetworks.PatternMatching.preprocess as pp
import BooleanNetworks.PatternMatching.walllabels as wl

def makeWallGraph(domains,outedges):
    # make list of walls in here too, as well as wall graph. I think it will be faster that way.
    walls=[]
    outdom=[]
    indom=[]
    for o,(n,d) in zip(outedges,enumerate(domains)):
        for i in o:
            c=domains[i]
            k=[abs(int(v-w)) for v,w in zip(d,c)].index(1)
            w=list(d)
            w[k]=w[k]-0.5 if d[k]>c[k] else w[k]+0.5
            walls.append(tuple(w))
            outdom.append(i)
            indom.append(n)
    walloutedges=[]
    for od in outdom:
        woe=[]
        nextdoms=outedges[od]
        for j in range(len(walls)):
            if indom[j]==od and outdom[j] in nextdoms:
                woe.append(j)
        walloutedges.append(tuple(woe))
    return walls, walloutedges

def checkDomainOutedges(domains,outedges):
    Domains=np.array(domains)
    noedges=[]
    for k,d in enumerate(Domains):
        diffs=np.abs(Domains-d)
        for j,r in enumerate(diffs):
            if np.abs(np.sum(r) -1.0)<0.1:
                if k not in outedges[j] and j not in outedges[k] and (k,j) not in noedges:
                    noedges.append((j,k))
    return noedges

def searchForPatterns(pymod='oneintermediatenode'):
    print "Preprocessing..."
    eval('import '+pymod)
    pymod.writeVars()
    pymod.writePatterns()
    domains=pymod.makeDomains()
    domainoutedges=pymod.makeDomainGraph(domains)
    walldomains,walloutedges=makeWallGraph(domains,domainoutedges)
    varsaffectedatwall=pymod.makeVarsAffected(walldomains)
    wallinds,walloutedges,walldomains,varsaffectedatwall,allwalllabels = pp.filterAll(walloutedges,walldomains,varsaffectedatwall)
    varnames=fp.parseVars()
    patternnames,patternmaxmin=fp.parsePatterns()
    patterns=pp.constructCyclicPatterns(varnames,patternnames,patternmaxmin)
    for pattern in patterns:
        print "\n"
        print '-'*25
        print "Pattern: {}".format(pattern)
        match=pm.matchCyclicPattern(pattern,wallinds,walloutedges,walldomains,varsaffectedatwall, allwalllabels,showfirstwall=0)
        print "Results: {}".format(match)
        print '-'*25
        # sys.stdout.flush()
