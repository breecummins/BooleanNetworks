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
    allcombos = itertools.chain(*[itertools.combinations(range(len(alldeps)),n) for n in range(len(alldeps)+1)])
    nodestates = []
    # nodeinds = []
    for c in allcombos:
        # nodeinds.append(tuple([alldeps[k] for k in c]))
        ns = [0]*len(acts) + [1]*len(reps)
        for j in c:
            if j < len(acts):
                ns[j] = 1
            else:
                ns[j] = 0
        nodestates.append(tuple(ns))
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
