import sys,itertools
import walllabels as WL
import preprocess as pp
import fileparser as fp

# Need large example to test if dict version is better than 2 list version

def recursePattern_Dict(previouswall,currentwall,match,matches,patterns,pDict):
    if len(match) >= pDict['lenpattern'] and any([pDict['stop'] in labels[1] for labels in pDict['walllabels'][match[-2] * pDict['numwalls']+match[-1]]]):  
        matches.append(match)
        return matches
    else:
        ind=previouswall*pDict['numwalls']+currentwall
        for p,P in patterns:
            for nextwall,labels in pDict['walllabels'][ind]:
                if p in labels: # if we hit the next pattern element, reduce pattern by one
                    matches=recursePattern_Dict(currentwall,nextwall,match+[currentwall],matches,patterns[1:],pDict)
                if P in labels: # if we hit an intermediate node, keep the same pattern
                    matches=recursePattern_Dict(currentwall,nextwall,match+[currentwall],matches,patterns,pDict)
        return matches

def matchPattern_Dict(pattern,paramDict,cyclic=1,showfirstwall=0):
    '''
    This function finds paths in a directed graph that are consistent with a target pattern. The nodes
    of the directed graph are called walls, and each node is associated with a wall label (in walldomains)
    and a wall number (the index of the label in walldomains). The outgoing edges of a node with wall
    number w are stored in outedges at index w. Each element of outedges is a collection of wall numbers. 

    The pattern is a sequence of words from the alphabet ('u','d','m','M'), with each word containing no more
    than one 'm' or 'M'. The variable locations in walldomains will be transformed in a path-dependent manner into 
    words of the same type that have at most one 'm' or 'M'. There can be at most one 'm' 
    or 'M' at each wall because we assume that the input graph arises from a switching network where each 
    regulation event occurs at a unique threshold. The paths in the graph that have word labels that 
    match the pattern will be returned as sequences of wall numbers. Intermediate wall labels may be inserted 
    into the pattern as long as they do not have an 'm' or 'M' in the label, and are consistent with the next 
    word in the pattern. Example: 'uMdd' in a four dimensional system means that the first variable is 
    increasing (up), the second variable is at a maximum (Max), and the third and fourth variables are 
    decreasing (down). The character 'm' means a variable is at a minimum (min). If the words 'uMdd' then 'udmd'
    appear in a pattern, the intermediate node 'uddd' may be inserted between these two in a match.

    The inputs pattern and paramDict are produced by functions in the module preprocess and walllabels. 
    See the code for more information.

    pattern: list of uniform-length words from the alphabet ('u','d','m','M'); at most one 'm' or 'M' per string.
             If a cyclic path is desired, then the first and last words of pattern must be identical.
    paramDict keywords:
        numwalls: integer denoting the number of walls in the graph
        walllabels: a dictionary of lists of tuples keyed by first wall*numwalls + second wall. Each tuple contains
            as a first element the third wall and as a second element the list of wall labels associated with the
            triple (first wall, second wall, third wall).

    cyclic=1 means only cyclic paths are sought. cyclic=0 means acyclic paths are acceptable.

    showfirstwall=1 prints informative messages for the user for tracking the progress of the code on long, slow simulations.

    See functions beginning with "call" below for example calls of this function.

    '''
    # check for empty patterns
    if not pattern:
        return "None. Pattern is empty."
    # check if any word in pattern is not a wall label (it's pointless to search in that case)
    # first make flat list
    flatwalllabels = [elem for labels in paramDict['walllabels'].itervalues() for l in labels for elem in l[1]]
    if not set(pattern).issubset(flatwalllabels):
        return "None. No results found. Pattern contains an element that is not a wall label."
    # find all possible starting nodes for a matching path
    startwallpairs=getFirstAndNextWalls_Dict(pattern[0],paramDict['numwalls'],paramDict['walllabels'])
    firstwalls,nextwalls=zip(*startwallpairs)
    # return trivial length one patterns
    if len(pattern)==1:
        return firstwalls
    # pre-cache intermediate nodes that may exist in the wall graph
    intermediatenodes=[p.replace('m','d').replace('M','u')  if set(p).intersection(['m','M']) else '' for p in pattern[1:]] 
    patternParams = zip(pattern[1:],intermediatenodes)
    # add recursive function stopping criteria
    paramDict['stop'] = pattern[-1]
    paramDict['lenpattern'] = len(pattern)
    # find matches
    results=[]
    if showfirstwall:
        print "All first walls {}".format(firstwalls)
    for w,n in startwallpairs:
        if showfirstwall:
            print "First wall {}".format(w)
        # force print messages thus far
        sys.stdout.flush() 
        # seek match starting with w, n
        R = recursePattern_Dict(w,n,[w],[],patternParams,paramDict) 
        # pull out nonempty paths
        results.extend([tuple(l) for l in R if l])
    # record only unique paths
    results = list(set(results))
    if cyclic:
        # sort out acyclic paths, since walls may share a wall label
        results = [l for l in results if l[0]==l[-1]]
    return results or "None. No results found."

