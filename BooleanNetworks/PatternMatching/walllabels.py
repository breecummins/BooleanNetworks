import itertools
import sys

def infoFromWalls(q,wallval,walls,num_walls,walldomains):
    if num_walls>1:
        greaterthan=True
        lessthan=True
        nonzero=False
        for k in walls:
            d=wallval-walldomains[k][q]
            if d>0:
                nonzero=True
                lessthan=False
            elif d<0:
                nonzero=True
                greaterthan=False
        GT,LT=greaterthan*nonzero,lessthan*nonzero
    else:
        GT,LT=False,False
    return GT,LT

def infoFromWalls2(varind,varval,wallinds,walldomains):
    # We want the difference between the value at the current wall, varval,
    # and the value at all adjacent walls to have the same sign (or zero,
    # but not all can be zero).
    # return isgreaterthan, islessthan 
    signs = [cmp(varval - walldomains[k][varind],0) for k in wallinds]
    if set([-1,1]).issubset(signs):
        return False,False
    elif set([1]).issubset(signs):
        return True,False
    elif set([-1]).issubset(signs):
        return False,True
    else:
        return False,False

def getChars(Z,(previouswall,currentwall,nextwall),inedges,outedges,walldomains,varatwall):
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

def getChars2(isvaratwall,(p,c,n)):
    chars=[]
    if p<c<n:
        chars = ['u']
    elif p>c>n:
        chars = ['d']
    elif isvaratwall: # extrema allowed
        if p<c>n:
            chars=['M'] 
        elif p>c<n:
            chars=['m']
    elif not isvaratwall: # extrema not allowed
        if p<c>n or p>c<n:
            raise RunTimeError('Debug: Extrema are not allowed for variables that are not affected at threshold.')
        elif p<c==n or p==c<n:
            chars = ['u']
        elif p>c==n or p==c>n:
            chars = ['d']
    return chars

def getAdditionalWallInfo(varind,(prevval,currval,nextval),(prev_out,curr_in,curr_out,next_in),walldomains):
    prev_gt_out,prev_lt_out=infoFromWalls2(varind,prevval,prev_out,walldomains)
    curr_gt_in,curr_lt_in=infoFromWalls2(varind,currval,curr_in,walldomains)
    curr_gt_out,curr_lt_out=infoFromWalls2(varind,currval,curr_out,walldomains)
    next_gt_in,next_lt_in=infoFromWalls2(varind,nextval,next_in,walldomains)
    return prev_gt_out,prev_lt_out,curr_gt_in,curr_lt_in,curr_gt_out,curr_lt_out,next_gt_in,next_lt_in

def getCharsExtrema(prev_gt_out,prev_lt_out,curr_gt_in,curr_lt_in,curr_gt_out,curr_lt_out,next_gt_in,next_lt_in):
    if (prev_gt_out or curr_lt_in) and (next_gt_in or curr_lt_out):
        chars=['m'] 
    elif (prev_lt_out or curr_gt_in) and (next_lt_in or curr_gt_out):
        chars=['M'] 
    elif prev_gt_out or curr_lt_in:  
        chars=['m','d']
    elif next_lt_in or curr_gt_out:
        chars=['M','d']
    elif prev_lt_out or curr_gt_in:
        chars=['M','u']
    elif next_gt_in or curr_lt_out:
        chars=['m','u']
    else:
        chars=['M','m','d','u']
    return chars

def getCharsNoExtrema(prev_gt_out,prev_lt_out,curr_gt_in,curr_lt_in,curr_gt_out,curr_lt_out,next_gt_in,next_lt_in):
    if ( (prev_gt_out or curr_lt_in) and (next_gt_in or curr_lt_out) ) or ( (prev_lt_out or curr_gt_in) and (next_lt_in or curr_gt_out) ):
        raise RunTimeError('Debug: Extrema are not allowed for variables that are not affected at threshold.')
    elif prev_gt_out or curr_lt_in or next_lt_in or curr_gt_out:
        chars=['d']
    elif prev_lt_out or curr_gt_in or next_gt_in or curr_lt_out:
        chars=['u']
    else:
        chars=['d','u']
    return chars

