def flattenlessone(l):
    if all(isinstance(el, list) for el in l) and not any(isinstance(a,list) for el in l for a in el):
        return l
    else:
        flat = []
        for el in l:
            flat.extend(flattenlessone(el))
        return flat

def repeatingLoop(match):
    N=len(match)
    if len(set(match)) == N:
        return False
    else:
        for n in range(1,N/2):
            if match[N-n:N] == match[N-2*n:N-n]:
                return True
        return False

def labelOptions(p,q):
    lo = set([p, ''.join([ c if c not in ['m','M'] else 'd' if c == 'm' else 'u' for c in p ])])
    return lo.difference(set(q))

def searchAdjacent(w,p,walllabels,outedges):
    next=[]
    lo = labelOptions(p,walllabels[w])
    for o in outedges[w]:
        if walllabels[o] in lo:
            next.append(o)
    return next

def recursePattern(startnode,pattern,match,walllabels,outedges,start,stop):
    # match needs to be initialized with first startnode
    if len(match) > 1 and match[0]==start and walllabels[match[-1]] == stop:
        return match
    else:
        matches=[]
        for p in pattern:
            next = searchAdjacent(startnode,p,walllabels,outedges)
            for n in next:
                if n == p: # if we hit the next node, reduce pattern by one
                    matches.append(recursePattern(n,pattern[1:],match+[n],walllabels,outedges,start,stop))
                elif not repeatingLoop(match+[n]): # if we didn't hit the next node, call pattern again, provided there isn't a repeating loop
                    matches.append(recursePattern(n,pattern,match+[n],walllabels,outedges,start,stop))
        return flattenlessone(matches)

def findFirstWall(p0,walllabels):
    for i,w in enumerate(walllabels):
        if w == p0:
            return i
    return None

def matchPattern(pattern,walllabels,outedges):
    '''
    Matches pattern in a labelled graph with edges in outedges and labels in walllabels. The pattern is 
    described in terms of walllabels, and a pattern label of the wrong type will return no match. If there
    is a match to the pattern, the paths that respect it will be returned in terms of wall number (the index
    of outedges).

    outedges: list of tuples of integers, index is wall number
    walllabels: list of uniform-length strings of labels from the alphabet ('u','d','m','M'), index is wall number
    pattern: list of uniform-length strings of labels from the alphabet ('u','d','m','M'); index is not meaningful except that the order of the pattern is preserved; exactly one 'm' or 'M' allowed per tuple; if there is no 'm' or 'M' in the first element of pattern, then the element must be a wall label that exists in the graph (eventually may change this); patterns containing exactly repeating sequences will not be found (eventually may change this).

    See patternmatch_unittests.py for examples of function calls.

    '''
    # give information about the type of pattern received
    if pattern[0] != pattern[-1]:
        print('Seeking acyclic path.')
    else:
        print('Seeking cyclic path. May not succeed unless walls are unique.')
    if any([p not in walllabels and ('m' in p or 'M' in p) for p in pattern]):
        return "None. The following extremal elements of the pattern do not exist as wall labels in the graph: {}.".format(list(set(pattern).difference(set(pattern).intersection(set(walllabels)))))
    w = findFirstWall(pattern[0],walllabels)
    if w is None:
        return "None. First element of pattern {} not found in graph.".format(pattern[0])
    elif len(pattern)==1:
        return [tuple(w)]
    else:
        R = recursePattern(w,pattern[1:],[w],walllabels,outedges,w,pattern[-1])
        L = list(set(tuple(l) for l in R if l))
        if L:
            return L
        else:
            return None