def callPatternMatchJSONWriteFile_Dict(basedir='',message='',cyclic=1):
    # basedir must contain the files output.json, patterns.txt, and equations.txt.
    # positive results saved to file; negative results not recorded
    if message:
        print "\n"
        print "-"*len(message)
        print message
        print "-"*len(message)
        print "\n"
    print "Preprocessing..."
    Patterns,parameterinds,paramDictlist=pp.preprocessJSON_Dict(basedir,cyclic)
    param=1
    f=open(basedir+'results.txt','w',0)
    for paramDict in paramDictlist: 
        print "\n"
        print "Morse set {} of {}".format(param,len(paramDictlist))
        print "Parameters={}".format(parameterinds[param-1])
        for pattern in Patterns:
            match=matchPattern_Dict(pattern,paramDict,cyclic=cyclic,showfirstwall=0)
            if 'None' not in match:
                f.write('\n'+"Parameters={}".format(parameterinds[param-1])+'\n')
                f.write("Pattern: {}".format(pattern)+'\n')
                f.write("Results: {}".format(match)+'\n')
        param+=1
    f.close()

def preprocess_dict(basedir,cyclic=1):
    # will be obsolete soon
    # read input files
    outedges,(walldomains,wallthresh),varnames,threshnames,(patternnames,patternmaxmin)=fp.parseAll(basedir+'outEdges.txt',basedir+'walls.txt',basedir+'variables.txt',basedir+'equations.txt',basedir+'patterns.txt')
    # put max/min patterns in terms of the alphabet u,m,M,d
    patterns=pp.translatePatterns(varnames,patternnames,patternmaxmin,cyclic=cyclic)
    # record which variable is affected at each wall
    varsaffectedatwall=pp.varsAtWalls(threshnames,walldomains,wallthresh,varnames)
    # make memory structure
    N, walllabelsdict = makeDictOfWallLabels(outedges,walldomains,varsaffectedatwall)
    paramDict={'walllabels':walllabelsdict,'numwalls':N}
    return patterns,paramDict

def preprocessJSON_Dict(basedir,cyclic=1):
    # will be obsolete soon
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
        newoutedgeslist.append(pp.filterOutEdgesJSON(wallinds,outedges))
    outedgeslist=newoutedgeslist
    # put max/min patterns in terms of the alphabet u,m,M,d
    patterns=pp.translatePatterns(varnames,patternnames,patternmaxmin,cyclic=cyclic)
    # record which variable is affected at each wall
    varsaffectedatwalllist=[]
    for (wd,wt) in zip(walldomainslist,wallthreshlist):
        varsaffectedatwalllist.append(pp.varsAtWalls(threshnames,wd,wt,varnames))
    # create wall labels
    paramDictlist=[]
    for (oe,wd,vw) in zip(outedgeslist,walldomainslist,varsaffectedatwalllist):
        n,wl=makeDictOfWallLabels(oe,wd,vw)
        paramDictlist.append({'walllabels':wl,'numwalls':n})
    return patterns,splitparameterinds,paramDictlist

def getFirstAndNextWalls_Dict(firstpattern,numwalls,walllabelsdict):
    # Given the first word in the pattern, find the nodes in the graph that have 
    # this pattern for some path. Our searches will start at each of these nodes, 
    # and proceed to the next nodes found in this algorithm.
    startwallpairs=[]
    for d in walllabelsdict.items():
        previouswall,currentwall = divmod(d[0],numwalls)
        for nextwall in d[1]:
            if firstpattern in nextwall[1]:
                startwallpairs.append((currentwall,nextwall[0]))
    return list(set(startwallpairs))

def makeDictOfWallLabels(outedges,walldomains,varsaffectedatwall):
    # Assumption: Walls must be numbered 0 to N-1
    # make inedges
    inedges=[tuple([j for j,o in enumerate(outedges) if node in o]) for node in range(len(outedges))]   
    # construct the wall label for every permissible triple (in-edge, wall, out-edge)
    walllabels=[]
    for k,(ie,oe) in enumerate(zip(inedges,outedges)):
        W=[]
        for i,o in itertools.product(ie,oe):
            # make wall labels for wall tuple (i,k,o)
            pds=WL.pathDependentStringConstruction(i,k,o,walldomains,outedges,varsaffectedatwall[k],inedges)
            # save tuple and list of wall labels
            W.append(((i,k,o),pds))
        walllabels.extend(W)
    # collapse in-edge and wall into one index to use as key in dict to access out-edge and list of wall labels associated to triple
    N=len(outedges)
    walllabelsdict={}
    for t,wl in walllabels:
        ind=t[0]*N+t[1]
        if ind in walllabelsdict.keys():
            walllabelsdict[ind].append((t[2],wl))
        else:
            walllabelsdict[ind]=[(t[2],wl)]
    # print walllabels
    # print '\n'
    # print walllabelsdict
    return N,walllabelsdict


