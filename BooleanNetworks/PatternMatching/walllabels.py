import itertools
import sys

def infoFromWalls(q,wallval,walls,num_walls,walldomains):
    if num_walls>1:
        gt=True
        lt=True
        nz=False
        for k in walls:
            d=wallval-walldomains[k][q]
            if d>0:
                nz=True
                lt=False
            elif d<0:
                nz=True
                gt=False
        GT,LT=gt*nz,lt*nz
    else:
        GT,LT=False,False
    return GT,LT

def getChars(Z,previouswall,currentwall,nextwall,outedges,walldomains,varatwall,inedges):
    # Z contains the variable index and the values of variable at the previous, 
    # current, and next walls respectively. Given the graph labeled with walldomains, 
    # we find all possible behaviors of the variable at the current wall given the
    # trajectory defined by the previous and next walls.
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
            prev_out=outedges[previouswall]
            num_out_prev=len(prev_out)
            prev_gt_out,prev_lt_out=infoFromWalls(q,p,prev_out,num_out_prev,walldomains)
            curr_in=inedges[currentwall]
            num_in_current=len(curr_in)
            current_gt_in,current_lt_in=infoFromWalls(q,w,curr_in,num_in_current,walldomains)
            curr_out=outedges[currentwall]
            num_out_current=len(curr_out)
            current_gt_out,current_lt_out=infoFromWalls(q,w,curr_out,num_out_current,walldomains)
            next_in=inedges[nextwall]
            num_in_next=len(next_in)
            next_gt_in,next_lt_in=infoFromWalls(q,n,next_in,num_in_next,walldomains)
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
            prev_out=outedges[previouswall]
            num_out_prev=len(prev_out)
            prev_gt_out,prev_lt_out=infoFromWalls(q,p,prev_out,num_out_prev,walldomains)
            curr_in=inedges[currentwall]
            num_in_current=len(curr_in)
            current_gt_in,current_lt_in=infoFromWalls(q,w,curr_in,num_in_current,walldomains)
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
            curr_out=outedges[currentwall]
            num_out_current=len(curr_out)
            current_gt_out,current_lt_out=infoFromWalls(q,w,curr_out,num_out_current,walldomains)
            next_in=inedges[nextwall]
            num_in_next=len(next_in)
            next_gt_in,next_lt_in=infoFromWalls(q,n,next_in,num_in_next,walldomains)
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
            prev_out=outedges[previouswall]
            num_out_prev=len(prev_out)
            prev_gt_out,prev_lt_out=infoFromWalls(q,p,prev_out,num_out_prev,walldomains)
            curr_in=inedges[currentwall]
            num_in_current=len(curr_in)
            current_gt_in,current_lt_in=infoFromWalls(q,w,curr_in,num_in_current,walldomains)
            curr_out=outedges[currentwall]
            num_out_current=len(curr_out)
            current_gt_out,current_lt_out=infoFromWalls(q,w,curr_out,num_out_current,walldomains)
            next_in=inedges[nextwall]
            num_in_next=len(next_in)
            next_gt_in,next_lt_in=infoFromWalls(q,n,next_in,num_in_next,walldomains)
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

def pathDependentStringConstruction(previouswall,wall,nextwall,walldomains,outedges,varatwall,inedges):
    # make a label for 'wall' that depends on where the path came from and where it's going
    if wall==nextwall: #if at steady state, do not label
        return []
    walllabels=['']
    Z=zip(range(len(walldomains[0])),walldomains[previouswall],walldomains[wall],walldomains[nextwall])
    for z in Z:
        chars=getChars(z,previouswall,wall,nextwall,outedges,walldomains,varatwall,inedges)
        if chars:
            walllabels=[l+c for l in walllabels for c in chars]
        else:
            return []
    return walllabels

def getFirstAndNextWalls(firstpattern,triples,sortedwalllabels):
    # Given the first word in the pattern, find the nodes in the graph that have 
    # this pattern for some path. Our searches will start at each of these nodes, 
    # and proceed to the next nodes found in this algorithm.
    startwallpairs=[]
    for k,l in enumerate(triples):
        for j,t in enumerate(l):
            if firstpattern in sortedwalllabels[k][j]:
                startwallpairs.append(t[1:])
    return list(set(startwallpairs))

def makeAllTriples(outedges,walldomains,varsaffectedatwall):
    # step through every wall in the list 
    # make inedges
    inedges=[tuple([j for j,o in enumerate(outedges) if node in o]) for node in range(len(outedges))]   
    # construct the wall label for every permissible triple (in-edge, wall, out-edge)
    allwalllabels=[]
    triples=[]
    # trip2=[]
    unfoldedwalllabels=[]
    for k,(ie,oe) in enumerate(zip(inedges,outedges)):
        wl=[]
        uwl=[]
        t=[]
        # t2=[]
        for i,o in itertools.product(ie,oe):
            pds=pathDependentStringConstruction(i,k,o,walldomains,outedges,varsaffectedatwall[k],inedges)
            wl.extend(pds)
            # t2.extend((i,k,o))
            uwl.append(pds)
            t.append((i,k,o))
        allwalllabels.append(wl)
        # trip2.append(t2)
        unfoldedwalllabels.extend(uwl)
        triples.extend(t)
    # now sort the triples and make a sorted wall label list too
    sorttriples=sorted(zip(triples,range(len(triples))))
    triples,sortedinds=zip(*sorttriples)
    sortedwalllabels=[unfoldedwalllabels[j] for j in sortedinds]
    collapsedtriples=[]
    collapsedsortedwalls=[]
    i=0   
    t = triples[0] 
    for m in range(len(allwalllabels)): 
        ct=[]      
        cw=[] 
        while t[0]==m:
            ct.append(t)
            cw.append(sortedwalllabels[i])
            i+=1
            if i <len(triples):
                t = triples[i] 
            else:
                t=[-1]
        collapsedtriples.append(ct)
        collapsedsortedwalls.append(cw)
    paramDict={'triples':collapsedtriples,'walllabels_previous':collapsedsortedwalls,'walllabels_current':allwalllabels}
    return paramDict

if __name__=='__main__':
    import testcases as tc #pragma: no cover
    import preprocess as PP #pragma: no cover
    inds,outedges,walldomains,varsaffectedatwall,allwalllabels,inedges,triples,sortedwalllabels= PP.filterAllTriples(*tc.test0()) #pragma: no cover
    N,wld=makeDictOfWallLabels(outedges,walldomains,varsaffectedatwall) #pragma: no cover


