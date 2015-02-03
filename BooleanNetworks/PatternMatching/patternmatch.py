import sys
import walllabels as WL
from preprocess import preprocess

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

def recursePattern(startnode,match,matches,patterns,previouspattern,walllabels,pDict):
    if len(match) >= pDict['lenpattern'] and pDict['stop'] in walllabels: # the first condition requires all walls to be present in the pattern. A way to ensure this is to have only extrema in the pattern - i.e. every p in pattern has exactly one 'm' or 'M'. This is why this condition exists in the input sanity check.
        matches.append(match)
        return matches
    else:
        for p,P in patterns:
            for n in WL.getNextNodes(startnode,pDict['outedges']):  # every filtered wall has an outgoing edge
                if len(match) == 1 or previouspattern in WL.pathDependentStringConstruction(match[-2],match[-1],n,pDict['walldomains'],pDict['outedges'],pDict['varsaffectedatwall'][match[-1]]): # consistency check to catch false positives
                    nextwalllabels=pDict['allwalllabels'][n]
                    if p in nextwalllabels: # if we hit the next pattern element, reduce pattern by one
                        # WE MAY GET FALSE POSITIVES WITHOUT THE CONSISTENCY CHECK ABOVE (this is because we have to pick the right q in the next step)
                        matches=recursePattern(n,match+[n],matches,patterns[1:],p,walllabels,pDict)
                    elif P and P in nextwalllabels and not repeatingLoop(match+[n]): # if we hit an intermediate node, call pattern without reduction provided there isn't a repeating loop 
                        matches=recursePattern(n,match+[n],matches,patterns,P,walllabels,pDict)
        return matches

def labelOptions(p):
    # Construct the intermediate nodes that are allowed for 
    # each word (p) in pattern. This algorithm depends on the
    # fact that there is exactly one 'm' or 'M' in each word.
    if 'm' in p:
        return p.replace('m','d')
    elif 'M' in p:
        return p.replace('M','u')
    else:
        return None

def sanityCheck(pattern):
    # Make sure the input pattern meets the requirements of the algorithm.
    if not pattern:
        return "None. Pattern is empty."
    notextrema = [p for p in pattern if not set(p).intersection(['m','M'])]
    if notextrema:
        return "None. Pattern element(s) {} are not extrema. An 'm' or 'M' is required in every element.".format(notextrema)
    return "sane"  

