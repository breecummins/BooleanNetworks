import itertools, sys

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
        if p<w==n:
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

def repeatingLoop(match):
    # see if the match has a repeating loop inside it
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
    return [j for j,o in enumerate(outedges) if node in o]

def recursePattern(startnode,match,matches,patterns,previouspattern,walllabels,pDict):
    if len(match) >= pDict['lenpattern'] and pDict['stop'] in walllabels: # the first condition requires all walls to be present in the pattern. A way to ensure this is to have only extrema in the pattern - i.e. every p in pattern has exactly one 'm' or 'M'. This is why this condition exists in the input sanity check.
        matches.append(match)
        return matches
    else:
        for p,P in patterns:
            for n in getNextNodes(startnode,pDict['outedges']):  # every wall has an outgoing edge by graph construction
                if len(match) == 1 or set(previouspattern).intersection(pathDependentStringConstruction2(match[-2],match[-1],n,pDict['walldomains'],pDict['varsaffectedatwall'][match[-1]])): # consistency check to catch false positives
                    walllabels = [w for q in getNextNodes(n,pDict['outedges']) for w in pathDependentStringConstruction2(match[-1],n,q,pDict['walldomains'],pDict['varsaffectedatwall'][n]) ]
                    if p in walllabels: # if we hit the next pattern element, reduce pattern by one
                        # WE MAY GET FALSE POSITIVES WITHOUT THE CONSISTENCY CHECK ABOVE (this is because we have to pick the right q in the next step)
                        matches=recursePattern(n,match+[n],matches,patterns[1:],patterns[0][1],walllabels,pDict)
                    elif set(walllabels).intersection(P) and not repeatingLoop(match+[n]): # if we hit an intermediate node, call pattern without reduction provided there isn't a repeating loop 
                        matches=recursePattern(n,match+[n],matches,patterns,patterns[0][1],walllabels,pDict)
        return matches

def labelOptions(p):
    # Construct the intermediate nodes that are allowed for 
    # each word (p) in pattern. This algorithm depends on the
    # fact that there is exactly one 'm' or 'M' in each word.
    if 'm' in p:
        return [p,p.replace('m','d')]
    elif 'M' in p:
        return [p,p.replace('M','u')]

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

def cycleInfo(pattern,cycliconly):
    # Potentially useful message for user.
    if pattern[0] != pattern[-1]:
        return 'Seeking acyclic paths.'
    else:
        if cycliconly:
            return 'Seeking cyclic paths.'
        else:
            return('Seeking both cyclic and acyclic paths.')

def sanityCheck(pattern):
    # Make sure the input pattern meets the requirements of the algorithm.
    if not pattern:
        return "None. Pattern is empty."
    notextrema = [p for p in pattern if not set(p).intersection(['m','M'])]
    if notextrema:
        return "None. Pattern element(s) {} are not extrema. An 'm' or 'M' is required in every element.".format(notextrema)
    return "sane"  

