import sys,itertools
import walllabels as WL
import preprocess as pp

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
    startwallpairs=WL.getFirstAndNextWalls_Dict(pattern[0],paramDict['numwalls'],paramDict['walllabels'])
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

def recursePattern(firstwall,nextwall,match,matches,patterns,pDict):
    # THIS FUNCTION USES MEMORY INSTEAD OF CPU; allwalllabels and sortedwalllabels are different indexings
    # of the same information. Could use just one and do a sort at every recursive call instead.
    if len(match) >= pDict['lenpattern'] and pDict['stop'] in pDict['allwalllabels'][match[-1]]: 
        # print patterns
        # print match  
        matches.append(match)
        return matches
    else:
        for p,P in patterns:
            for k,t in enumerate(pDict['triples'][firstwall]):
                if t[1] == nextwall:
                    labels=pDict['sortedwalllabels'][firstwall][k]
                    # print labels
                    if p in labels: # if we hit the next pattern element, reduce pattern by one
                        matches=recursePattern(t[1],t[2],match+[t[1]],matches,patterns[1:],pDict)
                    if P in labels: # if we hit an intermediate node, keep the same pattern
                        matches=recursePattern(t[1],t[2],match+[t[1]],matches,patterns,pDict)
        return matches

def matchPattern(pattern,origwallinds,paramDict,cyclic=1,showfirstwall=0):
    '''
    This function finds paths in a directed graph that are consistent with a target pattern. The nodes
    of the directed graph are called walls, and each node is associated with a wall label (in walldomains)
    and a wall number (the index of the label in walldomains). The outgoing edges of a node with wall
    number w are stored in outedges at index w. Each element of outedges is a collection of wall numbers. 

    The pattern is a sequence of words from the alphabet ('u','d','m','M'), with each word containing EXACTLY
    one 'm' or 'M'. The variable locations in walldomains will be transformed in a path-dependent manner into 
    words of the same type that have AT MOST one 'm' or 'M'. There can be at most one 'm' 
    or 'M' at each wall because we assume that the input graph arises from a switching network where each 
    regulation event occurs at a unique threshold. The paths in the graph that have word labels that 
    match the pattern will be returned as sequences of wall numbers. Intermediate wall labels may be inserted 
    into the pattern as long as they do not have an 'm' or 'M' in the label, and are consistent with the next 
    word in the pattern. Example: 'uMdd' in a four dimensional system means that the first variable is 
    increasing (up), the second variable is at a maximum (Max), and the third and fourth variables are 
    decreasing (down). The character 'm' means a variable is at a minimum (min). If the words 'uMdd' then 'udmd'
    appear in a pattern, the intermediate node 'uddd' may be inserted between these two in a match.

    The following variables are produced by functions in the module preprocess in. See the code for more information.

    pattern: list of uniform-length words from the alphabet ('u','d','m','M'); exactly one 'm' or 'M' REQUIRED per string
    origwallinds: list of integers denoting the original wall number in the full wall graph. In the algorithm, walls are 
        referred to by the index of origwallinds, not the value. 
    paramDict keywords:
        triples: list of tuples (previouswall,currentwall,nextwall) allowable from graph
        allwalllabels: list of lists of uniform-length words from the alphabet ('u','d','m','M') with at most one of 
            ['m','M'] in each word describing the possible wall labels at currentwall
        sortedwalllabels: allwalllabels re-indexed according to previouswall

    cyclic=1 means only cyclic paths are sought. cyclic=0 means acyclic paths are acceptable.

    showfirstwall=1 prints informative messages for the user for tracking the progress of the code on long, slow simulations.

    See functions beginning with "call" below for example calls of this function.

    '''
    # print pattern
    # check for empty patterns
    if not pattern:
        return "None. Pattern is empty."
    # check if any word in pattern is not a wall label (it's pointless to search in that case)
    awl = [a for l in paramDict['allwalllabels'] for a in l]
    if not set(pattern).issubset(awl):
        return "None. No results found. Pattern contains an element that is not a wall label."
    # find all possible starting nodes for a matching path
    startwallpairs=WL.getFirstAndNextWalls(pattern[0],paramDict['triples'],paramDict['sortedwalllabels'])
    firstwalls,nextwalls=zip(*startwallpairs)
    # return trivial length one patterns
    if len(pattern)==1:
        return [ (origwallinds.index(w),) for w in firstwalls ] or "None. No results found."
    # pre-cache intermediate nodes that may exist in the wall graph
    intermediatenodes=[p.replace('m','d').replace('M','u')  if set(p).intersection(['m','M']) else '' for p in pattern[1:]] 
    patternParams = zip(pattern[1:],intermediatenodes)
    paramDict['stop'] = pattern[-1]
    paramDict['lenpattern'] = len(pattern)
    # find matches
    results=[]
    if showfirstwall:
        print "All first walls {}".format([origwallinds[w] for w in firstwalls])
    for w,n in startwallpairs:
        if showfirstwall:
            print "First wall {}".format(origwallinds[w])
        sys.stdout.flush() # force print messages thus far
        R = recursePattern(w,n,[w],[],patternParams,paramDict) # seek match starting with w, n
        results.extend([tuple(l) for l in R if l]) # pull out nonempty paths
    # now translate paths into original wall numbers; paths not guaranteed unique so use set()
    results = list(set(results))
    if cyclic:
        # sort out acyclic paths, since walls may share a wall label
        results = [l for l in results if l[0]==l[-1]]
    # if cyclic:
    #     # sorting out acyclic paths, since walls may share a wall label
    #     results = [tuple([origwallinds[r] for r in l]) for l in list(set(results)) if l[0]==l[-1]]
    # else:
    #     results = [tuple([origwallinds[r] for r in l]) for l in list(set(results))]        
    return results or "None. No results found."