def matchCyclicPattern(pattern,origwallinds,outedges,walldomains,varsaffectedatwall,allwalllabels,showfirstwall=0,cyclewarn=1):
    '''
    This function finds paths in a directed graph that are consistent with a target pattern. The nodes
    of the directed graph are called walls, and each node is associated with a wall label (in walldomains)
    and a wall number (the index of the label in walldomains). The outgoing edges of a node with wall
    number w are stored in outedges at index w. Each element of outedges is a collection of wall numbers.
    The pattern is a sequence of words from the alphabet ('u','d','m','M'). The labels in walldomains
    will be transformed in a path-dependent manner into words of the same type. The paths in the graph 
    that have word labels that match the pattern will be returned as sequences of wall numbers. The graph
    will be reduced in size by the removal of boundary walls, steady states, and white walls, since these
    will not participate in cycles.

    The following variables are produced by the function preprocess in this module. See the code for more information.

    pattern: list of uniform-length words from the alphabet ('u','d','m','M'); exactly one 'm' or 'M' REQUIRED per string; patterns containing exactly repeating sequences will not be found if the same walls must be traversed to match the pattern
    origwallinds: list of integers denoting the original wall label in the full wall graph. The input data have been filtered to remove walls that cannot participate in a cycle, and the remaining walls have been renamed to the new indices of the filtered data. From now on, 'index wall n' means the wall associated with the index n in all of the filtered data.
    outedges: list of tuples of integers denoting a directed edge from the index wall to the tuple walls
    walldomains: list of tuples of floats denoting the variable values at the index wall
    varsaffectedatwall: list of integers reporting which variable is affected the index wall 
    allwalllabels: list of lists of uniform-length words from the alphabet ('u','d','m','M'); describing the possible wall labels at each node; at MOST there is one 'm' or 'M' per string

    showfirstwall and cyclewarn print informative messages for the user. By default, showfirstwall is turned off, since it exists only for tracking the progress of the code.

    See patternmatch_tests.py for examples of function calls.

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
    # alter pattern to cyclic if needed
    if pattern[0] != pattern[-1]:
        pattern.append(pattern[0])
        if cyclewarn:
            print 'Input pattern is assumed to cycle around in a loop.'
    # find all possible starting nodes for a matching path
    firstwalls=WL.getFirstwalls(pattern[0],allwalllabels)
    # return trivial length one patterns
    if len(pattern)==1:
        return [ (origwallinds.index(w),) for w in firstwalls ] or "None. No results found."
    # pre-cache intermediate nodes that may exist in the wall graph (saves time in recursive call)
    patternoptions=[labelOptions(p) for p in pattern[1:]]
    patternParams = zip(pattern[1:],patternoptions)
    paramDict = {'walldomains':walldomains,'outedges':outedges,'stop':pattern[-1],'lenpattern':len(pattern),'varsaffectedatwall':varsaffectedatwall,'allwalllabels':allwalllabels}
    # find matches
    results=[]
    if showfirstwall:
        print "All first walls {}".format([origwallinds.index(w) for w in firstwalls])
    for w in firstwalls:
        if showfirstwall:
            print "First wall {}".format(w)
        sys.stdout.flush() # force print messages thus far
        R = recursePattern(w,[w],[],patternParams,[],[],paramDict) # seek match starting at w
        results.extend([tuple(l) for l in R if l]) # pull out nonempty paths
    # now translate cyclic paths into original wall numbers; not guaranteed unique because not checking for identical paths that start at different nodes
    results = [tuple([origwallinds[r] for r in l]) for l in list(set(results)) if l[0]==l[-1]]
    return results or "None. No results found."

def callPatternMatch(basedir='',message=''):
    # basedir must contain the files outEdges.txt, walls.txt, patterns.txt, variables.txt, and 
    # equations.txt.
    if message:
        print "-"*len(message)
        print message
        print "-"*len(message)
    Patterns,origwallinds,outedges,walldomains,varsaffectedatwall,allwalllabels=preprocess(basedir) 
    for pattern in Patterns:
        print pattern
        print matchCyclicPattern(pattern, origwallinds,outedges,walldomains,varsaffectedatwall,allwalllabels,showfirstwall=1)

if __name__=='__main__':
    # walldomains=[(0,0.5),(0,1.5),(0.5,0),(0.5,1),(0.5,2),(1,0.5),(1,1.5),(1.5,0),(1.5,1),(1.5,2),(2,0.5),(2,1.5),(2.5,0),(2.5,1),(2.5,2),(3,0.5),(3,1.5)]
    # outedges=[(5,),(3,),(5,),(5,),(3,),(10,),(3,),(10,),(10,),(6,),(13,),(6,8),(13,),(11,),(11,),(13,),(11,)]
    # testStringConstruction(walldomains,outedges)

    # walldomains=[(0,0.5),(0,1.5),(0.5,0),(0.5,1),(0.5,2),(1,0.5),(1,1.5),(1.5,0),(1.5,1),(1.5,2),(2,0.5),(2,1.5),(2.5,0),(2.5,1),(2.5,2),(3,0.5),(3,1.5),(0.5,0.5)]
    # outedges=[(17,),(3,),(17,),(17,),(3,),(10,17),(3,),(10,),(10,),(6,),(13,),(6,8),(13,),(11,),(11,),(13,),(11,),(17,)]
    # testStringConstruction(walldomains,outedges)

    # Arnaud's simulation data
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

