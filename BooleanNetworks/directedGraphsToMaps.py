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
    basestate = [0]*len(acts) + [1]*len(reps)
    for c in allcombos:
        ns = list(basestate)
        for j in c:
            if j in acts:
                ns[alldeps.index(j)] = 1
            else:
                ns[alldeps.index(j)] = 0
        nodestates.append(tuple(ns))

    def recurseMaps(maps,inds,templ):
        # start by taking combinations of 0's and 1's for the given state indices
        for p in itertools.product([1,0],repeat=len(inds)):
            tp = list(templ)
            for k,j in enumerate(inds):
                tp[j] = p[k]
            if len(acts) > 0:
                actons = [s for i,s in enumerate(inds) if p[i] == 1 and sum(nodestates[s][:len(acts)]) >= 1]
                actints = [int(''.join([str(a) for a in n]),2) for n in [nodestates[k][:len(acts)] for k in actons]]
            if len(reps) > 0:
                repoff = [s for i,s in enumerate(inds) if p[i] == 1 and sum(nodestates[s][len(acts):]) < len(reps)]
                repints = [int(''.join([str(a) for a in n]),2) for n in [nodestates[k][len(acts):] for k in repoff]]
            # propagate the 'actons' and 'repoff' forward; i.e., if first place is an 
            # activator and (1,0,0) maps to 1, then everything else with 1 in the first 
            # place (e.g. (1,0,1)) must map to 1 as well. Likewise, if last place is 
            # a repressor and (0,0,0) maps to 1, then everything else with a 0 in the 
            # last place must map to 1 as well.
            for k1,t in enumerate(tp):
                if len(acts) > 0:
                    baseactint = int(''.join([str(a) for a in nodestates[k1][:len(acts)]]),2)
                    if t == None and any([(baseactint & a) == a for a in actints]):
                        tp[k1] = 1
                if len(reps) > 0:
                    baserepint = int(''.join([str(a) for a in nodestates[k1][len(acts):]]),2)
                    if t == None and any([(baserepint | r) == r for r in repints]):
                        tp[k1] = 1
            nonecount = tp.count(None)
            if nonecount == 0:
                # if the map is complete, record it and continue
                maps.append(tp)
            elif nonecount == 1:
                # if there are two possible maps, record them and continue
                ind = tp.index(None)
                tp0 = list(tp)
                tp0[ind]=0
                maps.append(tp0)
                tp[ind]=1
                maps.append(tp)
            else:
                # There could be 4 or more possible maps, have to check. 
                # Find the indices of the smallest number of 'on' activators or 'off' repressors
                # and run the algorithm again.
                noneinds = [j for j in range(len(tp)) if tp[j]==None]
                if len(acts) > 0:
                    actsums = [sum(nodestates[j][:len(acts)]) for j in noneinds]
                    try:
                        minactsums = min([a for a in actsums if a !=0])
                    except:
                        minactsums = float('inf')
                else:
                    minactsums = float('inf')
                if len(reps) > 0:
                    repsums = [len(reps) - sum(nodestates[j][len(acts):]) for j in noneinds]
                    try:
                        minrepsums = min([r for r in repsums if r !=0])
                    except:
                        minrepsums = float('inf')
                else:
                    minrepsums = float('inf')
                if minactsums == minrepsums:
                    newinds = [j for k,j in enumerate(noneinds) if actsums[k] == minactsums or repsums[k] == minrepsums]
                elif minactsums < minrepsums:
                    newinds = [j for k,j in enumerate(noneinds) if actsums[k] == minactsums]
                elif minrepsums < minactsums:
                    try:
                        newinds = [j for k,j in enumerate(noneinds) if repsums[k] == minrepsums]
                    except:
                        raise ValueError('Node has no activators or repressors.')
                maps = recurseMaps(maps,newinds,tp)
        return maps

    template = [None]*len(nodestates)
    basestate = tuple(basestate)
    template[nodestates.index(basestate)] = 0
    highstate = tuple([int(not(b)) for b in basestate])
    template[nodestates.index(highstate)] = 1
    if len(nodestates) > 2:
        singleinds = [ j for j in range(len(nodestates)) if ( ( sum(nodestates[j][:len(acts)])==1 and sum(nodestates[j][len(acts):]) == len(reps) ) or (sum(nodestates[j][len(acts):])==len(reps)-1 and sum(nodestates[j][:len(acts)])==0) ) and template[j] == None ]
        maps = recurseMaps([],singleinds,template)
    else:
        maps = [template]
    return alldeps, nodestates, maps

def getConstraints(alldeps,nodestates,maps):
    return None

def prettyOutput(nodes,alldeps,nodestates,maps):
    deps = tuple([nodes[d] for d in alldeps])
    print("{0}".format(deps).replace("'", "")), 
    print('maps:'),
    L = len(str(deps).replace("'", "") + ' maps:')
    l = len(str(nodestates[0]))
    for k in range(1,len(maps)+1):
        if k < len(maps) and k < 9:
            print('{0} '.format(k)),
        elif k < len(maps) and k >= 9:
            print(k),
        else:
            print(k)
    print('-'*((L+3*len(maps))))
    for k,n in enumerate(nodestates):
        print(n),
        for i in range(len(maps)):
            if i == 0 and i < len(maps)-1:
                print(' '*(L-l) +'{0}'.format(maps[i][k])),
            elif i == 0 and i == len(maps)-1:
                print(' '*(L-l) +'{0}'.format(maps[i][k]))
            elif i < len(maps)-1:
                print(' {0}'.format(maps[i][k])),
            else:
                print(' {0}'.format(maps[i][k]))
    print('-'*((L+3*len(maps))))

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
    nodedeps = []
    nodedepstates = []
    nodemaps = []
    for k,n in enumerate(nodes):
        alldeps, nodestates, maps = makeMap(activatorinds[k],repressorinds[k])
        constraints = getConstraints(alldeps,nodestates,maps)
        print('Node {0}'.format(n))
        prettyOutput(nodes,alldeps,nodestates,maps)
        nodedeps.append(alldeps)
        nodedepstates.append(nodestates)
        nodemaps.append(maps)
    return nodes,nodedeps,nodedepstates,nodemaps
