import itertools
import walllabels as wl
import preprocess as pp

def recursePattern(lastwall,currentwall,match,matches,patterns,wallinfo,cyclic):
    if len(patterns)==0:
        if (cyclic and match[0]==lastwall) or not cyclic: 
            matches.append(tuple(match))
    elif (lastwall,currentwall) in wallinfo:
        extremum,intermediate = patterns[0]
        for nextwall,labels in wallinfo[(lastwall,currentwall)]:
            if extremum in labels: # extrema = reduce pattern by one
                matches=recursePattern(currentwall,nextwall,match+[currentwall],matches,patterns[1:],wallinfo,cyclic)
            if intermediate in labels: # intermediate = same pattern
                matches=recursePattern(currentwall,nextwall,match+[currentwall],matches,patterns,wallinfo,cyclic)
    return matches

def recursePatternOneMatch(lastwall,currentwall,match,patterns,wallinfo,cyclic):
    # Throwing an error is a hacky kludge. I haven't been able to figure out how to fix it.
    if len(patterns)==0:
        if (cyclic and match[0]==lastwall) or not cyclic: 
            raise ValueError(str([tuple(match)]))
    elif (lastwall,currentwall) in wallinfo:
        extremum,intermediate = patterns[0]
        for nextwall,labels in wallinfo[(lastwall,currentwall)]:
            if extremum in labels: # extrema = reduce pattern by one
                matches=recursePatternOneMatch(currentwall,nextwall,match+[currentwall],patterns[1:],wallinfo,cyclic)
            if intermediate in labels: # intermediate = same pattern
                matches=recursePatternOneMatch(currentwall,nextwall,match+[currentwall],patterns,wallinfo,cyclic)
    return []


def matchPattern(pattern,wallinfo,cyclic=1,findallmatches=1):
    '''
    This function finds paths in a directed graph that are consistent with a target pattern. The nodes
    of the directed graph are called walls, and each node is associated with a wall label (in walldomains)
    and a wall number (the index of the label in walldomains). The outgoing edges of a node with wall
    number w are stored in outedges at index w. Each element of outedges is a collection of wall numbers. 

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

    The following variables are produced by functions in the module preprocess. See the code for more information.

    pattern: list of uniform-length words from the alphabet ('u','d','m','M'); exactly one 'm' or 'M' REQUIRED per string
    wallinfo:
        dictionary where keys are tuples (previouswall,currentwall) and values are lists of tuples 
        ( nextwall, list of wall labels for triple (previouswall,currentwall,nextwall) );
        the labels are uniform-length words from the alphabet ('u','d','m','M') with at most one of ['m','M']
    cyclic:
        cyclic=1 (default) means only cyclic paths are sought. cyclic=0 means acyclic paths are acceptable.
    findallmatches:
        findallmatches=1 (default) returns all matches. findallmatches=0 returns the first match. 

    See functions beginning with "call" below for example calls of this function.

    '''
    # check for empty patterns
    if not pattern:
        return "None. Pattern is empty."
    # check if any word in pattern is not a wall label (it's pointless to search in that case)
    flatlabels = set([w for _,list_of_labels in wallinfo.iteritems() for (_,labels) in list_of_labels for w in labels])
    if not set(pattern).issubset(flatlabels):
        return "None. No results found. Pattern contains an element that is not a wall label."
    # find all possible starting nodes for a matching path
    startwallpairs=wl.getFirstAndNextWalls(pattern[0],wallinfo)
    firstwalls,nextwalls=zip(*startwallpairs)
    # return trivial length one patterns
    if len(pattern)==1:
        return firstwalls
    # pre-cache intermediate nodes that may exist in the wall graph
    intermediatenodes=[p.replace('m','d').replace('M','u') for p in pattern[1:]] 
    patterns = zip(pattern[1:],intermediatenodes)
   # seek results
    if findallmatches: # find every path that matches the pattern
        results=[]
        for w,n in startwallpairs:
            matches = recursePattern(w,n,[w],[],patterns,wallinfo,cyclic) # seek match starting with w, n
            results.extend(matches) 
        # paths not guaranteed unique so use set()
        return list(set(results)) or "None. No results found."
    else: # find the first path that matches the pattern and quit 
        for w,n in startwallpairs:
            try:
                match = recursePatternOneMatch(w,n,[w],patterns,wallinfo,cyclic) # seek match starting with w, n
            except ValueError as v:
                match=eval(v.args[0])
            if match:
                break
        return match or "None. No results found."

def callPatternMatch(fname='dsgrn_output.json',pname='patterns.txt',rname='results.txt',cyclic=1,findallmatches=1, printtoscreen=0,writetofile=1):
    # output printed to screen
    print "Preprocessing..."
    patterns,wallinfo=pp.preprocess(fname,pname,cyclic) 
    print "Searching..."
    if writetofile: f=open(rname,'w',0)
    for pattern in patterns:
        matches=matchPattern(pattern,wallinfo,cyclic=cyclic,findallmatches=findallmatches)
        if printtoscreen:
            print "\n"
            print '-'*25
            print "Pattern: {}".format(pattern)
            print "Results: {}".format(matches)
            print '-'*25
        if writetofile and 'None' not in matches:
            f.write("Pattern: {}".format(pattern)+'\n')
            f.write("Results: {}".format(matches)+'\n')
    if writetofile: f.close()