def pathDependentLabelConstruction2(triple,inandoutedges,walldomains,varatwall):
    # make a label for 'wall' that depends on where the path came from and where it's going
    if triple[1]==triple[2]: #if at steady state, do not label
        raise RunTimeError('Debug: Wall has a self-loop.')
    walllabels=['']
    for varind in range(len(walldomains[0])): # for every variable find allowable letters for (prev,curr,next)
        isvaratwall = varind==varatwall
        varvalues=tuple([walldomains[k][varind] for k in triple])
        chars=getChars2(isvaratwall,varvalues) #simple algorithm
        if chars:
            pass            
        elif isvaratwall:
            chars=getCharsExtrema(*getAdditionalWallInfo(varind,varvalues,inandoutedges,walldomains))
        else:
            chars=getCharsNoExtrema(*getAdditionalWallInfo(varind,varvalues,inandoutedges,walldomains))
        walllabels=[l+c for l in walllabels for c in chars]
    return walllabels


def pathDependentLabelConstruction((previouswall,wall,nextwall),inedges,outedges,walldomains,varatwall):
    # make a label for 'wall' that depends on where the path came from and where it's going
    if wall==nextwall: #if at steady state, do not label
        return []
    walllabels=['']
    Z=zip(range(len(walldomains[0])),walldomains[previouswall],walldomains[wall],walldomains[nextwall])
    for z in Z:
        chars=getChars(z,(previouswall,wall,nextwall),inedges,outedges,walldomains,varatwall)
        if chars:
            walllabels=[l+c for l in walllabels for c in chars]
        else:
            return []
    return walllabels

def getFirstAndNextWalls(firstpattern,wallinfo):
    # Given the first word in the pattern, find the nodes in the graph that have 
    # this pattern for some path. Our searches will start at each of these nodes, 
    # and proceed to the next nodes found in this algorithm.
    startwallpairs=[]
    for (lastwall,currentwall), list_of_labels in wallinfo.iteritems():
        for (nextwall,labels) in list_of_labels:
            if firstpattern in labels:
                startwallpairs.append((currentwall,nextwall))
    return list(set(startwallpairs))


def makeWallInfo(outedges,walldomains,varsaffectedatwall):
    # make inedges
    inedges=[tuple([j for j,o in enumerate(outedges) if node in o]) for node in range(len(outedges))]   
    # make every triple and the list of associated wall labels; store in dict indexed by (inedge,wall)
    wallinfo={}
    for currentwall,(ie,oe) in enumerate(zip(inedges,outedges)):
       for previouswall,nextwall in itertools.product(ie,oe):
            # construct the wall label for every permissible triple
            triple=(previouswall,currentwall,nextwall)
            inandoutedges=(outedges[previouswall],inedges[currentwall],outedges[currentwall],inedges[nextwall])
            varatwall=varsaffectedatwall[currentwall]
            pdlc=pathDependentLabelConstruction2(triple,inandoutedges,walldomains,varatwall)
            # pdlc=pathDependentLabelConstruction(triple,inedges,outedges,walldomains,varatwall)
            key=triple[:-1]
            value=(triple[-1],pdlc)
            if key in wallinfo:
                wallinfo[key].append(value)
            else:
                wallinfo[key]=[value]
    return wallinfo

if __name__=='__main__':
    import testcases as tc #pragma: no cover
    import preprocess as PP #pragma: no cover
    inds,outedges,walldomains,varsaffectedatwall,allwalllabels,inedges,triples,sortedwalllabels= PP.filterAllTriples(*tc.test0()) #pragma: no cover
    N,wld=makeDictOfWallLabels(outedges,walldomains,varsaffectedatwall) #pragma: no cover