def callPatternMatch(basedir='',message='',cyclic=1):
    # basedir must contain the files outEdges.txt, walls.txt, patterns.txt, variables.txt, and 
    # equations.txt.
    # output printed to screen
    if message:
        print "\n"
        print "-"*len(message)
        print message
        print "-"*len(message)
        print "\n"
    print "Preprocessing..."
    Patterns,origwallinds,paramDict=pp.preprocess(basedir,cyclic) 
    for pattern in Patterns:
        print "\n"
        print '-'*25
        print "Pattern: {}".format(pattern)
        match=matchPattern(pattern,origwallinds,paramDict,cyclic=cyclic,showfirstwall=1)
        print "Results: {}".format(match)
        print '-'*25

def callPatternMatchJSON(basedir='',message='',cyclic=1):
    # basedir must contain the files output.json, patterns.txt, and equations.txt.
    # output printed to screen
    if message:
        print "\n"
        print "-"*len(message)
        print message
        print "-"*len(message)
        print "\n"
    print "Preprocessing..."
    Patterns,origwallindslist,parameterinds,paramDictlist=pp.preprocessJSON(basedir,cyclic)
    param=1
    for (origwallinds,paramDict) in zip(origwallindslist,paramDictlist): 
        print "\n"
        print '-'*50
        print "Morse set {} of {}".format(param,len(origwallindslist))
        print "Parameters={}".format(parameterinds[param-1])
        print '-'*50
        param+=1
        for pattern in Patterns:
            print "\n"
            print '-'*25
            print "Pattern: {}".format(pattern)
            match=matchPattern(pattern,origwallinds,paramDict,cyclic=cyclic,showfirstwall=1)
            print "Results: {}".format(match)
            print '-'*25

def callPatternMatchJSONWriteFile(basedir='',message='',cyclic=1):
    # basedir must contain the files output.json, patterns.txt, and equations.txt.
    # positive results saved to file; negative results not recorded
    if message:
        print "\n"
        print "-"*len(message)
        print message
        print "-"*len(message)
        print "\n"
    print "Preprocessing..."
    Patterns,origwallindslist,parameterinds,paramDictlist=pp.preprocessJSON(basedir,cyclic)
    param=1
    f=open(basedir+'results.txt','w',0)
    for (origwallinds,paramDict) in zip(origwallindslist,paramDictlist): 
        print "\n"
        print "Morse set {} of {}".format(param,len(origwallindslist))
        print "Parameters={}".format(parameterinds[param-1])
        for pattern in Patterns:
            match=matchPattern(pattern,origwallinds,paramDict,cyclic=cyclic,showfirstwall=0)
            if 'None' not in match:
                f.write('\n'+"Parameters={}".format(parameterinds[param-1])+'\n')
                f.write("Pattern: {}".format(pattern)+'\n')
                f.write("Results: {}".format(match)+'\n')
        param+=1
    f.close()

def callPatternMatchWithPatternGeneratorWriteFile(patternstart,patternremainder,basedir='',message='',cyclic=1):
    # basedir must contain the files outEdges.txt, walls.txt, variables.txt, patterngenerator.txt,
    # and equations.txt.
    # use when patterns.txt would take too much memory
    # positive results saved to file; negative results not recorded
    if message:
        print "\n"
        print "-"*len(message)
        print message
        print "-"*len(message)
        print "\n"
    print "Preprocessing..."
    patternstart,patternremainder,origwallinds,varnames,paramDict=pp.preprocessPatternGenerator(basedir) 
    f=open(basedir+'results.txt','w',0)
    for r in itertools.permutations(patternremainder):
        patterns=pp.constructPatternGenerator(patternstart+list(r),varnames)
        for pattern in patterns:
            match=matchPattern(pattern,origwallinds,paramDict,cyclic=cyclic,showfirstwall=0)
            if 'None' not in match:
                f.write('\n'+"Parameters={}".format(parameterinds[param-1])+'\n')
                f.write("Pattern: {}".format(pattern)+'\n')
                f.write("Results: {}".format(match)+'\n')
    f.close()

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
