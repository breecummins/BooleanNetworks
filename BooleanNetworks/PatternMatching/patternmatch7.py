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
    if pattern[0] != pattern[-1]:
        print('Seeking path, not cycle.')
    if any([p not in walllabels and ('m' in p or 'M' in p) for p in pattern]):
        return "None. The following extrema in the pattern do not exist on the walls: {}.".format(list(set(pattern).difference(set(pattern).intersection(set(walllabels)))))
    w = findFirstWall(pattern[0],walllabels)
    if w is None:
        return "None. First element of pattern not found in graph."
    elif len(pattern)==1:
        return [w]
    else:
        R = recursePattern(w,pattern[1:],[w],walllabels,outedges,w,pattern[-1])
        L = list(set(tuple(l) for l in R if l))
        if L:
            return "Paths are {}.".format(L)
        else:
            return None



if __name__ == "__main__":
    outedges=[] # list of tuples of integers, position is wall index
    walllabels=[] # list of tuples of labels ('u','d','m','M'), position is wall index
    pattern=[] # list of tuples of labels, position is not meaningful, exactly one 'm' or 'M' allowed per tuple (i.e. already split data appropriately and 0's all removed)

    # # ASSUME ALL WALLS UNIQUE, ASSUME GIVEN PATH EXISTS EXACTLY IN GRAPH, ASSUME FIRST ELEMENT OF PATTERN IS A WALL

    # # EXAMPLE 0
    # outedges=[(1,),(2,),(3,),(0,)]
    # walllabels=['uuu','uMu','udu','umu']
    # pattern=['uuu','uMu','udu','umu','uuu']
    # match = matchPattern(pattern,walllabels,outedges)
    # print(match) # == [0,1,2,3,0]

    # # EXAMPLE 0
    # outedges=[(1,),(2,),(3,),(0,)]
    # walllabels=['uuu','uMu','udu','umu']
    # pattern=['uMu','udu','umu','uuu','uMu'] # permuted pattern
    # match = matchPattern(pattern,walllabels,outedges)
    # print(match) # == [1,2,3,0,1]

    # # ASSUME ALL WALLS UNIQUE, GIVEN PATH HAS INTERMEDIATE LOWERCASE WALLS ONLY, ASSUME FIRST ELEMENT OF PATTERN IS A WALL

    # # EXAMPLE 1
    # outedges=[(1,),(2,3),(3,),(0,)]
    # walllabels=['uuu','uMu','udu','umu']
    # pattern=['uMu','umu','uMu'] # permuted pattern
    # match = matchPattern(pattern,walllabels,outedges)
    # print(match) # == [(1, 2, 3, 0, 1), (1, 3, 0, 1)]

    # # EXAMPLE 2
    # outedges=[(1,2),(3,),(4,5),(7,),(8,),(4,6),(0,),(8,),(8,)]
    # walllabels=['uuu','uuM','uMu','uud','udM','udu','umu','uMd','udd']
    # pattern=['uuu','uMu','udu','umu','uuu']
    # match = matchPattern(pattern,walllabels,outedges)
    # print(match) # == [0,2,5,6,0]

    # # EXAMPLE 2
    # outedges=[(1,2),(3,),(4,5),(7,),(8,),(4,6),(0,),(8,),(8,)]
    # walllabels=['uuu','uuM','uMu','uud','udM','udu','umu','uMd','udd']
    # pattern=['uMu','udu','umu','uuu','uMu'] # permuted pattern
    # match = matchPattern(pattern,walllabels,outedges)
    # print(match) # == [2,5,6,0,2]

    # # EXAMPLE 2
    # outedges=[(1,2),(3,),(4,5),(7,),(8,),(4,6),(0,),(8,),(8,)]
    # walllabels=['uuu','uuM','uMu','uud','udM','udu','umu','uMd','udd']
    # pattern=['uMu','umu','uuM']
    # match = matchPattern(pattern,walllabels,outedges)
    # print(match) # == [2,5,6,0,1]

    # # EXAMPLE 2: THE FOLLOWING PATTERN DNE
    # outedges=[(1,2),(3,),(4,5),(7,),(8,),(4,6),(0,),(8,),(8,)]
    # walllabels=['uuu','uuM','uMu','uud','udM','udu','umu','uMd','udd']
    # pattern=['uMu','udu','udM','uMd','udd','Mdd']
    # match = matchPattern(pattern,walllabels,outedges)
    # print(match) # == None

    # # EXAMPLE 2: THE FOLLOWING PATTERN DNE
    # outedges=[(1,2),(3,),(4,5),(7,),(8,),(4,6),(0,),(8,),(8,)]
    # walllabels=['uuu','uuM','uMu','uud','udM','udu','umu','uMd','udd']
    # pattern=['udM','udd','uMd']
    # match = matchPattern(pattern,walllabels,outedges)
    # print(match) # == None

    # # EXAMPLE 3: THE FOLLOWING PATTERN DNE
    # outedges=[(1,2),(3,),(4,5),(7,),(8,),(4,6),(0,),(8,),(9,),(10,),(8,)]
    # walllabels=['uuu','uuM','uMu','uud','udM','udu','umu','uMd','udd','Mdd','mdd']
    # pattern=['udM','udd','uMd']
    # match = matchPattern(pattern,walllabels,outedges)
    # print(match) # == None

    # EXAMPLE 3
    outedges=[(1,2),(3,),(4,5),(7,),(8,),(4,6),(0,),(8,),(8,9),(10,),(8,)]
    walllabels=['uuu','uuM','uMu','uud','udM','udu','umu','uMd','udd','Mdd','mdd']
    pattern=['umu','uuM','uMd','Mdd']
    match = matchPattern(pattern,walllabels,outedges)
    print(match) # == [6,0,1,3,7,8,9]

    # # EXAMPLE 3: THE FOLLOWING PATTERN DNE
    # outedges=[(1,2),(3,),(4,5),(7,),(8,),(4,6),(0,),(8,),(9,),(10,),(8,)]
    # walllabels=['uuu','uuM','uMu','uud','udM','udu','umu','uMd','udd','Mdd','mdd']
    # pattern=['umu','uuM','uMd','Mdd','mdd','udM']
    # match = matchPattern(pattern,walllabels,outedges)
    # print(match) # == None

