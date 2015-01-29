import itertools

def isVarGTorLT(nodeval,nodelist,walldomains,varind):
    # Find out whether nodeval (associated to varind) is 
    # >= or <= all the values in the corresponding element 
    # of the walldomain entry for each value of nodelist.
    # This helps determine the behavior of the variable 
    # varind at the current wall.
    #
    # optimized; previous version iterated over list 3 times
    #
    gt=True
    lt=True
    nz=False
    for k in nodelist:
        d=nodeval-walldomains[k][varind]
        if d>0:
            nz=True
            lt=False
        elif d<0:
            nz=True
            gt=False
    return gt*nz,lt*nz

def getChars(Z,previouswall,nextwall,outedges,walldomains):
    # Z contains the variable index and the values of variable at the previous, 
    # current, and next walls respectively. Given the graph labeled with walldomains, 
    # we find all possible behaviors of the variable at the current wall given the
    # trajectory defined by the previous and next walls.
    #
    # this algorithm works but is heinous to read; making it shorter means it runs slower
    #
    q,p,w,n=Z
    if p<w<n:
        chars = ['u']
    elif p>w>n:
        chars = ['d']
    elif p<w>n:
        chars=['M']
    elif p>w<n:
        chars=['m']
    elif p==w and w!=n:
        nn=getNextNodes(previouswall,outedges)
        pgt,plt=isVarGTorLT(p,nn,walldomains,q)
        if w>n:
            if pgt:
                chars=['d']
            elif plt:
                chars=['M']
            else:
                chars=['d','M']
        elif w<n:
            if pgt:
                chars=['m']
            elif plt:
                chars=['u']
            else:
                chars=['u','m']
    elif w==n and w!=p:
        pp=getPreviousNodes(nextwall,outedges)
        ngt,nlt=isVarGTorLT(n,pp,walldomains,q)
        if p<w:
            if ngt:
                chars=['u']
            elif nlt:
                chars=['M']
            else:
                chars=['u','M']
        elif p>w:
            if ngt:
                chars=['m']
            elif nlt:
                chars=['d']
            else:
                chars=['d','m']
    else:
        nn=getNextNodes(previouswall,outedges)
        pp=getPreviousNodes(nextwall,outedges)
        pgt,plt=isVarGTorLT(p,nn,walldomains,q)
        ngt,nlt=isVarGTorLT(n,pp,walldomains,q)
        if pgt:
            if ngt:
                chars=['m']
            elif nlt:
                chars=['d']
            else:
                chars=['m','d']
        elif plt:
            if ngt:
                chars=['u']
            elif nlt:
                chars=['M']
            else:
                chars=['M','u']
        elif ngt:
            chars=['u','m']
        elif nlt:
            chars=['d','M']
        else:
            chars=['d','M','u','m']
    return chars

def getChars2(z,varatwall):
    # z contains the variable index and the values of variable at the previous, 
    # current, and next walls respectively. Given the graph labeled with walldomains, 
    # we find all possible behaviors of the variable at the current wall given the
    # trajectory defined by the previous and next walls, mediated by whether or
    # not the variable in z[0] can be affected at the current wall. The variable
    # that's affected at the wall is stored in varatwall.
    q,p,w,n=z
    if p<w<n:
        chars=['u']
    elif p>w>n:
        chars=['d']
    elif q==varatwall:
        if p>w<n:
            chars = ['m']
        elif p<w>n:
            chars = ['M']
        elif p<w==n:
            chars = ['u','M']
        elif p==w<n:
            chars = ['u','m']
        elif p>w==n:
            chars = ['d','m']
        elif p==w>n:
            chars = ['d','M']
        else:
            chars = ['u','d','m','M']
    else:
        if p<w==n or p==w<n:
            chars = ['u']
        elif p>w==n or p==w>n:
            chars = ['d']
        elif p==w==n:
            chars = ['u','d']
        else:
            chars = [] # if the path indicates a max or a min, then this is a nonviable path
    return chars

def pathDependentStringConstruction2(previouswall,wall,nextwall,walldomains,varatwall):
    # make a label for 'wall' that depends on where the path came from and where it's going
    if wall==nextwall: #if at steady state, do not label
        return []
    walllabels=['']
    Z=zip(range(len(walldomains[0])),walldomains[previouswall],walldomains[wall],walldomains[nextwall])
    while Z:
        chars=getChars2(Z[0],varatwall)
        if chars:
            walllabels=[l+c for l in walllabels for c in chars]
            Z.pop(0)
        else:
            return []
    return walllabels

def pathDependentStringConstruction(previouswall,wall,nextwall,walldomains,outedges):
    # make a label for 'wall' that depends on where the path came from and where it's going
    if wall==nextwall: #if at steady state, do not label
        return []
    walllabels=['']
    Z=zip(range(len(walldomains[0])),walldomains[previouswall],walldomains[wall],walldomains[nextwall])
    while Z:
        chars=getChars(Z[0],previouswall,nextwall,outedges,walldomains)
        walllabels=[l+c for l in walllabels for c in chars]
        Z.pop(0)
    return walllabels

def testStringConstruction(walldomains,outedges):
    R=range(len(outedges))
    inedges=[tuple([j for j,o in enumerate(outedges) if i in o ]) for i in R]
    for k in R:
        ie=inedges[k]
        oe=outedges[k]
        wl=[]
        for i,o in itertools.product(ie,oe):
            wl.extend(pathDependentStringConstruction(i,k,o,walldomains,outedges))
        # print ie
        # print oe
        print(list(set(wl)))

def getFirstwalls(firstpattern,outedges,walldomains,varsaffectedatwall):
    # Given the first word in the pattern, find the nodes in the graph that have 
    # this pattern for some path. Our searches will start at each of these nodes.
    inedges=[tuple([j for j,o in enumerate(outedges) if i in o]) for i in range(len(outedges))]
    firstwalls=[]
    for k,(ie,oe) in enumerate(zip(inedges,outedges)):
        wl=[]
        for i,o in itertools.product(ie,oe):
            wl.extend(pathDependentStringConstruction2(i,k,o,walldomains,varsaffectedatwall[k]))
        if firstpattern in wl:
            firstwalls.append(k)
    return firstwalls

