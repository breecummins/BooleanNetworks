def flattenlessone(l):
    if all(isinstance(el, list) for el in l) and not any(isinstance(a,list) for el in l for a in el):
        return l
    else:
        flat = []
        for el in l:
            flat.extend(flattenlessone(el))
        return flat

def recursePattern(pattern,outedges,walllabels,match=[],startnode=-1):
    if not pattern:
        return []
    else:
        matches=[]
        for p in pattern:
            for i in range(len(outedges)):
                if i in outedges[startnode]:
                    if walllabels[i] == p:
                        matches.append(recursePattern(pattern[1:],outedges,walllabels,match+[i]))
                    elif walllabels[i] == tuple([ c if c not in ['m','M'] else 'd' if c == 'm' else 'u' for c in p ]):
                        matches.append(recursePattern(pattern,outedges,walllabels,match+[i]))
        return flattenlessone(matches)


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
