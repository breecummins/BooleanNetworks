import itertools
import sys

def getNextNodes(node,outedges):
    return [o for o in outedges[node]]

def getPreviousNodes(node,outedges):
    return [j for j,o in enumerate(outedges) if node in o]

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

def helper2(q,w,n,nextwall,currentwall,outedges,walldomains):
    # is the next wall <= or >= (or neither) all of its previous adjacent walls?
    # is the current wall <= or >= (or neither) all of its next adjacent walls?
    nn=getPreviousNodes(nextwall,outedges)
    if len(nn)>1:
        ngtw,nltw=isVarGTorLT(n,nn,walldomains,q)
    else:
        ngtw,nltw=False,False
    qn=getNextNodes(currentwall,outedges)
    if len(qn)>1:
        wgtn,wltn=isVarGTorLT(w,qn,walldomains,q)
    else:
        wgtn,wltn=False,False
    return wgtn,wltn,ngtw,nltw

def helper1(q,p,w,previouswall,currentwall,outedges,walldomains):
    # is the previous wall <= or >= (or neither) all of its next adjacent walls?
    # is the current wall <= or >= (or neither) all of its previous adjacent walls?
    pp=getNextNodes(previouswall,outedges)
    if len(pp)>1:
        pgtw,pltw=isVarGTorLT(p,pp,walldomains,q)
    else:
        pgtw,pltw=False,False
    qp=getPreviousNodes(currentwall,outedges)
    if len(qp)>1:
        wgtp,wltp=isVarGTorLT(w,qp,walldomains,q)
    else:
        wgtp,wltp=False,False
    return wgtp,wltp,pgtw,pltw


def getChars(Z,previouswall,currentwall,nextwall,outedges,walldomains,varatwall):
    # Z contains the variable index and the values of variable at the previous, 
    # current, and next walls respectively. Given the graph labeled with walldomains, 
    # we find all possible behaviors of the variable at the current wall given the
    # trajectory defined by the previous and next walls.
    #
    # this algorithm works but is heinous to read; the only way I saw to make it shorter
    # is to do unnecessary calculations. This is important to avoid since the function
    # is inside a recursive call.
    #
    q,p,w,n=Z
    if p<w<n:
        chars = ['u']
    elif p>w>n:
        chars = ['d']
    elif q != varatwall:
        if p<w>n or p>w<n:
            chars=[]
        elif p<w==n or p==w<n:
            chars = ['u']
        elif p>w==n or p==w>n:
            chars = ['d']
        else: #p==w==n
            wgtp,wltp,pgtw,pltw = helper1(q,p,w,previouswall,currentwall,outedges,walldomains)
            wgtn,wltn,ngtw,nltw = helper2(q,w,n,nextwall,currentwall,outedges,walldomains)
            # print wltp
            if pgtw or wltp:
                # print ngtw,wltn
                if ngtw or wltn:
                    chars=[] 
                else:
                    chars=['d']
            elif pltw or wgtp:
                if nltw or wgtn:
                    chars=[]
                else:
                    chars=['u']
            elif ngtw or wltn:
                chars=['u']
            elif nltw or wgtn:
                chars=['d']
            else:
                chars=['d','u']
    else: #q==varatwall
        if p<w>n:
            chars=['M']
        elif p>w<n:
            chars=['m']
        elif p==w and w!=n:
            wgtp,wltp,pgtw,pltw = helper1(q,p,w,previouswall,currentwall,outedges,walldomains)
            if w>n:
                if wgtp or pltw:
                    chars=['M']
                elif wltp or pgtw:
                    chars=['d']
                else:
                    chars=['d','M']
            elif w<n:
                if wgtp or pltw:
                    chars=['u']
                elif wltp or pgtw:
                    chars=['m']
                else:
                    chars=['u','m']
        elif w==n and w!=p:
            wgtn,wltn,ngtw,nltw = helper2(q,w,n,nextwall,currentwall,outedges,walldomains)
            if p<w:
                if ngtw or wltn:
                    chars=['u']
                elif nltw or wgtn:
                    chars=['M']
                else:
                    chars=['u','M']
            elif p>w:
                if ngtw or wltn:
                    chars=['m']
                elif nltw or wgtn:
                    chars=['d']
                else:
                    chars=['d','m']
        else: #p==w==n and q==varatwall
            wgtp,wltp,pgtw,pltw = helper1(q,p,w,previouswall,currentwall,outedges,walldomains)
            wgtn,wltn,ngtw,nltw = helper2(q,w,n,nextwall,currentwall,outedges,walldomains)
            if pgtw or wltp:
                if ngtw or wltn:
                    chars=['m']
                elif nltw or wgtn:
                    chars=['d']
                else:
                    chars=['m','d']
            elif pltw or wgtp:
                if ngtw or wltn:
                    chars=['u']
                elif nltw or wgtn:
                    chars=['M']
                else:
                    chars=['M','u']
            elif ngtw or wltn:
                chars=['u','m']
            elif nltw or wgtn:
                chars=['d','M']
            else:
                chars=['d','M','u','m']
    return chars

def getChars2(Z,previouswall,currentwall,nextwall,outedges,walldomains,varatwall):
    # No extra info assumed
    #
    q,p,w,n=Z
    if p<w<n:
        chars = ['u']
    elif p>w>n:
        chars = ['d']
    elif q != varatwall:
        if p<w>n or p>w<n:
            chars=[]
        elif p<w==n or p==w<n:
            chars = ['u']
        elif p>w==n or p==w>n:
            chars = ['d']
        else: #p==w==n
            chars=['d','u']
    else: #q==varatwall
        if p<w>n:
            chars=['M']
        elif p>w<n:
            chars=['m']
        elif p==w>n:
            chars=['d','M']
        elif p==w<n:
            chars=['u','m']
        elif p<w==n:
            chars=['u','M']
        elif p>w==n:
            chars=['d','m']
        else: #p==w==n and q==varatwall
            chars=['d','M','u','m']
    return chars

def pathDependentStringConstruction(previouswall,wall,nextwall,walldomains,outedges,varatwall):
    # make a label for 'wall' that depends on where the path came from and where it's going
    if wall==nextwall: #if at steady state, do not label
        return []
    walllabels=['']
    Z=zip(range(len(walldomains[0])),walldomains[previouswall],walldomains[wall],walldomains[nextwall])
    while Z:
        chars=getChars(Z[0],previouswall,wall,nextwall,outedges,walldomains,varatwall)
        if chars:
            walllabels=[l+c for l in walllabels for c in chars]
            Z.pop(0)
        else:
            return []
    return walllabels

def getFirstwalls(firstpattern,allwalllabels):
    # Given the first word in the pattern, find the nodes in the graph that have 
    # this pattern for some path. Our searches will start at each of these nodes.
    return [k for k,wl in enumerate(allwalllabels) if firstpattern in wl]

def makeAllWallLabels(outedges,walldomains,varsaffectedatwall):
    inedges=[tuple([j for j,o in enumerate(outedges) if i in o]) for i in range(len(outedges))]
    allwalllabels=[]
    for k,(ie,oe) in enumerate(zip(inedges,outedges)):
        # if k==7:
        #     print ie
        #     print oe
        wl=[]
        for i,o in itertools.product(ie,oe):
            # if k==7:
            #     print i,o
            wl.extend(pathDependentStringConstruction(i,k,o,walldomains,outedges,varsaffectedatwall[k]))
        allwalllabels.append(list(set(wl)))
        # if k==7:
        #     print allwalllabels[-1]
        #     sys.exit()
    return allwalllabels



