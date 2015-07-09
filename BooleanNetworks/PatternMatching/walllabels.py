import itertools
import sys

def getChars(isvaratwall,(p,c,n)):
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

def infoFromWalls(varind,varval,wallinds,walldomains):
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

def getAdditionalWallInfo(varind,(prevval,currval,nextval),(prev_out,curr_in,curr_out,next_in),walldomains):
    prev_gt_out,prev_lt_out=infoFromWalls(varind,prevval,prev_out,walldomains)
    curr_gt_in,curr_lt_in=infoFromWalls(varind,currval,curr_in,walldomains)
    curr_gt_out,curr_lt_out=infoFromWalls(varind,currval,curr_out,walldomains)
    next_gt_in,next_lt_in=infoFromWalls(varind,nextval,next_in,walldomains)
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

def pathDependentLabelConstruction(triple,inandoutedges,walldomains,varatwall):
    # make a label for the given triple
    if triple[1]==triple[2]: # can't handle steady states
        raise RunTimeError('Debug: Wall has a self-loop.')
    walllabels=['']
    # for every variable find allowable letters for triple
    for varind in range(len(walldomains[0])): 
        # try simple algorithm first
        isvaratwall = varind==varatwall
        varvalues=tuple([walldomains[k][varind] for k in triple])
        chars=getChars(isvaratwall,varvalues) 
        if chars:
            # simple algorithm worked, skip complex algorithm
            pass            
        elif isvaratwall:
            # use extra information to get the characters when extrema are allowed
            chars=getCharsExtrema(*getAdditionalWallInfo(varind,varvalues,inandoutedges,walldomains))
        else:
            # use extra information to get the characters when extrema are not allowed
            chars=getCharsNoExtrema(*getAdditionalWallInfo(varind,varvalues,inandoutedges,walldomains))
        # make every combination of characters in the growing labels
        walllabels=[l+c for l in walllabels for c in chars]
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
            pdlc=pathDependentLabelConstruction(triple,inandoutedges,walldomains,varatwall)
            key=triple[:-1]
            value=(triple[-1],pdlc)
            if key in wallinfo:
                wallinfo[key].append(value)
            else:
                wallinfo[key]=[value]
    return wallinfo


