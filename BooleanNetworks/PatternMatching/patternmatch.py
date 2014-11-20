def flattenlessone(l):
    if all(isinstance(el, list) for el in l) and not any(isinstance(a,list) for el in l for a in el):
        return l
    else:
        flat = []
        for el in l:
            if any(isinstance(a,list) for a in el):
                flat.extend(flattenlessone(el))
            else:
                flat.append(el)
        return flat

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
    return set([p, ''.join([ c if c not in ['m','M'] else 'd' if c == 'm' else 'u' for c in p ])])

def searchAdjacent(w,p,walllabels,outedges):
    return [o for o in outedges[w] if walllabels[o] in labelOptions(p)]

def recursePattern(startnode,pattern,match,walllabels,outedges,start,stop,lenpattern):
    # this algorithm assumes we start at the first node matching pattern[0]
    if len(match) >= lenpattern and match[0]==start and walllabels[match[-1]] == stop:
        return match
    else:
        matches=[]
        for p in pattern:
            next = searchAdjacent(startnode,p,walllabels,outedges)
            for n in next:
                if n == p: # if we hit the next node, reduce pattern by one
                    matches.append(recursePattern(n,pattern[1:],match+[n],walllabels,outedges,start,stop,lenpattern))
                elif not repeatingLoop(match+[n]): # if we hit an intermediate node, call pattern again, provided there isn't a repeating loop
                    matches.append(recursePattern(n,pattern,match+[n],walllabels,outedges,start,stop,lenpattern))
        return flattenlessone(matches)

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
    results=[]
    for w in firstwalls:
        # seek match starting at w
        R = recursePattern(w,pattern[1:],[w],walllabels,outedges,w,pattern[-1],len(pattern))
        # pull out the unique paths found
        results.extend(list(set(tuple(l) for l in R if l)))
    if results:
        return list(set(results))
    else:
        return None
