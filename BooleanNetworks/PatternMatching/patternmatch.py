import sys,itertools
import walllabels as WL
import preprocess as pp

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

def recursePattern(startnode,match,matches,patterns,previouspattern,pDict):
    if len(match) >= pDict['lenpattern'] and pDict['stop'] in pDict['allwalllabels'][match[-1]]: # the first condition requires all walls to be present in the pattern. A way to ensure this is to have only extrema in the pattern - i.e. every p in pattern has exactly one 'm' or 'M'. This is why this condition exists in the input sanity check.
        matches.append(match)
        return matches
    else:
        for p,P in patterns:
            for n in WL.getNextNodes(startnode,pDict['outedges']):  # every filtered wall has an outgoing edge
                if len(match)>100*pDict['lenpattern']:
                    print "Aborting. Match is too long."
                elif len(match) == 1 or previouspattern in WL.pathDependentStringConstruction(match[-2],match[-1],n,pDict['walldomains'],pDict['outedges'],pDict['varsaffectedatwall'][match[-1]]): # consistency check to catch false positives
                    nextwalllabels=pDict['allwalllabels'][n]
                    if p in nextwalllabels: # if we hit the next pattern element, reduce pattern by one
                        # WE MAY GET FALSE POSITIVES WITHOUT THE CONSISTENCY CHECK ABOVE (this is because we have to pick the right q in the next step)
                        matches=recursePattern(n,match+[n],matches,patterns[1:],p,pDict)
                    if P and P in nextwalllabels and not repeatingLoop(match+[n]): # if we hit an intermediate node, call pattern without reduction provided there isn't a repeating loop 
                        matches=recursePattern(n,match+[n],matches,patterns,P,pDict)
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

