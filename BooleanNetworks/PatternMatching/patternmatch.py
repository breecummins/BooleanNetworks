def repeatingLoop(match):
    N=len(match)
    if len(set(match)) == N:
        return False
    else:
        for n in range(1,N/2+1):
            if match[N-n:N] == match[N-2*n:N-n]:
                return True
        return False

def recursePattern(startnode,match,matches,patterns,pDict):
    # optimized
    if len(match) >= pDict['lenpattern'] and pDict['walllabels'][match[-1]] == pDict['stop']: # the first condition requires all walls to be present in the pattern. A way to ensure this is to have only extrema in the pattern - i.e. every p in pattern has exactly one 'm' or 'M'. This is why this condition exists in the input sanity check.
        matches.append(match)
        return matches
    else:
        for p,P in patterns:
            next = [o for o in pDict['outedges'][startnode] if pDict['walllabels'][o] in P] # get adjacent nodes with labels that are compatible with the pattern
            for n in next:
                if pDict['walllabels'][n] == p: # if we hit the next pattern element, reduce pattern by one
                    matches=recursePattern(n,match+[n],matches,patterns[1:],pDict)
                elif not repeatingLoop(match+[n]): # if we hit an intermediate node, call pattern without reduction provided there isn't a repeating loop; note: checking repeatingLoop over and over again is slow, but I haven't found a better method
                    matches=recursePattern(n,match+[n],matches,patterns,pDict)
        return matches

def labelOptions(p):
    # there is exactly one 'm' or 'M' in p
    if 'm' in p:
        return [p,p.replace('m','d')]
    elif 'M' in p:
        return [p,p.replace('M','u')]

def sanitycheck(pattern,walllabels):
    # make sure inputs meet requirements of algorithm
    if not pattern:
        return "None. Pattern is empty."
    missing = [p for p in pattern if p not in walllabels] 
    if missing:
        return "None. Pattern element(s) {} do not exist as wall labels in the graph.".format(missing)  
    notextrema = [p for p in pattern if not set(p).intersection(['m','M'])]
    if notextrema:
        return "None. Pattern element(s) {} are not extrema. An 'm' or 'M' is required in every element.".format(notextrema)
    multipleextrema = [w for w in walllabels if w.count('m') + w.count('M') > 1]
    if multipleextrema:
        return "None. Graph label(s) {} contain more than one extremum.".format(multipleextrema)
    wrongchars = filter(None,[''.join([ s for s in set(w).difference(['u','d','m','M'])]) for w in walllabels])
    if wrongchars:
        return "None. Graph labels contain inadmissible character(s) {}.".format(wrongchars)
    return "sane"  

def matchPattern(pattern,walllabels,outedges,suppress=0):
    '''
    Matches pattern in a labeled graph with edges in outedges and labels in walllabels. The pattern is 
    described in terms of walllabels, and a pattern label of the wrong type will return no match. If there
    is a match to the pattern, the paths that respect it will be returned in terms of wall number (the index
    of outedges).

    outedges: list of tuples of integers, index is wall number
    walllabels: list of uniform-length strings of labels from the alphabet ('u','d','m','M'); index is wall number;
        every wall has at most one 'm' or 'M' in its label
    pattern: list of uniform-length strings of labels from the alphabet ('u','d','m','M'); exactly one 'm' or 'M' REQUIRED per string; to find a path, all elements of pattern must be wall labels that exist in the graph; patterns containing exactly repeating sequences will not be found if the same walls must be traversed to match the pattern
    suppress: 0 means give information about cyclic or acyclic pattern request, 1 means suppress it

    See patternmatch_unittests.py for examples of function calls. 

    See notes for meaning of alphabet. Briefly, 'uMdd' means that on the wall in question, the first variable is 
    increasing (up), the second variable is at a maximum (Max), and the third and fourth variables are decreasing
    (down). The character 'm' means a variable is at a minimum (min). There can be at most one 'm' or 'M' at each 
    wall, because we assume that the input graph arises from a switching network where each regulation event occurs
    at a unique threshold.

    '''
    # sanity check the input 
    S=sanitycheck(pattern,walllabels)
    if S !="sane":
        return S
    # give information about the type of pattern received
    if not suppress:
        if pattern[0] != pattern[-1]:
            print('Seeking acyclic path.')
        else:
            print('Seeking cyclic path. Acyclic paths that match the pattern may exist if wall labels are not unique, but these will not be returned.')
    # calculate all possible starting nodes and return trivial length one patterns
    firstwalls=[i for i in range(len(walllabels)) if walllabels[i] == pattern[0]]
    if len(pattern)==1:
        return [ (w,) for w in firstwalls ]
    # pre-cache intermediate nodes that may exist in the wall graph (saves time in recursive call)
    patternoptions=[labelOptions(p) for p in pattern[1:]]
    patternParams = zip(pattern[1:],patternoptions)
    paramDict = {'walllabels':walllabels,'outedges':outedges,'stop':pattern[-1],'lenpattern':len(pattern)}
    # find matches
    results=[]
    for w in firstwalls:
        R = recursePattern(w,[w],[],patternParams,paramDict) # seek match starting at w
        results.extend(list(set(tuple(l) for l in R if l))) # pull out the unique paths found
    # prep matches for return
    if results:
        results = list(set(results))
        if pattern[0]==pattern[-1]:
            # remove acyclic paths from a cyclic search
            results = [r for r in results if r[0]==r[-1]]
        return results
    else:
        return "None. No results found."
