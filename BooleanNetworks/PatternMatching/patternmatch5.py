def labelOptions(p):
    return set([p, ''.join([ c if c not in ['m','M'] else 'd' if c == 'm' else 'u' for c in p ])])

def searchAdjacent(p,walllabels,nextedges):
    next=[]
    for o in nextedges:
        if walllabels[o] in labelOptions(p):
            next.append(o)
    return next

def pathToEnd(start,end,walllabels,outedges):
    # start is an index, end is a label
    # trivial case
    if start == end:
        return [start]
    # end is one step away
    startinds = outedges[start]
    startlabels = [walllabels[i] for i in startinds]
    if end in startlabels:
        return [start,startinds[startlabels.index(end)]]
    # end is n steps away, where all intermediate n-1 steps have the same label
    endlabels = labelOptions(end)
    intermediate = endlabels.intersection(startlabels)
    nextlabels = startlabels
    path = [start]
    while intermediate in nextlabels:
        ind = nextlabels.index(intermediate)
        path.append(ind)
        nextinds = outedges[ind]
        nextlabels = [walllabels[i] for i in nextinds]
        if end in nextlabels:
            return path.append(nextinds[nextlabels.index(end)])
    return []


def recursePattern(pattern,walllabels,outedges,startnode=-1):
    if not pattern:
        return []
    else:
        match=[startnode]
        p = pattern[0]
        next = searchAdjacent(p,walllabels,outedges[match[-1]])
        for n in next:
            if walllabels[n] == p:
                match.extend(recursePattern(pattern[1:],walllabels,outedges,n))
            else:
                # need path between walllabels[n] and p
                match.extend(pathToEnd(n,p,walllabels,outedges))
                match.extend(recursePattern(pattern[1:],walllabels,outedges,match[-1]))
        return match

def matchPattern(pattern,walllabels,outedges,cycle='y'):
    # make sure there is a wall associated to each entry (assumes each p in pattern has exactly one m or M)
    for p in pattern:
        if p not in walllabels:
            return None
    # make start node with an output to every edge
    outedges.extend([tuple(range(len(walllabels)))])
    walllabels.append('-1')
    # if looking for a cycle, make sure data is cyclic
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