def wallLabelCheck(pattern,allwalllabels):
    awl = [a for l in allwalllabels for a in l]
    if not set(pattern).issubset(awl):
        return "None. No results found. Pattern contains element that is not a wall label."
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
    The graph is assumed to consist of a collection of nontrivial strongly connected components, since only 
    these nodes participate in cycles. (This reduction should have been performed in the preprocessing step.)

    The pattern is a sequence of words from the alphabet ('u','d','m','M'), with each word containing EXACTLY
    one 'm' or 'M'. The variable locations in walldomains will be transformed in a path-dependent manner into 
    words of the same type that have AT MOST one 'm' or 'M'. There can be at most one 'm' 
    or 'M' at each wall because we assume that the input graph arises from a switching network where each 
    regulation event occurs at a unique threshold. The paths in the graph that have word labels that 
    match the pattern will be returned as sequences of wall numbers. Intermediate wall labels may be inserted 
    into the pattern as long as they do not have an 'm' or 'M' in the label, and are consistent with the next 
    word in the pattern. Example: 'uMdd' in a four dimensional system means that the first variable is 
    increasing (up), the second variable is at a maximum (Max), and the third and fourth variables are 
    decreasing (down). The character 'm' means a variable is at a minimum (min). If the words 'uMdd' then 'udmd'
    appear in a pattern, the intermediate node 'uddd' may be inserted between these two in a match.

    The following variables are produced by the function preprocess in this module. See the code for more information.

    pattern: list of uniform-length words from the alphabet ('u','d','m','M'); exactly one 'm' or 'M' REQUIRED per string; patterns containing exactly repeating sequences will not be found if the same walls must be traversed to match the pattern
    origwallinds: list of integers denoting the original wall label in the full wall graph. The input data have been filtered to remove walls that cannot participate in a cycle, and the remaining walls have been renamed to the new indices of the filtered data. From now on, 'index wall n' means the wall associated with the index n in all of the filtered data.
    outedges: list of tuples of integers denoting a directed edge from the index wall to the tuple walls
    walldomains: list of tuples of floats denoting the variable values at the index wall
    varsaffectedatwall: list of integers reporting which variable is affected the index wall 
    allwalllabels: list of lists of uniform-length words from the alphabet ('u','d','m','M'); describing the possible wall labels at each node; at MOST there is one 'm' or 'M' per string

    showfirstwall and cyclewarn print informative messages for the user. By default, showfirstwall is turned off, since it exists only for tracking the progress of the code.

    See patternmatch_tests.py for examples of function calls.

    '''
    # sanity check the input, abort if insane 
    S=sanityCheck(pattern)
    if S != "sane":
        return S
    # check if any word in pattern is not a wall label
    # if so, there's no need to search
    W=wallLabelCheck(pattern,allwalllabels)
    if W:
        return W
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
        print "All first walls {}".format([origwallinds[w] for w in firstwalls])
    for w in firstwalls:
        if showfirstwall:
            print "First wall {}".format(origwallinds[w])
        sys.stdout.flush() # force print messages thus far
        R = recursePattern(w,[w],[],patternParams,[],paramDict) # seek match starting at w
        results.extend([tuple(l) for l in R if l]) # pull out nonempty paths
    # now translate cyclic paths into original wall numbers; not guaranteed unique because not checking for identical paths that start at different nodes
    results = [tuple([origwallinds[r] for r in l]) for l in list(set(results)) if l[0]==l[-1]]
    return results or "None. No results found."

def callPatternMatch(basedir='',message=''):
    # basedir must contain the files outEdges.txt, walls.txt, patterns.txt, variables.txt, and 
    # equations.txt.
    if message:
        print "\n"
        print "-"*len(message)
        print message
        print "-"*len(message)
        print "\n"
    print "Preprocessing..."
    Patterns,origwallinds,outedges,walldomains,varsaffectedatwall,allwalllabels=pp.preprocess(basedir) 
    for pattern in Patterns:
        print "\n"
        print '-'*25
        print "Pattern: {}".format(pattern)
        match=matchCyclicPattern(pattern,origwallinds,outedges,walldomains,varsaffectedatwall, allwalllabels,showfirstwall=1)
        print "Results: {}".format(match)
        print '-'*25

def callPatternMatchJSON(basedir='',message=''):
    # basedir must contain the files output.json, patterns.txt, and equations.txt.
    if message:
        print "\n"
        print "-"*len(message)
        print message
        print "-"*len(message)
        print "\n"
    print "Preprocessing..."
    Patterns,origwallindslist,outedgeslist,walldomainslist,varsaffectedatwalllist,allwalllabelslist,parameterinds=pp.preprocessJSON(basedir)
    param=1
    for (origwallinds,outedges,walldomains,varsaffectedatwall,allwalllabels) in zip(origwallindslist,outedgeslist,walldomainslist,varsaffectedatwalllist,allwalllabelslist): 
        print "\n"
        print '-'*50
        print "Morse set {} of {}".format(param,len(origwallindslist))
        print "Parameters={}".format(parameterinds[param-1])
        print '-'*50
        param+=1
        for pattern in Patterns:
            print "\n"
            print '-'*25
            print "Pattern: {}".format(pattern)
            match=matchCyclicPattern(pattern,origwallinds,outedges,walldomains,varsaffectedatwall, allwalllabels,showfirstwall=1)
            print "Results: {}".format(match)
            print '-'*25

def callPatternMatchJSONWriteFile(basedir='',message=''):
    # basedir must contain the files output.json, patterns.txt, and equations.txt.
    if message:
        print "\n"
        print "-"*len(message)
        print message
        print "-"*len(message)
        print "\n"
    print "Preprocessing..."
    Patterns,origwallindslist,outedgeslist,walldomainslist,varsaffectedatwalllist,allwalllabelslist,parameterinds=pp.preprocessJSON(basedir)
    param=1
    f=open(basedir+'results.txt','w')
    for (origwallinds,outedges,walldomains,varsaffectedatwall,allwalllabels) in zip(origwallindslist,outedgeslist,walldomainslist,varsaffectedatwalllist,allwalllabelslist): 
        print "\n"
        print "Morse set {} of {}".format(param,len(origwallindslist))
        print "Parameters={}".format(parameterinds[param-1])
        for pattern in Patterns:
            match=matchCyclicPattern(pattern,origwallinds,outedges,walldomains,varsaffectedatwall, allwalllabels,showfirstwall=0)
            if 'None' not in match:
                f.write('\n'+"Parameters={}".format(parameterinds[param-1])+'\n')
                f.write("Pattern: {}".format(pattern)+'\n')
                f.write("Results: {}".format(match)+'\n')
        param+=1
    f.close()

def constructPatternGenerator(sequence,varnames):
    # check that there is a max between each max/min pair (at least for 2 pairs)
    for v in varnames:
        m=sequence.count(v+' min')
        if m !=sequence.count(v+' max'):
            print 'No cyclic pattern possible. Check that number of maxima and minima match for every variable.'
            sequence=[]
            break
        elif sequence.count(v+' min')==2:
            i=sequence.index(v+' min')
            k=sequence[i+1:].index(v+' min')
            try:
                j=sequence[i+1:].index(v+' max')
                if j<k:
                    pass                
                else:
                    sequence=[]
                    break
            except:
                sequence=[]
                break
        elif sequence.count(v+'min')>2:
            print 'WARNING: More than 2 max/min pairs for one variable. Spurious patterns may be created.'
    if sequence:
        patternnames=[[s.split()[::2][0] for s in sequence]]
        patternmaxmin=[[s.split()[1::2][0] for s in sequence]]
        patterns=pp.constructCyclicPatterns(varnames,patternnames,patternmaxmin)
    else:
        patterns=[]
    return patterns
 

def callPatternMatchWithPatternGeneratorWriteFile(patternstart,patternremainder,basedir='',message=''):
    # basedir must contain the files outEdges.txt, walls.txt, variables.txt, patterngenerator.txt,
    # and equations.txt.
    if message:
        print "\n"
        print "-"*len(message)
        print message
        print "-"*len(message)
        print "\n"
    print "Preprocessing..."
    patternstart,patternremainder,origwallinds,outedges,walldomains,varsaffectedatwall,allwalllabels,varnames=pp.preprocessPatternGenerator(basedir) 
    f=open(basedir+'results.txt','w')
    for r in itertools.permutations(patternremainder):
        patterns=constructPatternGenerator(patternstart+list(r),varnames)
        for pattern in patterns:
            flag='No match'
            match=matchCyclicPattern(pattern,origwallinds,outedges,walldomains,varsaffectedatwall, allwalllabels,showfirstwall=0)
            if 'None' not in match:
                flag='Match'
                f.write('\n'+"Parameters={}".format(parameterinds[param-1])+'\n')
                f.write("Pattern: {}".format(pattern)+'\n')
                f.write("Results: {}".format(match)+'\n')
        print flag
    f.close()
