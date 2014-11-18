def labelOptions(p):
    return set([p, ''.join([ c if c not in ['m','M'] else 'd' if c == 'm' else 'u' for c in p ])])

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
    return None

def matchPattern(pattern,walllabels,outedges):
    if pattern[0] != pattern[-1]:
        print('Seeking path, not cycle.')
    w = findFirstWall(pattern[0],walllabels)
    if w is None:
        return "First label not found in graph. Process aborted."
    else:
        return recursePattern(w,pattern[1:],walllabels,outedges)



if __name__ == "__main__":
    # ASSUME ALL WALLS UNIQUE

    outedges=[] # list of tuples of integers, position is wall index
    walllabels=[] # list of tuples of labels ('u','d','m','M'), position is wall index
    pattern=[] # list of tuples of labels, position is not meaningful, exactly one 'm' or 'M' allowed per tuple (i.e. already split data appropriately and 0's all removed)

    # EXAMPLE 1
    outedges=[(1,2),(3,),(4,5),(7,),(8,),(4,6),(0,),(8,),(8,)]
    walllabels=['uuu','uuM','uMu','uud','udM','udu','umu','uMd','udd']
    pattern=['uuu','uMu','udu','umu','uuu']
    match = matchPattern(pattern,walllabels,outedges)
    print(match) # == [0,2,5,6,0]

    outedges=[(1,2),(3,),(4,5),(7,),(8,),(4,6),(0,),(8,),(8,)]
    walllabels=['uuu','uuM','uMu','uud','udM','udu','umu','uMd','udd']
    pattern=['uMu','udu','umu','uuu','uMu']
    match = matchPattern(pattern,walllabels,outedges)
    print(match)

    outedges=[(1,2),(3,),(4,5),(7,),(8,),(4,6),(0,),(8,),(8,)]
    walllabels=['uuu','uuM','uMu','uud','udM','udu','umu','uMd','udd']
    pattern=['uMu','udu','udM','uMd','udd','Mdd']
    match = matchPattern(pattern,walllabels,outedges)
    print(match)
