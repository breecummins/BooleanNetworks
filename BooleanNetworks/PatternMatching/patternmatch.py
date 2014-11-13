def labelOptions(p):
    return set([p, tuple([ c if c not in ['m','M'] else 'u' if c == 'm' else 'd' for c in p ])])

def searchAdjacent(w,p,walllabels,outedges):
    next=[]
    lo = labelOptions(p)
    for o in outedges[w]:
        if walllabels[o] in lo:
            next.append(o)
    return next

def recursePattern(startnode,pattern,walllabels,outedges):
    if not pattern:
        return []
    else:
        match=[startnode]
        for p in pattern:
            next = searchAdjacent(match[-1],p,walllabels,outedges)
            for n in next:
                match.extend(recursePattern(n,pattern[1:],walllabels,outedges))
        return match

def findFirstWall(p0,walllabels):
    for i,w in enumerate(walllabels):
        if w == p0:
            return i

def matchPattern(pattern,walllabels,outedges,cycle='y'):
    if cycle == 'y' and pattern[0] != pattern[-1]:
        pattern = pattern + [pattern[0]]
    w = findFirstWall(pattern[0],walllabels)
    if w is None:
        return "First label not found in graph. Process aborted."
    return recursePattern(w,pattern,walllabels,outedges)



if __name__ == "__main__":
    outedges=[] # list of tuples of integers, position is wall index
    walllabels=[] # list of tuples of labels ('u','d','m','M'), position is wall index
    pattern=[] # list of tuples of labels, position is not meaningful, exactly one 'm' or 'M' allowed per tuple (i.e. already split data appropriately and 0's all removed)

    # EXAMPLE 1
    outedges=[(1,2),(3,),(4,5),(7,),(8,),(4,6),(0,),(8,),(8,)]
    walllabels=[('u','u','u'),('u','u','M'),('u','M','u'),('u','u','d'),('u','d','M'),('u','d','u'),('u','m','u'),('u','M','d'),('u','d','d')]
    pattern=[('u','u','u'),('u','M','u'),('u','m','u'),('u','u','u')]
    match = matchPattern(pattern,walllabels,outedges,cycle='y')
    print(match) # == [0,2,5,6,0]

    pattern=[('u','M','u'),('u','m','u')]
    match = matchPattern(pattern,walllabels,outedges,cycle='y')
    print(match)

    pattern=[('u','M','u'),('u','M','d')]
    match = matchPattern(pattern,walllabels,outedges,cycle='y')
    print(match)

    # EXAMPLE 2
