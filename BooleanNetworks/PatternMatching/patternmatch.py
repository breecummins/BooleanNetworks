import preprocess as pp

def callPatternMatch(fname='dsgrn_output.json',pname='patterns.txt',rname='results.txt',cyclic=1,findallmatches=1, printtoscreen=0,writetofile=1): # pragma: no cover
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

def matchPattern(pattern,wallinfo,cyclic=1,findallmatches=1):
    '''
    This function finds paths in a directed graph that are consistent with a target pattern. The nodes
    of the directed graph are called walls, and each node is associated with a set of wall labels given 
    in the dictionary wallinfo. The wall labels are not unique, because the labeling is path dependendent. 
    For more details see the walllabels.py module. The walls themselves have integer labels that are used 
    to index wallinfo.

    The pattern is a list of words from the alphabet ('u','d','m','M'), with each word containing 
    EXACTLY one 'm' or 'M'. The letter 'u' means increasing (up), 'd' is decreasing, 'M' is a local max, 
    and 'm' is a local min. Example: 'uMdd' in a four dimensional system means that the first variable is 
    increasing, the second variable is at a maximum, and the third and fourth variables are decreasing. 
    The wall labels in wallinfo are words from the same alphabet and have AT MOST one 'm' or 'M'. There can 
    be at most one 'm' or 'M' at each wall because we assume that the wall graph arises from a switching
    network where each regulation event occurs at a unique threshold. 

    The paths in the graph that have word labels matching the pattern will be returned as a list of tuples 
    of wall integer labels. Intermediate wall labels may be inserted into the pattern as long as they do not 
    have an 'm' or 'M' in the label, and are consistent with the next word in the pattern.  For example, if 
    the words 'uMdd' then 'udmd' appear in a pattern, then repeats of the intermediate node 'uddd' may be 
    inserted between these two in a match.

    The following variables are produced by functions in the module preprocess.py.

    pattern: 
        list of uniform-length words from the alphabet ('u','d','m','M'); exactly one 'm' or 'M' REQUIRED 
        per string
    wallinfo:
        dictionary where the keys are tuples (previouswall,currentwall) and values are lists of tuples 
        ( nextwall, list of wall labels for triple (previouswall,currentwall,nextwall) );
        the labels are uniform-length words from the alphabet ('u','d','m','M') with at most one of ['m','M']
    cyclic:
        cyclic=1 (default) means only cyclic paths are sought. cyclic=0 means acyclic paths are acceptable.
    findallmatches:
        findallmatches=1 (default) returns all matches. findallmatches=0 returns the first match only. 

    See callPatternMatch() in this module for an example call of this function.

    '''
    # check for empty patterns
    if not pattern:
        return "None, no results found. Pattern is empty."
    # check if any word in pattern is not a wall label (it's pointless to search in that case)
    flatlabels = set([w for _,list_of_labels in wallinfo.iteritems() for (_,labels) in list_of_labels for w in labels])
    if not set(pattern).issubset(flatlabels):
        return "None, no results found. Pattern contains an element that is not a wall label."
    # find all possible starting nodes for a matching path
    startwallpairs=pathInitializer(pattern[0],wallinfo)
    # return trivial length one patterns
    if len(pattern)==1:
        return [s[0] for s in startwallpairs]
    # compute intermediate nodes that may exist in the wall graph
    intermediatenodes=[p.replace('m','d').replace('M','u') for p in pattern[1:]] 
    alternativepattern = zip(pattern[1:],intermediatenodes)
    # seek results
    if findallmatches: # find every path that matches the pattern
        results=[]
        for w,n in startwallpairs: # seek match starting with w, n
            matches = recursePattern(w,n,[w],[],alternativepattern,wallinfo,cyclic) 
            results.extend(matches) 
        return list(set(results)) or "None, no results found."
    else: # find the first path that matches the pattern and quit 
        for w,n in startwallpairs: # seek match starting with w, n
            try:
                match = recursePatternOneMatch(w,n,[w],alternativepattern,wallinfo,cyclic) 
            except ValueError as v:
                match=eval(v.args[0])
            if match:
                break
        return match or "None. No results found."

def pathInitializer(firstpattern,wallinfo):
    # Given the first word in the pattern, find the nodes in the graph that have 
    # this pattern for some path. 
    startwallpairs=[]
    for (lastwall,currentwall), list_of_labels in wallinfo.iteritems():
        for (nextwall,labels) in list_of_labels:
            if firstpattern in labels:
                startwallpairs.append((currentwall,nextwall))
    return list(set(startwallpairs))

def recursePattern(lastwall,currentwall,match,matches,pattern,wallinfo,cyclic):
    # Core algorithm for pattern matching.
    if len(pattern)==0:
        if (cyclic and match[0]==lastwall) or not cyclic: 
            matches.append(tuple(match))
    elif (lastwall,currentwall) in wallinfo:
        extremum,intermediate = pattern[0]
        for (nextwall,labels) in wallinfo[(lastwall,currentwall)]:
            if extremum in labels: # extremum = reduce pattern by one
                matches=recursePattern(currentwall,nextwall,match+[currentwall],matches,pattern[1:],wallinfo,cyclic)
            if intermediate in labels: # intermediate = same pattern
                matches=recursePattern(currentwall,nextwall,match+[currentwall],matches,pattern,wallinfo,cyclic)
    return matches

def recursePatternOneMatch(lastwall,currentwall,match,pattern,wallinfo,cyclic):
    # Stop after one match by throwing an error. Return the match in the error text (this is a hack).
    if len(pattern)==0:
        if (cyclic and match[0]==lastwall) or not cyclic: 
            raise ValueError(str([tuple(match)]))
    elif (lastwall,currentwall) in wallinfo:
        extremum,intermediate = pattern[0]
        for (nextwall,labels) in wallinfo[(lastwall,currentwall)]:
            if extremum in labels: # extremum = reduce pattern by one
                matches=recursePatternOneMatch(currentwall,nextwall,match+[currentwall],pattern[1:],wallinfo,cyclic)
            if intermediate in labels: # intermediate = same pattern
                matches=recursePatternOneMatch(currentwall,nextwall,match+[currentwall],pattern,wallinfo,cyclic)
    return []


