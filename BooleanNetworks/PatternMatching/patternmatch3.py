def labelOptions(p):
    return set([p, ''.join([ c if c not in ['m','M'] else 'd' if c == 'm' else 'u' for c in p ])])

def searchAdjacent(oe,p,walllabels):
    return [walllabels.index(l) for l in set(oe).intersection(labelOptions(p))]

def recursePattern(pattern,walllabels,outedges,startnode=-1):
    if not pattern:
        return []
    else:
        match=[startnode]
        p = pattern[0]
        next = searchAdjacent(outedges[match[-1]],p,walllabels)
        for n in next:
            if walllabels[n] == p:
                match.extend(recursePattern(pattern[1:],walllabels,outedges,n))
            else:
                # need path between walllabels[n] and p
                match.extend(recursePattern([p],walllabels,outedges,n))
        return match

def makeNewOutedges(walllabels,outedges):
    return [[walllabels[o] for o in outedges[w]] for w in range(len(walllabels))]

def matchPattern(pattern,walllabels,outedges,cycle='y'):
    # make start node with an output to every edge
    outedges.extend([tuple(range(len(walllabels)))])
    walllabels.append('-1')
    outedges = makeNewOutedges(walllabels,outedges)
    if cycle == 'y' and pattern[0] != pattern[-1]:
        pattern = pattern + [pattern[0]]
    return recursePattern(pattern,walllabels,outedges)[1:]



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
