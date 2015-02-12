import itertools
import sys

def getNextNodes(node,outedges):
    return outedges[node]

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

def infoFromEntranceWalls(q,wallval,wallind,outedges,walldomains):
    # is the wall <= or >= (or neither) all of its entrance walls?
    entrancewalls=getPreviousNodes(wallind,outedges)
    num_entrancewalls=len(entrancewalls)
    if num_entrancewalls>1:
        GT,LT=isVarGTorLT(wallval,entrancewalls,walldomains,q)
    else:
        GT,LT=False,False
    return GT,LT,num_entrancewalls

def infoFromExitWalls(q,wallval,wallind,outedges,walldomains):
    # is the wall <= or >= (or neither) all of its exit walls?
    exitwalls=getNextNodes(wallind,outedges)
    num_exitwalls=len(exitwalls)
    if num_exitwalls>1:
        GT,LT=isVarGTorLT(wallval,exitwalls,walldomains,q)
    else:
        GT,LT=False,False
    return GT,LT,num_exitwalls

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
            chars=[] # no extrema allowed
        elif p<w==n or p==w<n:
            chars = ['u']
        elif p>w==n or p==w>n:
            chars = ['d']
        elif p==w==n:
            prev_gt_out,prev_lt_out,num_out_prev=infoFromExitWalls(q,p,previouswall,outedges,walldomains)
            current_gt_in,current_lt_in,num_in_current=infoFromEntranceWalls(q,w,currentwall,outedges,walldomains)
            current_gt_out,current_lt_out,num_out_current=infoFromExitWalls(q,w,currentwall,outedges,walldomains)
            next_gt_in,next_lt_in,num_in_next=infoFromEntranceWalls(q,n,nextwall,outedges,walldomains)
            # note that there is extra information only if there are additional in- or out-edges
            # hence the checking of num_* > 1
            if num_out_prev==1 and num_in_current==1 and num_out_current==1 and num_in_next==1:
                chars=['d','u']
            elif (num_out_prev>1 or num_in_current>1) and (num_out_current>1 or num_in_next>1):
                if prev_gt_out or current_lt_in:
                    if next_gt_in or current_lt_out:
                        chars=[] # no extrema allowed
                    else:
                        chars=['d']
                elif prev_lt_out or current_gt_in:
                    if next_lt_in or current_gt_out:
                        chars=[] # no extrema
                    else:
                        chars=['u']
                elif next_gt_in or current_lt_out:
                    chars=['u']
                elif next_lt_in or current_gt_out:
                    chars=['d']
                else:
                    chars=['d','u']
            elif num_out_prev==1 and num_in_current==1:
                if next_gt_in or current_lt_out:
                    chars=['u']
                elif next_lt_in or current_gt_out:
                    chars=['d']
                else:
                    chars=['d','u']
            elif num_out_current==1 and num_in_next==1:
                if prev_gt_out or current_lt_in:
                    chars=['d']
                elif prev_lt_out or current_gt_in:
                    chars=['u']
                else:
                    chars=['d','u']
    elif q==varatwall:
        if p<w>n:
            chars=['M'] # extrema allowed
        elif p>w<n:
            chars=['m']
        elif p==w and w!=n:
            prev_gt_out,prev_lt_out,num_out_prev=infoFromExitWalls(q,p,previouswall,outedges,walldomains)
            current_gt_in,current_lt_in,num_in_current=infoFromEntranceWalls(q,w,currentwall,outedges,walldomains)
            if num_out_prev >1 or num_in_current>1:
                if w>n:
                    if current_gt_in or prev_lt_out:
                        chars=['M']
                    elif current_lt_in or prev_gt_out:
                        chars=['d']
                    else:
                        chars=['d','M']
                elif w<n:
                    if current_gt_in or prev_lt_out:
                        chars=['u']
                    elif current_lt_in or prev_gt_out:
                        chars=['m']
                    else:
                        chars=['u','m']
            elif num_out_prev==1 and num_in_current==1:
                if w>n:
                    chars=['d','M']
                elif w<n:
                    chars=['u','m']
        elif w==n and w!=p:
            current_gt_out,current_lt_out,num_out_current=infoFromExitWalls(q,w,currentwall,outedges,walldomains)
            next_gt_in,next_lt_in,num_in_next=infoFromEntranceWalls(q,n,nextwall,outedges,walldomains)
            if num_out_current>1 or num_in_next>1:
                if p<w:
                    if next_gt_in or current_lt_out:
                        chars=['u']
                    elif next_lt_in or current_gt_out:
                        chars=['M']
                    else:
                        chars=['u','M']
                elif p>w:
                    if next_gt_in or current_lt_out:
                        chars=['m']
                    elif next_lt_in or current_gt_out:
                        chars=['d']
                    else:
                        chars=['d','m']
            elif num_out_current==1 and num_in_next==1:
                if p<w:
                    chars=['u','M']
                elif p>w:
                    chars=['d','m']
        elif p==w==n:
            prev_gt_out,prev_lt_out,num_out_prev=infoFromExitWalls(q,p,previouswall,outedges,walldomains)
            current_gt_in,current_lt_in,num_in_current=infoFromEntranceWalls(q,w,currentwall,outedges,walldomains)
            current_gt_out,current_lt_out,num_out_current=infoFromExitWalls(q,w,currentwall,outedges,walldomains)
            next_gt_in,next_lt_in,num_in_next=infoFromEntranceWalls(q,n,nextwall,outedges,walldomains)
            if num_out_prev==1 and num_in_current==1 and num_out_current==1 and num_in_next==1:
                chars=['d','M','u','m']
            elif (num_out_prev>1 or num_in_current>1) and (num_out_current>1 or num_in_next>1):
                if prev_gt_out or current_lt_in:
                    if next_gt_in or current_lt_out:
                        chars=['m']
                    elif next_lt_in or current_gt_out:
                        chars=['d']
                    else:
                        chars=['m','d']
                elif prev_lt_out or current_gt_in:
                    if next_gt_in or current_lt_out:
                        chars=['u']
                    elif next_lt_in or current_gt_out:
                        chars=['M']
                    else:
                        chars=['M','u']
                elif next_gt_in or current_lt_out:
                    chars=['u','m']
                elif next_lt_in or current_gt_out:
                    chars=['d','M']
                else:
                    chars=['d','M','u','m']
            elif num_out_prev==1 and num_in_current==1:
                if next_gt_in or current_lt_out:
                    chars=['u','m']
                elif next_lt_in or current_gt_out:
                    chars=['d','M']
                else:
                    chars=['d','M','u','m']
            elif num_out_current==1 and num_in_next==1:
                if prev_gt_out or current_lt_in:
                    chars=['d','m']
                elif prev_lt_out or current_gt_in:
                    chars=['u','M']
                else:
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
    # step through every wall in the list 
    # construct the wall label for every permissible triple (in-edge, wall, out-edge)
    inedges=[tuple([j for j,o in enumerate(outedges) if i in o]) for i in range(len(outedges))]
    allwalllabels=[]
    for k,(ie,oe) in enumerate(zip(inedges,outedges)):
        wl=[]
        for i,o in itertools.product(ie,oe):
            wl.extend(pathDependentStringConstruction(i,k,o,walldomains,outedges,varsaffectedatwall[k]))
        allwalllabels.append(list(set(wl)))
    return allwalllabels



