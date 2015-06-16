import sys,itertools
import walllabels as WL
import preprocess as pp

#THIS MODULE USES MEMORY INSTEAD OF CPU

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

def recursePattern(startnode,match,matches,patterns,previouspattern,pDict,lenabort=3):
    if len(match) >= pDict['lenpattern'] and pDict['stop'] in pDict['allwalllabels'][match[-1]]: # Stop condition ensures that the whole pattern is in the match. For this to work, every word in the pattern must have exactly one 'm' or 'M' (pattern checked for this in the function sanityCheck). The algorithm excludes the insertion of intermediate extrema in the match. 
        matches.append(match)
        return matches
    else:
        for p,P in patterns:
            for n in pDict['outedges'][startnode]:  # every filtered wall has an outgoing edge
                if len(match)>lenabort*pDict['lenpattern']: # exclude long matches to avoid chaotic behavior
                    print "Aborting. Match is too long."
                else: 
                    nextwalllabels=pDict['allwalllabels'][n]
                    if p in nextwalllabels: # if we hit the next pattern element, reduce pattern by one
                        matches=recursePattern(n,match+[n],matches,patterns[1:],p,pDict)
                    if P in nextwalllabels and not repeatingLoop(match+[n]): # if we hit an intermediate node, call pattern without reduction provided there isn't a repeating loop 
                        matches=recursePattern(n,match+[n],matches,patterns,P,pDict)
        return matches

def filterFalsePositives(matches,pDict,patternParams):
    # consistency check to catch false positives
    filteredmatches=[]
    for match in matches:
        if match and match not in filteredmatches: goodmatch=1
        else: goodmatch=0
        if goodmatch:
            i=0
            for k in range(1,len(match)-1):
                pd = WL.pathDependentStringConstruction(match[k-1],match[k],match[k+1],pDict['walldomains'],pDict['outedges'],pDict['varsaffectedatwall'][match[k]],pDict['inedges'])
                p=set(pd).intersection(patternParams[i])
                # print (match[k-1],match[k],match[k+1]),pd,p,patternParams[i]
                if not p:
                    goodmatch=0
                    break
                if any(['m' in q or 'M' in q for q in p]):
                    i+=1
        if goodmatch:
            filteredmatches.append(match)
    return filteredmatches

def sanityCheck(pattern,allwalllabels,cyclewarn):
    '''
    Make sure the input pattern meets the requirements of the algorithm.

    '''
    # reject empty patterns
    if not pattern:
        return "None. Pattern is empty."
    # alter pattern to cyclic if needed
    if pattern[0] != pattern[-1]:
        pattern.append(pattern[0])
        if cyclewarn:
            print 'Input pattern is assumed to cycle around in a loop.'
    # every element of the pattern must have exactly one extremum
    badones = filter(None,[p if (p.count('m')+p.count('M'))!=1 else None for p in pattern])
    if badones:
        return "None. Pattern element(s) {} don't have exactly one 'm' or 'M'.".format(badones)
    # extrema must alternate between maxima and minima for every variable
    for k in range(len(pattern[0])):
        seq = filter(None,[p[k] if p[k] in ['m','M'] else None for p in pattern[:-1]])
        if len(seq)%2 != 0:
            return "None. Variable {} has an odd number of extrema.".format(k)
        elif len(seq) > 2 and ( set(seq[::2])==set(['m','M']) or set(seq[1::2])==set(['m','M']) ):
            return "None. Variable {} has two identical extrema in a row.".format(k)
    # check if any word in pattern is not a wall label (it's pointless to search in that case)
    awl = [a for l in allwalllabels for a in l]
    if not set(pattern).issubset(awl):
        return "None. No results found. Pattern contains an element that is not a wall label."
    # FIXME: ADD CHECK FOR REPEATING PATTERN
    return "sane"  

def matchPattern(pattern,origwallinds,outedges,walldomains,varsaffectedatwall,allwalllabels,inedges,showfirstwall=0,cyclewarn=1,showsanitycheck=0):
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
    S=sanityCheck(pattern,allwalllabels,cyclewarn)
    if S != "sane":
        if showsanitycheck:
            print S
        return S
    # find all possible starting nodes for a matching path
    firstwalls=WL.getFirstwalls(pattern[0],allwalllabels)
    # return trivial length one patterns
    if len(pattern)==1:
        return [ (origwallinds.index(w),) for w in firstwalls ] or "None. No results found."
    # pre-cache intermediate nodes that may exist in the wall graph (saves time in recursive call)
    intermediatenodes=[p.replace('m','d').replace('M','u') for p in pattern[1:]] 
    patternParams = zip(pattern[1:],intermediatenodes)
    paramDict = {'walldomains':walldomains,'outedges':outedges,'stop':pattern[-1],'lenpattern':len(pattern),'varsaffectedatwall':varsaffectedatwall,'allwalllabels':allwalllabels,'inedges':inedges}
    # find matches
    results=[]
    if showfirstwall:
        print "All first walls {}".format([origwallinds[w] for w in firstwalls])
    for w in firstwalls:
        if showfirstwall:
            print "First wall {}".format(origwallinds[w])
        sys.stdout.flush() # force print messages thus far
        R = recursePattern(w,[w],[],patternParams,[],paramDict) # seek match starting at w
        filteredR = filterFalsePositives(R,paramDict,patternParams)
        results.extend([tuple(l) for l in filteredR])
    # now translate cyclic paths into original wall numbers; not guaranteed unique because not checking for identical paths that start at different nodes; also, sorting out acyclic paths, since walls may share a wall label
    results = [tuple([origwallinds[r] for r in l]) for l in list(set(results)) if l[0]==l[-1]]
    return results or "None. No results found."

