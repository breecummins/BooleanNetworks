def labelOptions(p):
    return set([p, ''.join([ c if c not in ['m','M'] else 'd' if c == 'm' else 'u' for c in p ])])

def findWall(p,walllabels):
    walls=[]
    for l in labelOptions(p):
        try:
            walls.extend(walllabels.index(l))
        except:
            pass
    return walls

def recursePattern(startnode,pattern,walllabels,outedges):
    if not pattern:
        return True
    else:
        for p in pattern:
            candidates = set(findWall(p,walllabels)).intersection(set(outedges[startnode]))
            if candidates:
                for c in candidates:
                    if walllabels[c] == p:
                        match = recursePattern(c,pattern[1:],walllabels,outedges)
                    else:
                        match = recursePattern(c,[p],walllabels,outedges)
            else:
                return False
        return match

def matchPattern(pattern,walllabels,outedges,cycle='y'):
    # make start node with an output to every edge
    if not pattern:
        return True
    # outedges.extend([tuple(range(len(walllabels)))])
    # walllabels.append('-1')
    # outedges = makeNewOutedges(walllabels,outedges)
    if cycle == 'y' and pattern[0] != pattern[-1]:
        pattern = pattern + [pattern[0]]   
    walls = findWall(pattern[0],walllabels)
    for w in walls:
        match = recursePattern(w,pattern,walllabels,outedges)
        if match:
            return True    
    return False

if __name__ == "__main__":
    outedges=[] # list of tuples of integers, position is wall index
    walllabels=[] # list of tuples of labels ('u','d','m','M'), position is wall index
    pattern=[] # list of tuples of labels, position is not meaningful, exactly one 'm' or 'M' allowed per tuple (i.e. already split data appropriately and 0's all removed)

    # EXAMPLE 1
    outedges=[(1,2),(3,),(4,5),(7,),(8,),(4,6),(0,),(8,),(8,)]
    walllabels=['uuu','uuM','uMu','uud','udM','udu','umu','uMd','udd']
    pattern=['uuu','uMu','umu','uuu']
    match = matchPattern(pattern,walllabels,outedges,cycle='y')
    print(match) # == [0,2,5,6,0]

    outedges=[(1,2),(3,),(4,5),(7,),(8,),(4,6),(0,),(8,),(8,)]
    walllabels=['uuu','uuM','uMu','uud','udM','udu','umu','uMd','udd']
    pattern=['uMu','umu']
    match = matchPattern(pattern,walllabels,outedges,cycle='y')
    print(match)

    outedges=[(1,2),(3,),(4,5),(7,),(8,),(4,6),(0,),(8,),(8,)]
    walllabels=['uuu','uuM','uMu','uud','udM','udu','umu','uMd','udd']
    pattern=['uMu','uMd']
    match = matchPattern(pattern,walllabels,outedges,cycle='y')
    print(match)

    # EXAMPLE 2
