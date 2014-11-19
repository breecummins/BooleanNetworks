def flattenlessone(l):
    if all(isinstance(el, list) for el in l) and not any(isinstance(a,list) for el in l for a in el):
        return l
    else:
        flat = []
        for el in l:
            flat.extend(flattenlessone(el))
        return flat

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
            print(next)
            for n in next:
                matches.append(recursePattern(n,pattern[1:],match+[n],walllabels,outedges,start,stop))
        return flattenlessone(matches)

def findFirstWall(p0,walllabels):
    for i,w in enumerate(walllabels):
        if w == p0:
            return i
    return None

def matchPattern(pattern,walllabels,outedges):
    if pattern[0] != pattern[-1]:
        print('Seeking path, not cycle.')
    w = findFirstWall(pattern[0],walllabels)
    if w is None:
        return "First label not found in graph. Process aborted."
    elif len(pattern)==1:
        return [w]
    else:
        R = recursePattern(w,pattern[1:],[w],walllabels,outedges,w,pattern[-1])
        return list(set(tuple(l) for l in R))



if __name__ == "__main__":
    outedges=[] # list of tuples of integers, position is wall index
    walllabels=[] # list of tuples of labels ('u','d','m','M'), position is wall index
    pattern=[] # list of tuples of labels, position is not meaningful, exactly one 'm' or 'M' allowed per tuple (i.e. already split data appropriately and 0's all removed)

    # ASSUME ALL WALLS UNIQUE, ASSUME GIVEN PATH EXISTS EXACTLY IN GRAPH

    # EXAMPLE 0
    outedges=[(1,),(2,),(3,),(0,)]
    walllabels=['uuu','uMu','udu','umu']
    pattern=['uuu','uMu','udu','umu','uuu']
    match = matchPattern(pattern,walllabels,outedges)
    print(match) # == [0,2,5,6,0]

    outedges=[(1,),(2,),(3,),(0,)]
    walllabels=['uuu','uMu','udu','umu']
    pattern=['uMu','udu','umu','uuu','uMu'] # permuted pattern
    match = matchPattern(pattern,walllabels,outedges)
    print(match)

