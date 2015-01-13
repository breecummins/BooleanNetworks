import itertools
from translatewallstostrings2 import filterBoundaryWallsAndSteadyStates

def isVarGTorLT(nodeval,nodelist,walldomains,varind):
    node_gt=True
    node_lt=True
    for k in nodelist:
        W=walldomains[k][varind]
        if nodeval>W:
            node_lt=False
        elif nodeval<W:
            node_gt=False
    return node_gt,node_lt


def pathDependentStringConstruction(previouswall,wall,nextwall,walldomains,outedges):
    # this works but is heinous; to shorten it requires more computation, which is important to avoid since this function is called many times
    walllabels=['']
    for q,(p,w,n) in enumerate(zip(walldomains[previouswall],walldomains[wall],walldomains[nextwall])):
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
        addition=[[ l+c for l in walllabels] for c in chars]
        walllabels=[b for a in addition for b in a]
    return walllabels

def repeatingLoop(match):
    N=len(match)
    if len(set(match)) == N:
        return False
    else:
        for n in range(1,N/2+1):
            if match[N-n:N] == match[N-2*n:N-n]:
                return True
        return False

def getNextNodes(node,outedges):
    return [o for o in outedges[node]]

def getPreviousNodes(node,outedges):
    return [j for j,o in enumerate(outedges) if node in o ]

def recursePattern(startnode,match,matches,patterns,previouspattern,walllabels,pDict):
    if len(match) >= pDict['lenpattern'] and pDict['stop'] in walllabels: # the first condition requires all walls to be present in the pattern. A way to ensure this is to have only extrema in the pattern - i.e. every p in pattern has exactly one 'm' or 'M'. This is why this condition exists in the input sanity check.
        matches.append(match)
        return matches
    else:
        for p,P in patterns:
            for n in getNextNodes(startnode,pDict['interioroutedges']):  #only interior walls allowed in path
            	interior_n = n
            	n = pDict['interiorwallinds'][n] # change interior index to full index for use in creating wall label in pathDependentStringConstruction 
                if len(match) == 1 or set(previouspattern).intersection(pathDependentStringConstruction(match[-2],match[-1],n,pDict['walldomains'])): # consistency check to catch false positives
                    walllabels = [w for q in getNextNodes(interior_n,pDict['interioroutedges']) for w in pathDependentStringConstruction(match[-1],n,q,pDict['walldomains']) ]
                    if p in walllabels: # if we hit the next pattern element, reduce pattern by one
                        # WE MAY GET FALSE POSITIVES WITHOUT THE CONSISTENCY CHECK ABOVE (this is because we have to pick the right q in the next step)
                        matches=recursePattern(n,match+[n],matches,patterns[1:],patterns[0][1],walllabels,pDict)
                    elif set(walllabels).intersection(P) and not repeatingLoop(match+[n]): # if we hit an intermediate node, call pattern without reduction provided there isn't a repeating loop; note: checking repeatingLoop over and over again is slow, but I haven't found a better method
                        matches=recursePattern(n,match+[n],matches,patterns,patterns[0][1],walllabels,pDict)
        return matches

def labelOptions(p):
    # there is exactly one 'm' or 'M' in p
    if 'm' in p:
        return [p,p.replace('m','d')]
    elif 'M' in p:
        return [p,p.replace('M','u')]

def sanitycheck(pattern):
    # make sure inputs meet requirements of algorithm
    if not pattern:
        return "None. Pattern is empty."
    notextrema = [p for p in pattern if not set(p).intersection(['m','M'])]
    if notextrema:
        return "None. Pattern element(s) {} are not extrema. An 'm' or 'M' is required in every element.".format(notextrema)
    return "sane"  

def matchPattern(pattern,walldomains,outedges,suppress=0):
    '''
    Matches pattern in a labeled graph with edges in outedges and labels in walllabels. The pattern is 
    described in terms of walllabels, and a pattern label of the wrong type will return no match. If there
    is a match to the pattern, the paths that respect it will be returned in terms of wall number (the index
    of outedges).

    outedges: list of tuples of integers, index is wall number
    pattern: list of uniform-length strings of labels from the alphabet ('u','d','m','M'); exactly one 'm' or 'M' REQUIRED per string; patterns containing exactly repeating sequences will not be found if the same walls must be traversed to match the pattern
    suppress: 0 means give information about cyclic or acyclic pattern request, 1 means suppress it

    No unit tests currently available.

    See notes for meaning of alphabet. Briefly, 'uMdd' means that the first variable is increasing (up), the 
    second variable is at a maximum (Max), and the third and fourth variables are decreasing (down). The character
    'm' means a variable is at a minimum (min). There can be at most one 'm' or 'M' at each wall, because we 
    assume that the input graph arises from a switching network where each regulation event occurs at a unique 
    threshold.

    '''
    # sanity check the input 
    S=sanitycheck(pattern)
    if S !="sane":
        return S
    # give information about the type of pattern received
    if not suppress:
        if pattern[0] != pattern[-1]:
            print('Seeking acyclic path.')
        else:
            print('Seeking cyclic path. Acyclic paths that match the pattern may exist if wall labels are not unique, but these will not be returned.')
    # calculate all possible starting nodes 
    R=range(len(outedges))
    inedges=[tuple([j for j,o in enumerate(outedges) if i in o ]) for i in R]
    firstwalls=[]
    for k in R:
        ie=inedges[k]
        oe=outedges[k]
        wl=[]
        for i,o in itertools.product(ie,oe):
            wl.extend(pathDependentStringConstruction(i,k,o,walldomains))
        if pattern[0] in wl:
            firstwalls.append(k)
    # return trivial length one patterns
    if len(pattern)==1:
        return [ (w,) for w in firstwalls ]
    # get interior walls
    interiorwallinds,interioroutedges=filterBoundaryWallsAndSteadyStates(outedges)
    # pre-cache intermediate nodes that may exist in the wall graph (saves time in recursive call)
    patternoptions=[labelOptions(p) for p in pattern[1:]]
    patternParams = zip(pattern[1:],patternoptions)
    paramDict = {'walldomains':walldomains,'interioroutedges':interioroutedges,'interiorwallinds':interiorwallinds,'stop':pattern[-1],'lenpattern':len(pattern)}
    # find matches
    results=[]
    for w in firstwalls:
        R = recursePattern(w,[w],[],patternParams,[],[],paramDict) # seek match starting at w
        results.extend(list(set(tuple(l) for l in R if l))) # pull out the unique paths found
    # prep matches for return
    if results:
        results = list(set(results))
        if pattern[0]==pattern[-1]:
            # remove acyclic paths from a cyclic search
            results = [r for r in results if r[0]==r[-1]]
        return results
    else:
        return "None. No results found."