def matchPattern(pattern,walldomains,outedges,varsaffectedatwall,suppresscycleinfo=0,cycliconly=1):
    '''
    This function finds paths in a directed graph that are consistent with a target pattern. The nodes
    of the directed graph are called walls, and each node is associated with a wall label (in walldomains)
    and a wall number (the index of the label in walldomains). The outgoing edges of a node with wall
    number w are stored in outedges at index w. Each element of outedges is a collection of wall numbers.
    The pattern is a sequence of words from the alphabet ('u','d','m','M'). The labels in walldomains
    will be transformed in a path-dependent manner into words of the same type. The paths in the graph 
    that have word labels that match the pattern will be returned as sequences of wall numbers.

    pattern: list of uniform-length words from the alphabet ('u','d','m','M'); exactly one 'm' or 'M' REQUIRED per string; patterns containing exactly repeating sequences will not be found if the same walls must be traversed to match the pattern
    walldomains: list of tuples of floats from data using translatewallstostrings2, index is wall number
    outedges: list of tuples of integers from data using translatewallstostrings2, index is wall number
    varsaffectedatwall:
    suppresscycleinfo: default 0 means give information about cyclic or acyclic pattern request, 1 means suppress it
    cycliconly: only applies when the first and last elements of pattern agree; default 1 
        means return only cyclic paths, 0 means return all matching paths 

    See patternmatch_unittests2.py for examples of function calls.

    See notes for the meaning of alphabet. Briefly, 'uMdd' means that the first variable is increasing 
    (up), the second variable is at a maximum (Max), and the third and fourth variables are decreasing 
    (down). The character 'm' means a variable is at a minimum (min). There can be at most one 'm' or 
    'M' at each wall, because we assume that the input graph arises from a switching network where each
    regulation event occurs at a unique threshold.

    '''
    # sanity check the input, abort if insane 
    S=sanityCheck(pattern)
    if S != "sane":
        return S
    # give information about the type of pattern received
    if not suppresscycleinfo:
        print cycleInfo(pattern,cycliconly)
    # find all possible starting nodes for a matching path
    firstwalls=getFirstwalls(pattern[0],outedges,walldomains,varsaffectedatwall)
    # return trivial length one patterns
    if len(pattern)==1:
        return [ (w,) for w in firstwalls ]
    # pre-cache intermediate nodes that may exist in the wall graph (saves time in recursive call)
    patternoptions=[labelOptions(p) for p in pattern[1:]]
    patternParams = zip(pattern[1:],patternoptions)
    paramDict = {'walldomains':walldomains,'outedges':outedges,'stop':pattern[-1],'lenpattern':len(pattern),'varsaffectedatwall':varsaffectedatwall}
    # find matches
    results=[]
    print "All first walls {}".format(firstwalls)
    for w in firstwalls:
        print "First wall {}".format(w)
        sys.stdout.flush()
        R = recursePattern(w,[w],[],patternParams,[],[],paramDict) # seek match starting at w
        results.extend([tuple(l) for l in R if l]) # pull out nonempty paths
    # prep matches for return
    if results:
        results = list(set(results)) # get unique paths
        if cycliconly and pattern[0]==pattern[-1]:
            results = [r for r in results if r[0]==r[-1]] # remove acyclic paths from a cyclic search
        return results
    else:
        return "None. No results found."

def callPatternMatch(basedir='',message=''):
    if message:
        print "-"*len(message)
        print message
        print "-"*len(message)
    patterns,walldomains,outedges,varsaffectedatwall=pp.makeAll(basedir+'outEdges.txt',basedir+'walls.txt',basedir+'variables.txt',basedir+'equations.txt',basedir+'patterns.txt') 
    inds=[141, 150, 161, 170, 179]  
    inds=[10, 20, 30, 40, 50]
    inds=[549, 553, 558, 562, 567, 571, 578, 580, 1029, 1038, 1047]
    inds=[197, 205, 213, 221, 245, 246, 253, 254, 333, 341, 349, 357, 366, 374]
    inds=[297, 306, 315, 324]
    for pattern in patterns:
        print pattern
        for i in inds:
            print (varsaffectedatwall[i],walldomains[i])
        print matchPattern(pattern, walldomains,outedges,varsaffectedatwall)




