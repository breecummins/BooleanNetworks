import itertools

def nodesAndSigns(listofedges):
    '''
    Expects a list of tuples of the form (source_node_label,target_node_label,activator).
    
    Labels may be strings or numbers, and each unique label should refer to one and only
    one node. Every node must appear at least once as a source and at least once as a 
    target. This is an assumption of the underlying mathematical model, not a code 
    limitation.
    
    The last tuple element activator = 1 for an activating edge 
                                     = 0 for  a repressing edge

    Returns a tuple of unique nodes and two lists of index tuples, one pair of tuples per 
    node. Given node i, one tuple contains the indices of the activating nodes for node i 
    and the other the repressing nodes for node i.

    '''
    sources = []
    targets = []
    activators = []
    for e in listofedges:
        sources.append(e[0])
        targets.append(e[1])
        activators.append(e[2])
    nodes = set(targets)
    if nodes != set(sources):
        raise ValueError('All nodes must have at least one incoming and one outgoing edge.')
    nodes = tuple(nodes)
    activatorinds = []
    repressorinds = []
    for n in nodes:
        an = []
        rn = [] 
        for k,t in enumerate(targets):
            if n == t:
                ind = nodes.index(sources[k])
                if activators[k]:
                    an.append(ind)
                else:
                    rn.append(ind)
        activatorinds.append(tuple(an))
        repressorinds.append(tuple(rn))
    return nodes,activatorinds,repressorinds

def makeMap(acts,reps):
    '''
    Expects two tuples, one with indices for the activators and one for the repressors
    for a single node.

    '''
    alldeps = acts+reps
    allcombos = itertools.chain(*[itertools.combinations(alldeps,n) for n in range(len(alldeps)+1)])
    nodestates = []
    nodeinds = []
    for c in allcombos:
        nodeinds.append(c)
        ns = [0]*len(acts) + [1]*len(reps)
        for j in c:
            if j in acts:
                ns[alldeps.index(j)] = 1
            else:
                ns[alldeps.index(j)] = 0
        nodestates.append(tuple(ns))
    nodestateints = [int(''.join([str(a) for a in n]),2) for n in nodestates]

    def recurseMaps(maps,inds,templ):
        for p in itertools.product([1,0],repeat=len(inds)):
            tp = list(templ)
            for k,j in enumerate(inds):
                tp[j] = p[k]
            ons = [s for i,s in enumerate(inds) if p[i] == 1]
            for k1,t in enumerate(tp):
                if t == None and any([nodestateints[k1] & nodestateints[s] == nodestateints[s] for s in ons]):
                    tp[k1] = 1
            nonecount = tp.count(None)
            if nonecount == 0:
                maps.append(tp) 
            elif nonecount == 1:
                tp0 = list(tp)
                tp1 = list(tp)
                ind = tp.index(None)
                tp0[ind]=0
                tp1[ind]=1
                maps.append(tp0)
                maps.append(tp1)
            else:
                noneinds = [j for j in range(len(tp)) if tp[j]==None]
                minsums = min([sum(nodestates[j]) for j in noneinds])
                minsuminds = [j for j in noneinds if sum(nodestates[j]) == minsums]
                maps = recurseMaps(maps,minsuminds,tp)
        return maps


    template = [None]*len(nodestates)
    template[nodestateints.index(0)] = 0
    template[nodestateints.index(2**len(alldeps)-1)] = 1
    # find indices of single values
    singleinds = [j for j in range(len(nodestates)) if sum(nodestates[j])==1]
    if len(singleinds) != len(alldeps):
        raise ValueError('There is a logic bug here. Squish it.')

    maps = recurseMaps([],singleinds,template)

    print(nodeinds)
    print(nodestates)
    print(maps)
    # need to assign 1 or 0 for each nodestate consistent with Hill function framework
    # return alldeps, nodestates, maps

def makeAllMaps(nodes,activatorinds,repressorinds):
    pass
    # call makeMap inside for loop

def getConstraints():
    pass

def prettyOutput():
    pass

def translateNetworkToMaps(listofedges):
    '''
    Expects a list of tuples of the form (source_node_label,target_node_label,activator).
    
    Labels may be strings or numbers, and each unique label should refer to one and only
    one node. Every node must appear at least once as a source and at least once as a 
    target. This is an assumption of the underlying mathematical model, not a code 
    limitation.
    
    The last tuple element activator = 1 for an activating edge 
                                     = 0 for  a repressing edge

    Outputs acceptable Boolean maps consistent with the input directed graph.

    '''
    nodes,activatorinds,repressorinds = nodesAndSigns(listofedges)
    maps,nodeinds = makeAllMaps(nodes,activatorinds,repressorinds)
    constraints = getConstraints()
    prettyOutput(nodes,nodeinds,maps,constraints)