def callPatternMatch(basedir='',message=''):
    # basedir must contain the files outEdges.txt, walls.txt, patterns.txt, variables.txt, and 
    # equations.txt.
    # output printed to screen
    if message:
        print "\n"
        print "-"*len(message)
        print message
        print "-"*len(message)
        print "\n"
    print "Preprocessing..."
    Patterns,origwallinds,outedges,walldomains,varsaffectedatwall,allwalllabels,inedges,triples=pp.preprocess(basedir) 
    for pattern in Patterns:
        print "\n"
        print '-'*25
        print "Pattern: {}".format(pattern)
        match=matchPattern(pattern,origwallinds,outedges,walldomains,varsaffectedatwall, allwalllabels,inedges,showfirstwall=1)
        print "Results: {}".format(match)
        print '-'*25

def callPatternMatchJSON(basedir='',message=''):
    # basedir must contain the files output.json, patterns.txt, and equations.txt.
    # output printed to screen
    if message:
        print "\n"
        print "-"*len(message)
        print message
        print "-"*len(message)
        print "\n"
    print "Preprocessing..."
    Patterns,origwallindslist,outedgeslist,walldomainslist,varsaffectedatwalllist,allwalllabelslist,inedgeslist,parameterinds,tripleslist=pp.preprocessJSON(basedir)
    param=1
    for (origwallinds,outedges,walldomains,varsaffectedatwall,allwalllabels,inedges) in zip(origwallindslist,outedgeslist,walldomainslist,varsaffectedatwalllist,allwalllabelslist,inedgeslist): 
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
            match=matchPattern(pattern,origwallinds,outedges,walldomains,varsaffectedatwall, allwalllabels,inedges,showfirstwall=1)
            print "Results: {}".format(match)
            print '-'*25

def callPatternMatchJSONWriteFile(basedir='',message=''):
    # basedir must contain the files output.json, patterns.txt, and equations.txt.
    # positive results saved to file; negative results not recorded
    if message:
        print "\n"
        print "-"*len(message)
        print message
        print "-"*len(message)
        print "\n"
    print "Preprocessing..."
    Patterns,origwallindslist,outedgeslist,walldomainslist,varsaffectedatwalllist,allwalllabelslist,inedgeslist,parameterinds,tripleslist=pp.preprocessJSON(basedir)
    param=1
    f=open(basedir+'results.txt','w',0)
    for (origwallinds,outedges,walldomains,varsaffectedatwall,allwalllabels,inedges) in zip(origwallindslist,outedgeslist,walldomainslist,varsaffectedatwalllist,allwalllabelslist,inedgeslist): 
        print "\n"
        print "Morse set {} of {}".format(param,len(origwallindslist))
        print "Parameters={}".format(parameterinds[param-1])
        for pattern in Patterns:
            match=matchPattern(pattern,origwallinds,outedges,walldomains,varsaffectedatwall, allwalllabels,inedges,showfirstwall=0)
            if 'None' not in match:
                f.write('\n'+"Parameters={}".format(parameterinds[param-1])+'\n')
                f.write("Pattern: {}".format(pattern)+'\n')
                f.write("Results: {}".format(match)+'\n')
        param+=1
    f.close()

def callPatternMatchWithPatternGeneratorWriteFile(patternstart,patternremainder,basedir='',message=''):
    # basedir must contain the files outEdges.txt, walls.txt, variables.txt, patterngenerator.txt,
    # and equations.txt.
    # use when patterns.txt would take too much memory
    # positive results saved to file; negative results not recorded
    if message:
        print "\n"
        print "-"*len(message)
        print message
        print "-"*len(message)
        print "\n"
    print "Preprocessing..."
    patternstart,patternremainder,origwallinds,outedges,walldomains,varsaffectedatwall,allwalllabels,inedges,varnames,triples=pp.preprocessPatternGenerator(basedir) 
    f=open(basedir+'results.txt','w',0)
    for r in itertools.permutations(patternremainder):
        patterns=pp.constructPatternGenerator(patternstart+list(r),varnames)
        for pattern in patterns:
            flag='No match'
            match=matchPattern(pattern,origwallinds,outedges,walldomains,varsaffectedatwall, allwalllabels,inedges,showfirstwall=0)
            if 'None' not in match:
                flag='Match'
                f.write('\n'+"Parameters={}".format(parameterinds[param-1])+'\n')
                f.write("Pattern: {}".format(pattern)+'\n')
                f.write("Results: {}".format(match)+'\n')
        print flag
    f.close()