if __name__=='__main__':
    # walldomains=[(0,0.5),(0,1.5),(0.5,0),(0.5,1),(0.5,2),(1,0.5),(1,1.5),(1.5,0),(1.5,1),(1.5,2),(2,0.5),(2,1.5),(2.5,0),(2.5,1),(2.5,2),(3,0.5),(3,1.5)]
    # outedges=[(5,),(3,),(5,),(5,),(3,),(10,),(3,),(10,),(10,),(6,),(13,),(6,8),(13,),(11,),(11,),(13,),(11,)]
    # testStringConstruction(walldomains,outedges)

    # walldomains=[(0,0.5),(0,1.5),(0.5,0),(0.5,1),(0.5,2),(1,0.5),(1,1.5),(1.5,0),(1.5,1),(1.5,2),(2,0.5),(2,1.5),(2.5,0),(2.5,1),(2.5,2),(3,0.5),(3,1.5),(0.5,0.5)]
    # outedges=[(17,),(3,),(17,),(17,),(3,),(10,17),(3,),(10,),(10,),(6,),(13,),(6,8),(13,),(11,),(11,),(13,),(11,),(17,)]
    # testStringConstruction(walldomains,outedges)

    # Arnaud's simulation data
    import prepforpatternmatch as pp
    import os


    basedir=os.path.expanduser('~/ProjectData/DatabaseSimulations/5D_cycle_1/MGCC_14419/')  
    callPatternMatch(basedir,'5D Cycle 1, MGCC 14419')

    # # pattern=['Mud','dum','dMu','mdu','udM','umd','Mud'] # x max, y min, z max, x min, y max, z min; explicitly calculated, should be there; NOTE THAT Y AND Z are swapped.

    basedir=os.path.expanduser('~/ProjectData/DatabaseSimulations/3D_Example/MGCC_5/')    
    callPatternMatch(basedir,'3D Example, MGCC 5')

    # pattern=['uum','Muu','dMu','ddM','mdd','umd','uum'] # all maxes in order X1 X2 X3, then all mins in same order

    # The variables.txt file for 3D Cycle 1 may be wrong. I MADE IT UP as a placeholder until
    # I hear from Arnaud
    basedir=os.path.expanduser('~/ProjectData/DatabaseSimulations/3D_Cycle_1_Data/MGCC_30/')    
    callPatternMatch(basedir,'3D Cycle 1, MGCC 30')

    basedir=os.path.expanduser('~/ProjectData/DatabaseSimulations/3D_Cycle_1_Data/MGCC_45/')    
    callPatternMatch(basedir,'3D Cycle 1, MGCC 45')

    # pattern=['Muuuu','dMuuu','ddMuu','dddMu','ddddM','mdddd','umddd','uumdd','uuumd','uuuum','Muuuu'] # maxes in order X Y1 Y2 Y3 Z, then mins in same order
    # pattern=['Muuuu','dMuuu','ddMuu','ddduM','dddMd','mdddd','umddd','uumdd','uuudm','uuumu','Muuuu'] # maxes in order X Y1 Y2 Z Y3, then mins in same order
    # pattern=['uuuum','uuuMu','uMudu','Mdudu','ddMdu','ddddM','dddmd','mddud','umdud','uumud','uuuum']  
    # pattern=['uuuum','uuuMu','uMudu','Mdudu','ddMdu','ddddM','dddmd','dmdud','mudud','uumud','uuuum']  
    # pattern=['uuuMu','uuudm','uMudu','Mdudu','ddMdu','dddmu','ddduM','dmdud','mudud','uumud','uuuum'] 
    # pattern=['uuumu','uMuuu','Mduuu','dduuM','ddMud','dddMd','mdddd','umddd','uuddm','uumdu','uuumu'] 
    # pattern=['Muuuu','duuMu','duudM']

    # print "-------------------"
    # print "5D Model B1, MGCC 1"
    # print "-------------------"
    # basedir=os.path.expanduser('~/ProjectData/DatabaseSimulations/5D_ModelB1_Data/MGCC_1/')
    # walldomains=fp.parseWalls(basedir+'walls.txt')
    # outedges=fp.parseOutEdges(basedir+'outEdges.txt')
    # print matchPattern(pattern, walldomains,outedges)
   
    # print "--------------------"
    # print "5D Model B1, MGCC 188"
    # print "--------------------"
    # basedir=os.path.expanduser('~/ProjectData/DatabaseSimulations/5D_ModelB1_Data/MGCC_188/')
    # walldomains=fp.parseWalls(basedir+'walls.txt')
    # outedges=fp.parseOutEdges(basedir+'outEdges.txt')
    # print matchPattern(pattern, walldomains,outedges)

    # print "---------------------"
    # print "5D Model B1, MGCC 522"
    # print "---------------------"
    # basedir=os.path.expanduser('~/ProjectData/DatabaseSimulations/5D_ModelB1_Data/MGCC_522/')
    # walldomains=fp.parseWalls(basedir+'walls.txt')
    # outedges=fp.parseOutEdges(basedir+'outEdges.txt')
    # print matchPattern(pattern, walldomains,outedges)

