def repeatingLoop(match):
    N=len(match)
    if len(set(match)) == N:
        return False
    else:
        for n in range(1,N/2+1):
            if match[N-n:N] == match[N-2*n:N-n]:
                return True
        return False

def labelOptions(p):
    # there can be at most one 'm' or 'M' in p
    # optimized
    if 'm' in p:
        return [p,p.replace('m','d')]
    elif 'M' in p:
        return [p,p.replace('M','u')]
    else:
        return [p]

def recursePattern(startnode,pattern,patternoptions,match,walllabels,outedges,stop,lenpattern,matches):
    # optimized
    if len(match) >= lenpattern and walllabels[match[-1]] == stop:
        matches.append(match)
        return matches
    else:
        for p,P in zip(pattern,patternoptions):
            next = [o for o in outedges[startnode] if walllabels[o] in P] # get adjacent nodes with labels that are compatible with the pattern
            for n in next:
                if n == p: # if we hit the next pattern element, reduce pattern by one
                    matches=recursePattern(n,pattern[1:],patternoptions[1:],match+[n],walllabels,outedges,stop,lenpattern,matches)
                elif not repeatingLoop(match+[n]): # if we hit an intermediate node, call pattern again, provided there isn't a repeating loop
                # checking repeatingLoop over and over again is slow
                    matches=recursePattern(n,pattern,patternoptions,match+[n],walllabels,outedges,stop,lenpattern,matches)
        return matches

def matchPattern(pattern,walllabels,outedges,suppress=0):
    '''
    Matches pattern in a labelled graph with edges in outedges and labels in walllabels. The pattern is 
    described in terms of walllabels, and a pattern label of the wrong type will return no match. If there
    is a match to the pattern, the paths that respect it will be returned in terms of wall number (the index
    of outedges).

    outedges: list of tuples of integers, index is wall number
    walllabels: list of uniform-length strings of labels from the alphabet ('u','d','m','M'), index is wall number
    pattern: list of uniform-length strings of labels from the alphabet ('u','d','m','M'); index is not meaningful except that the order of the pattern is preserved; exactly one 'm' or 'M' allowed per tuple; to find a path, all elements of pattern must be wall labels that exist in the graph; patterns containing exactly repeating sequences will not be found if they induce the tranversal of a cycle more than once.
    suppress: 0 means give information about cyclic or acyclic pattern request, 1 means suppress it

    See patternmatch_unittests.py for examples of function calls.

    '''
    # handle trivial patterns
    if not pattern:
        return None
    missing = [p for p in pattern if p not in walllabels] 
    if missing:
        return "None. Pattern elements {} do not exist as wall labels in the graph.".format(missing)
    firstwalls=[i for i in range(len(walllabels)) if walllabels[i] == pattern[0]]
    if len(pattern)==1:
        return [ (w,) for w in firstwalls ]
    # give information about the type of pattern received
    if not suppress:
        if pattern[0] != pattern[-1]:
            print('Seeking acyclic path.')
        else:
            print('Seeking cyclic path. May return acyclic paths if wall labels are not unique.')
    # find matches
    patternoptions=[labelOptions(p) for p in pattern[1:]]
    results=[]
    for w in firstwalls:
        # seek match starting at w
        R = recursePattern(w,pattern[1:],patternoptions,[w],walllabels,outedges,pattern[-1],len(pattern),[])
        # pull out the unique paths found
        results.extend(list(set(tuple(l) for l in R if l)))
    if results:
        return list(set(results))
    else:
        return None
